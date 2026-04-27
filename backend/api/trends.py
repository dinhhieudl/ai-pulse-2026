"""Trends API — model performance trends over time + provider stats."""

from fastapi import APIRouter, Query, Depends
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db_models import ModelSnapshotDB, NewsItemDB
from datetime import datetime, timedelta

router = APIRouter()


@router.get("/models")
async def model_trends(
    model: str = Query(None, description="Filter by model name"),
    days: int = Query(30, ge=1, le=365),
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

    # Group by model
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


@router.get("/providers")
async def provider_coverage(
    days: int = Query(30, ge=1, le=365),
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

    # Also count by category
    cat_result = await session.execute(
        select(NewsItemDB.category, func.count(NewsItemDB.id))
        .where(NewsItemDB.created_at >= cutoff)
        .group_by(NewsItemDB.category)
    )
    cat_rows = cat_result.all()

    # Sentiment breakdown
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
