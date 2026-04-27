"""Model Leaderboard API endpoints — multi-source."""

from fastapi import APIRouter, Query
from models import LEADERBOARD_DB

router = APIRouter()


@router.get("/")
def get_leaderboard(
    provider: str = Query(None, description="Filter by provider"),
    source: str = Query(None, description="Filter by source: LMSYS, Vellum, HuggingFace"),
    q: str = Query(None, description="Search model name"),
    sort_by: str = Query("rank", description="Sort: rank, mmlu_score, elo_score, pricing_input"),
    order: str = Query("asc", description="asc or desc"),
):
    """Return model leaderboard with multi-source filtering."""
    items = list(LEADERBOARD_DB)

    if provider:
        items = [i for i in items if provider.lower() in i["provider"].lower()]

    if source:
        items = [i for i in items if source.lower() in i.get("source", "").lower()]

    if q:
        q_lower = q.lower()
        items = [i for i in items if q_lower in i["model"].lower()]

    reverse = order == "desc"
    if sort_by in ("rank", "mmlu_score", "elo_score", "arena_elo", "speed_tps"):
        items.sort(key=lambda x: x.get(sort_by) or 0, reverse=reverse)
    elif sort_by == "model":
        items.sort(key=lambda x: x.get("model", ""), reverse=reverse)

    return {"total": len(items), "items": items}


@router.get("/providers")
def get_providers():
    """List all unique providers."""
    providers = list({i["provider"] for i in LEADERBOARD_DB})
    return {"providers": sorted(providers)}


@router.get("/sources")
def get_sources():
    """List all leaderboard data sources."""
    sources = list({i.get("source", "Unknown") for i in LEADERBOARD_DB})
    return {"sources": sorted(sources)}
