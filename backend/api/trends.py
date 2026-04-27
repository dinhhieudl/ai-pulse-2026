"""Trends API — model performance trends over time + provider stats."""

from fastapi import APIRouter, Query, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db_models import ModelSnapshotDB, NewsItemDB
from datetime import datetime, timedelta

router = APIRouter()


@router.get(
    "/models",
    summary="Model score trends",
    description="Return daily snapshots of model scores (ELO, MMLU, speed) for trend charts. "
                "Snapshots are taken each scrape cycle. Filter by model name and time range.",
    responses={
        200: {
            "description": "Trend data grouped by model",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "model": "GPT-5.5",
                                "provider": "OpenAI",
                                "data_points": [
                                    {"date": "2026-04-25", "mmlu_score": 93.2, "elo_score": 1352, "speed_tps": 85},
                                    {"date": "2026-04-26", "mmlu_score": 93.2, "elo_score": 1353, "speed_tps": 86},
                                ],
                            }
                        ]
                    }
                }
            },
        }
    },
)
async def model_trends(
    model: str = Query(None, description="Filter by model name (partial match)", examples=["GPT"]),
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    session: AsyncSession = Depends(get_session),
):
    """Return model score snapshots over time for trend charts."""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    query = select(ModelSnapshotDB).where(ModelSnapshotDB.date >= cutoff)
    if model:
        query = query.where(ModelSnapshotDB.model.ilike(f"%{model}%"))
    query = query.order_by(ModelSnapshotDB.date)

    result = await session.execute(query)
    snapshots = result.scalars().all()

    trends = {}
    for s in snapshots:
        if s.model not in trends:
            trends[s.model] = {
                "model": s.model,
                "provider": s.provider,
                "data_points": [],
            }
        trends[s.model]["data_points"].append({
            "date": s.date,
            "mmlu_score": s.mmlu_score,
            "elo_score": s.elo_score,
            "speed_tps": s.speed_tps,
        })

    return {"items": list(trends.values())}


@router.get(
    "/providers",
    summary="Provider coverage statistics",
    description="Return news coverage stats: article counts by source, by category, and by sentiment. "
                "Useful for seeing which AI providers/topics are getting the most coverage.",
    responses={
        200: {
            "description": "Coverage breakdown",
            "content": {
                "application/json": {
                    "example": {
                        "by_source": [
                            {"source": "The Rundown AI", "count": 15},
                            {"source": "ArXiv", "count": 12},
                        ],
                        "by_category": [
                            {"category": "llm", "count": 30},
                            {"category": "image_gen", "count": 8},
                        ],
                        "by_sentiment": [
                            {"sentiment": "launch", "count": 20},
                            {"sentiment": "research", "count": 10},
                        ],
                    }
                }
            },
        }
    },
)
async def provider_coverage(
    days: int = Query(30, ge=1, le=365, description="Number of days to look back"),
    session: AsyncSession = Depends(get_session),
):
    """Return provider mention counts in news — who's getting the most coverage."""
    cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")

    result = await session.execute(
        select(NewsItemDB.source, func.count(NewsItemDB.id))
        .where(NewsItemDB.created_at >= cutoff)
        .group_by(NewsItemDB.source)
        .order_by(func.count(NewsItemDB.id).desc())
    )
    rows = result.all()

    cat_result = await session.execute(
        select(NewsItemDB.category, func.count(NewsItemDB.id))
        .where(NewsItemDB.created_at >= cutoff)
        .group_by(NewsItemDB.category)
    )
    cat_rows = cat_result.all()

    sent_result = await session.execute(
        select(NewsItemDB.sentiment, func.count(NewsItemDB.id))
        .where(NewsItemDB.created_at >= cutoff)
        .group_by(NewsItemDB.sentiment)
    )
    sent_rows = sent_result.all()

    return {
        "by_source": [{"source": r[0], "count": r[1]} for r in rows],
        "by_category": [{"category": r[0], "count": r[1]} for r in cat_rows],
        "by_sentiment": [{"sentiment": r[0], "count": r[1]} for r in sent_rows],
    }
