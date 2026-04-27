"""Scraper orchestrator — runs all scrapers and merges results into stores."""

import asyncio
import logging
from models import NEWS_DB, LEADERBOARD_DB

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


async def run_all_scrapers():
    """Execute all scrapers concurrently and merge into DBs."""
    logger.info("🔄 Running all scrapers...")

    # Run news + leaderboard scrapers concurrently
    all_scrapers = NEWS_SCRAPERS + LEADERBOARD_SCRAPERS
    tasks = [s.run() for s in all_scrapers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    # Process news results
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

    # Merge news (deduplicate by id)
    seen_ids = {item["id"] for item in NEWS_DB}
    added_news = 0
    for item in news_items:
        if item["id"] not in seen_ids:
            NEWS_DB.insert(0, item)
            seen_ids.add(item["id"])
            added_news += 1

    # Keep only latest 200 news items
    while len(NEWS_DB) > 200:
        NEWS_DB.pop()

    # Merge leaderboard (replace if new data, keep fallback if empty)
    if leaderboard_items:
        # Merge by (model, source) — each source contributes its own rankings
        existing_keys = {(e["model"], e.get("source", "")) for e in LEADERBOARD_DB}
        added_lb = 0
        for item in leaderboard_items:
            key = (item["model"], item.get("source", ""))
            if key not in existing_keys:
                LEADERBOARD_DB.append(item)
                existing_keys.add(key)
                added_lb += 1
        logger.info(f"✅ Leaderboard: +{added_lb} entries from scrapers")

    logger.info(f"✅ News: +{added_news} new items (total: {len(NEWS_DB)})")
    logger.info(f"✅ Leaderboard: {len(LEADERBOARD_DB)} total entries")


def run_all_scrapers_sync():
    """Synchronous wrapper for APScheduler."""
    asyncio.run(run_all_scrapers())
