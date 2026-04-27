"""Scraper orchestrator — runs all scrapers, merges into SQLite + in-memory stores."""

import asyncio
import logging
from datetime import datetime, timezone
from models import NEWS_DB, LEADERBOARD_DB
from db import async_session
from db_models import NewsItemDB, LeaderboardEntryDB, ModelSnapshotDB
from sqlalchemy import select

# News scrapers
from scrapers.rundown import RundownScraper
from scrapers.mit_tech import MITTechScraper
from scrapers.wired import WiredScraper
from scrapers.venturebeat import VentureBeatScraper
from scrapers.arxiv import ArXivScraper

# Leaderboard scrapers
from scrapers.lmsys import LMSYSScraper
from scrapers.vellum import VellumScraper
from scrapers.huggingface import HFLeaderboardScraper

logger = logging.getLogger("ai-pulse.orchestrator")

NEWS_SCRAPERS = [
    RundownScraper(),
    MITTechScraper(),
    WiredScraper(),
    VentureBeatScraper(),
    ArXivScraper(),
]

LEADERBOARD_SCRAPERS = [
    LMSYSScraper(),
    VellumScraper(),
    HFLeaderboardScraper(),
]


async def save_news_to_db(items: list[dict]):
    """Persist news items to SQLite."""
    async with async_session() as session:
        for item in items:
            exists = await session.execute(
                select(NewsItemDB).where(NewsItemDB.id == item["id"])
            )
            if exists.scalar_one_or_none():
                continue
            db_item = NewsItemDB(
                id=item["id"],
                title=item.get("title", ""),
                summary=item.get("summary", ""),
                url=item.get("url", ""),
                source=item.get("source", ""),
                category=item.get("category", "other"),
                sentiment=item.get("sentiment", "neutral"),
                published=item.get("published", ""),
            )
            session.add(db_item)
        await session.commit()


async def save_leaderboard_to_db(items: list[dict]):
    """Persist leaderboard entries + take daily snapshot."""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    async with async_session() as session:
        for item in items:
            # Upsert leaderboard entry
            exists = await session.execute(
                select(LeaderboardEntryDB).where(
                    LeaderboardEntryDB.model == item["model"],
                    LeaderboardEntryDB.source == item.get("source", ""),
                )
            )
            existing = exists.scalar_one_or_none()
            if existing:
                existing.rank = item.get("rank", existing.rank)
                existing.mmlu_score = item.get("mmlu_score", existing.mmlu_score)
                existing.elo_score = item.get("elo_score", existing.elo_score)
                existing.arena_elo = item.get("arena_elo", existing.arena_elo)
                existing.pricing_input = item.get("pricing_input", existing.pricing_input)
                existing.pricing_output = item.get("pricing_output", existing.pricing_output)
                existing.speed_tps = item.get("speed_tps", existing.speed_tps)
                existing.notes = item.get("notes", existing.notes)
                existing.scraped_at = datetime.now(timezone.utc)
            else:
                db_item = LeaderboardEntryDB(
                    rank=item.get("rank", 0),
                    model=item["model"],
                    provider=item["provider"],
                    mmlu_score=item.get("mmlu_score"),
                    elo_score=item.get("elo_score"),
                    arena_elo=item.get("arena_elo"),
                    pricing_input=item.get("pricing_input"),
                    pricing_output=item.get("pricing_output"),
                    speed_tps=item.get("speed_tps"),
                    source=item.get("source", ""),
                    released=item.get("released"),
                    notes=item.get("notes"),
                    snapshot_date=today,
                )
                session.add(db_item)

            # Daily snapshot for trends (one per model per day)
            snap_exists = await session.execute(
                select(ModelSnapshotDB).where(
                    ModelSnapshotDB.model == item["model"],
                    ModelSnapshotDB.date == today,
                )
            )
            if not snap_exists.scalar_one_or_none():
                snapshot = ModelSnapshotDB(
                    date=today,
                    model=item["model"],
                    provider=item["provider"],
                    mmlu_score=item.get("mmlu_score"),
                    elo_score=item.get("elo_score") or item.get("arena_elo"),
                    pricing_input=item.get("pricing_input"),
                    pricing_output=item.get("pricing_output"),
                    speed_tps=item.get("speed_tps"),
                    source=item.get("source", ""),
                )
                session.add(snapshot)

        await session.commit()


async def run_all_scrapers():
    """Execute all scrapers concurrently and merge into DBs."""
    logger.info("🔄 Running all scrapers...")

    all_scrapers = NEWS_SCRAPERS + LEADERBOARD_SCRAPERS
    tasks = [s.run() for s in all_scrapers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    news_items = []
    leaderboard_items = []

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Scraper failed: {result}")
            continue
        if i < len(NEWS_SCRAPERS):
            news_items.extend(result)
        else:
            leaderboard_items.extend(result)

    # Merge news into in-memory store
    seen_ids = {item["id"] for item in NEWS_DB}
    added_news = 0
    for item in news_items:
        if item["id"] not in seen_ids:
            NEWS_DB.insert(0, item)
            seen_ids.add(item["id"])
            added_news += 1
    while len(NEWS_DB) > 200:
        NEWS_DB.pop()

    # Merge leaderboard
    if leaderboard_items:
        existing_keys = {(e["model"], e.get("source", "")) for e in LEADERBOARD_DB}
        added_lb = 0
        for item in leaderboard_items:
            key = (item["model"], item.get("source", ""))
            if key not in existing_keys:
                LEADERBOARD_DB.append(item)
                existing_keys.add(key)
                added_lb += 1
        logger.info(f"✅ Leaderboard: +{added_lb} entries from scrapers")

    # Persist to SQLite
    try:
        await save_news_to_db(news_items)
        await save_leaderboard_to_db(leaderboard_items)
        logger.info("✅ Saved to SQLite")
    except Exception as e:
        logger.error(f"SQLite save failed: {e}")

    logger.info(f"✅ News: +{added_news} new items (total: {len(NEWS_DB)})")
    logger.info(f"✅ Leaderboard: {len(LEADERBOARD_DB)} total entries")


def run_all_scrapers_sync():
    """Synchronous wrapper for APScheduler."""
    asyncio.run(run_all_scrapers())
