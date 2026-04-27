"""Model Leaderboard API endpoints — multi-source."""

from fastapi import APIRouter, Query
from models import LEADERBOARD_DB

router = APIRouter()


@router.get(
    "/",
    summary="List model leaderboard",
    description="Return AI model rankings aggregated from LMSYS Chatbot Arena, Vellum LLM Leaderboard, "
                "and HuggingFace Open LLM Leaderboard. Includes ELO scores, MMLU benchmarks, pricing, and speed.",
    responses={
        200: {
            "description": "Leaderboard entries with optional filtering",
            "content": {
                "application/json": {
                    "example": {
                        "total": 10,
                        "items": [
                            {
                                "rank": 1,
                                "model": "GPT-5.5",
                                "provider": "OpenAI",
                                "mmlu_score": 93.2,
                                "elo_score": 1352,
                                "arena_elo": 1352,
                                "pricing_input": "$15.00",
                                "pricing_output": "$45.00",
                                "speed_tps": 85,
                                "source": "Combined",
                                "released": "2026-03",
                                "notes": "Multimodal, native tool use",
                            }
                        ],
                    }
                }
            },
        }
    },
)
def get_leaderboard(
    provider: str = Query(None, description="Filter by provider name", examples=["OpenAI"]),
    source: str = Query(None, description="Filter by data source", examples=["LMSYS Chatbot Arena"]),
    q: str = Query(None, description="Search model name", examples=["GPT"]),
    sort_by: str = Query("rank", description="Sort field: rank, mmlu_score, elo_score, arena_elo, speed_tps, model"),
    order: str = Query("asc", description="Sort order: asc or desc"),
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


@router.get("/providers", summary="List all model providers")
def get_providers():
    """Return a sorted list of unique provider names."""
    providers = list({i["provider"] for i in LEADERBOARD_DB})
    return {"providers": sorted(providers)}


@router.get("/sources", summary="List all leaderboard data sources")
def get_sources():
    """Return a sorted list of unique leaderboard data source names."""
    sources = list({i.get("source", "Unknown") for i in LEADERBOARD_DB})
    return {"sources": sorted(sources)}
