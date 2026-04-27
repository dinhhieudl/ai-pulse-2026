"""Compare API — side-by-side model comparison."""

from fastapi import APIRouter, Query
from models import LEADERBOARD_DB

router = APIRouter()


@router.get("/")
async def compare_models(
    models: str = Query(..., description="Comma-separated model names to compare"),
):
    """Compare multiple models side by side."""
    requested = [m.strip().lower() for m in models.split(",") if m.strip()]
    if not requested:
        return {"items": [], "error": "No models specified"}

    matched = []
    for req in requested:
        for entry in LEADERBOARD_DB:
            if req in entry["model"].lower():
                matched.append(entry)
                break

    return {"items": matched}


@router.get("/all")
async def list_all_models():
    """Return all model names for the compare picker."""
    return {
        "models": [
            {
                "model": e["model"],
                "provider": e["provider"],
                "elo_score": e.get("elo_score") or e.get("arena_elo"),
                "mmlu_score": e.get("mmlu_score"),
            }
            for e in LEADERBOARD_DB
        ]
    }
