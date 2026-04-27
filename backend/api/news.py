"""News API endpoints."""

from fastapi import APIRouter, Query
from models import NEWS_DB

router = APIRouter()


@router.get(
    "/",
    summary="List news articles",
    description="Return news items with optional filtering by category, source, and full-text search. "
                "Items include sentiment classification (launch/funding/update/research/positive/negative/neutral).",
    responses={
        200: {
            "description": "Paginated list of news items",
            "content": {
                "application/json": {
                    "example": {
                        "total": 42,
                        "offset": 0,
                        "limit": 50,
                        "items": [
                            {
                                "id": "a1b2c3d4e5f6",
                                "title": "OpenAI Announces GPT-5.5",
                                "summary": "Latest model with native tool use...",
                                "url": "https://openai.com/index/gpt-5-5",
                                "source": "The Rundown AI",
                                "category": "llm",
                                "sentiment": "launch",
                                "published": "2026-04-25",
                            }
                        ],
                    }
                }
            },
        }
    },
)
def get_news(
    category: str = Query(None, description="Filter: llm, image_gen, robotics, other", examples=["llm"]),
    source: str = Query(None, description="Filter by source name (partial match)", examples=["ArXiv"]),
    q: str = Query(None, description="Full-text search in title and summary", examples=["GPT"]),
    limit: int = Query(50, ge=1, le=200, description="Max items to return"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
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


@router.get("/sources", summary="List all news sources")
def get_sources():
    """Return a sorted list of unique news source names."""
    sources = list({i["source"] for i in NEWS_DB})
    return {"sources": sorted(sources)}


@router.get("/categories", summary="List categories with counts")
def get_categories():
    """Return each category and how many articles it contains."""
    counts = {}
    for item in NEWS_DB:
        cat = item["category"]
        counts[cat] = counts.get(cat, 0) + 1
    return {"categories": counts}
