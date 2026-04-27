"""Manual scrape trigger endpoint."""

from fastapi import APIRouter
from scrapers.orchestrator import run_all_scrapers
import asyncio

router = APIRouter()


@router.post("/run")
async def trigger_scrape():
    """Manually trigger a scrape cycle."""
    await run_all_scrapers()
    return {"status": "ok", "message": "Scrape cycle completed"}
