"""Digest API — generate daily/weekly AI news summaries."""

from fastapi import APIRouter, Query, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db_models import NewsItemDB, LeaderboardEntryDB
from datetime import datetime, timedelta

router = APIRouter()


@router.get(
    "/daily",
    summary="Daily news digest",
    description="Generate a digest of top news articles and top-5 leaderboard models for a given day.",
    responses={
        200: {
            "description": "Daily digest",
            "content": {
                "application/json": {
                    "example": {
                        "date": "2026-04-25",
                        "news": [
                            {
                                "title": "OpenAI Announces GPT-5.5",
                                "url": "https://openai.com/index/gpt-5-5",
                                "source": "The Rundown AI",
                                "category": "llm",
                                "sentiment": "launch",
                            }
                        ],
                        "top_models": [
                            {"rank": 1, "model": "GPT-5.5", "provider": "OpenAI", "elo_score": 1352}
                        ],
                    }
                }
            },
        }
    },
)
async def daily_digest(
    date: str = Query(None, description="Date in YYYY-MM-DD format (defaults to today)", examples=["2026-04-25"]),
    session: AsyncSession = Depends(get_session),
):
    """Generate a digest of top news for a given day."""
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")

    result = await session.execute(
        select(NewsItemDB)
        .where(NewsItemDB.created_at >= date)
        .where(NewsItemDB.created_at < f"{date} 23:59:59")
        .order_by(NewsItemDB.created_at.desc())
        .limit(10)
    )
    news = result.scalars().all()

    lb_result = await session.execute(
        select(LeaderboardEntryDB)
        .order_by(LeaderboardEntryDB.rank)
        .limit(5)
    )
    top_models = lb_result.scalars().all()

    return {
        "date": date,
        "news": [
            {
                "title": n.title,
                "url": n.url,
                "source": n.source,
                "category": n.category,
                "sentiment": n.sentiment,
            }
            for n in news
        ],
        "top_models": [
            {
                "rank": m.rank,
                "model": m.model,
                "provider": m.provider,
                "elo_score": m.elo_score or m.arena_elo,
            }
            for m in top_models
        ],
    }


@router.get(
    "/weekly",
    summary="Weekly news digest",
    description="Generate a digest of the past 7 days, including article count breakdown by category.",
    responses={
        200: {
            "description": "Weekly digest",
            "content": {
                "application/json": {
                    "example": {
                        "period": "2026-04-18 to 2026-04-25",
                        "total_articles": 42,
                        "by_category": {"llm": 30, "image_gen": 8, "robotics": 4},
                        "news": [],
                    }
                }
            },
        }
    },
)
async def weekly_digest(
    session: AsyncSession = Depends(get_session),
):
    """Generate a digest of the past week."""
    cutoff = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

    result = await session.execute(
        select(NewsItemDB)
        .where(NewsItemDB.created_at >= cutoff)
        .order_by(NewsItemDB.created_at.desc())
        .limit(20)
    )
    news = result.scalars().all()

    cat_result = await session.execute(
        select(NewsItemDB.category, func.count(NewsItemDB.id))
        .where(NewsItemDB.created_at >= cutoff)
        .group_by(NewsItemDB.category)
    )
    categories = {r[0]: r[1] for r in cat_result.all()}

    return {
        "period": f"{cutoff} to {datetime.utcnow().strftime('%Y-%m-%d')}",
        "total_articles": len(news),
        "by_category": categories,
        "news": [
            {
                "title": n.title,
                "url": n.url,
                "source": n.source,
                "category": n.category,
                "sentiment": n.sentiment,
            }
            for n in news
        ],
    }


@router.get(
    "/telegram",
    summary="Telegram-formatted digest",
    description="Generate a plain-text digest optimized for Telegram messages. "
                "Includes top news with emoji sentiment indicators and top-3 models.",
    responses={
        200: {
            "description": "Telegram-ready text",
            "content": {
                "application/json": {
                    "example": {
                        "text": "🤖 AI Pulse — 2026-04-25\n\n📰 Top News:\n🚀 OpenAI Announces GPT-5.5\n   https://openai.com/...\n\n🏆 Top Models:\n  #1 GPT-5.5 (OpenAI) — ELO: 1352"
                    }
                }
            },
        }
    },
)
async def telegram_digest(
    format: str = Query("short", description="short (5 items) or full (10 items)"),
    session: AsyncSession = Depends(get_session),
):
    """Generate a Telegram-friendly text digest."""
    date = datetime.utcnow().strftime("%Y-%m-%d")

    result = await session.execute(
        select(NewsItemDB)
        .where(NewsItemDB.created_at >= date)
        .order_by(NewsItemDB.created_at.desc())
        .limit(5 if format == "short" else 10)
    )
    news = result.scalars().all()

    lb_result = await session.execute(
        select(LeaderboardEntryDB)
        .order_by(LeaderboardEntryDB.rank)
        .limit(3)
    )
    top3 = lb_result.scalars().all()

    lines = [f"🤖 AI Pulse — {date}\n"]

    if news:
        lines.append("📰 Top News:")
        for i, n in enumerate(news, 1):
            emoji = {"launch": "🚀", "funding": "💰", "research": "🔬", "update": "⬆️"}.get(n.sentiment, "📌")
            lines.append(f"{emoji} {n.title}")
            lines.append(f"   {n.url}\n")

    if top3:
        lines.append("🏆 Top Models:")
        for m in top3:
            elo = m.elo_score or m.arena_elo or "?"
            lines.append(f"  #{m.rank} {m.model} ({m.provider}) — ELO: {elo}")

    return {"text": "\n".join(lines)}
