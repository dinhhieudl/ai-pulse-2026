"""
AI Pulse 2026 — FastAPI Backend
Multi-source AI news + leaderboard aggregator.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import logging

from api.news import router as news_router
from api.leaderboard import router as leaderboard_router
from api.scrape import router as scrape_router
from scrapers.orchestrator import run_all_scrapers, run_all_scrapers_sync

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-pulse")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: run scraper once, then schedule every 30 min
    logger.info("🚀 AI Pulse 2026 backend starting...")
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_all_scrapers_sync, "interval", minutes=30, id="scrape_cycle")
    scheduler.start()
    logger.info("⏰ Scraper scheduled every 30 minutes")
    yield
    scheduler.shutdown()


app = FastAPI(
    title="AI Pulse 2026 API",
    version="2.0.0",
    description="Multi-source AI intelligence: news from Rundown/MIT/Wired/VentureBeat/ArXiv + benchmarks from LMSYS/Vellum/HuggingFace",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router, prefix="/api/news", tags=["news"])
app.include_router(leaderboard_router, prefix="/api/leaderboard", tags=["leaderboard"])
app.include_router(scrape_router, prefix="/api/scrape", tags=["scrape"])


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "AI Pulse 2026", "version": "2.0.0"}
