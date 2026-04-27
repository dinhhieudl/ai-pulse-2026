"""News API endpoints."""

from fastapi import APIRouter, Query
from models import NEWS_DB

router = APIRouter()


@router.get("/")
def get_news(
    category: str = Query(None, description="Filter: llm, image_gen, robotics, other"),
    source: str = Query(None, description="Filter by source name"),
    q: str = Query(None, description="Search query"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Return news items with optional filtering and search."""
    items = list(NEWS_DB)

    if category:
        items = [i for i in items if i["category"] == category]

    if source:
        items = [i for i in items if source.lower() in i["source"].lower()]

    if q:
        q_lower = q.lower()
        items = [
            i for i in items
            if q_lower in i["title"].lower() or q_lower in i["summary"].lower()
        ]

    total = len(items)
    items = items[offset : offset + limit]

    return {
        "total": total,
        "offset": offset,
        "limit": limit,
        "items": items,
    }


@router.get("/sources")
def get_sources():
    """List all unique news sources."""
    sources = list({i["source"] for i in NEWS_DB})
    return {"sources": sorted(sources)}


@router.get("/categories")
def get_categories():
    """List categories with counts."""
    counts = {}
    for item in NEWS_DB:
        cat = item["category"]
        counts[cat] = counts.get(cat, 0) + 1
    return {"categories": counts}
