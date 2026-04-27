"""Compare API — side-by-side model comparison."""

from fastapi import APIRouter, Query
from models import LEADERBOARD_DB

router = APIRouter()


@router.get(
    "/",
    summary="Compare models",
    description="Compare 2–4 AI models side by side. Pass comma-separated model names. "
                "Returns full leaderboard entries for matched models.",
    responses={
        200: {
            "description": "Matched model entries for comparison",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "rank": 1, "model": "GPT-5.5", "provider": "OpenAI",
                                "mmlu_score": 93.2, "elo_score": 1352,
                                "pricing_input": "$15.00", "pricing_output": "$45.00",
                                "speed_tps": 85,
                            },
                            {
                                "rank": 2, "model": "Claude 4.7 Opus", "provider": "Anthropic",
                                "mmlu_score": 92.8, "elo_score": 1348,
                                "pricing_input": "$20.00", "pricing_output": "$60.00",
                                "speed_tps": 62,
                            },
                        ]
                    }
                }
            },
        }
    },
)
async def compare_models(
    models: str = Query(..., description="Comma-separated model names to compare", examples=["GPT-5.5,Claude 4.7 Opus"]),
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


@router.get(
    "/all",
    summary="List all models",
    description="Return all model names with basic info (provider, ELO, MMLU) for the compare picker UI.",
    responses={
        200: {
            "description": "All available models",
            "content": {
                "application/json": {
                    "example": {
                        "models": [
                            {"model": "GPT-5.5", "provider": "OpenAI", "elo_score": 1352, "mmlu_score": 93.2},
                            {"model": "Claude 4.7 Opus", "provider": "Anthropic", "elo_score": 1348, "mmlu_score": 92.8},
                        ]
                    }
                }
            },
        }
    },
)
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
