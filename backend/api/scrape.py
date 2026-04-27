"""Manual scrape trigger endpoint."""

from fastapi import APIRouter
from scrapers.orchestrator import run_all_scrapers

router = APIRouter()


@router.post(
    "/run",
    summary="Trigger scrape cycle",
    description="Manually trigger all scrapers to fetch fresh news and leaderboard data. "
                "Scrapers also run automatically every 30 minutes.",
    responses={
        200: {
            "description": "Scrape completed successfully",
            "content": {"application/json": {"example": {"status": "ok", "message": "Scrape cycle completed"}}},
        }
    },
)
async def trigger_scrape():
    """Manually trigger a scrape cycle."""
    await run_all_scrapers()
    return {"status": "ok", "message": "Scrape cycle completed"}
