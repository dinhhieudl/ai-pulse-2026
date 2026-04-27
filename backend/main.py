"""
AI Pulse 2026 — FastAPI Backend
Multi-source AI news + leaderboard aggregator with SQLite persistence.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
import logging

from api.news import router as news_router
from api.leaderboard import router as leaderboard_router
from api.scrape import router as scrape_router
from api.bookmarks import router as bookmarks_router
from api.trends import router as trends_router
from api.compare import router as compare_router
from api.user_links import router as user_links_router
from api.digest import router as digest_router
from scrapers.orchestrator import run_all_scrapers, run_all_scrapers_sync
from db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ai-pulse")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB, run scraper once, then schedule every 30 min
    logger.info("🚀 AI Pulse 2026 backend starting...")

    await init_db()
    logger.info("✅ SQLite database initialized")

    scheduler = BackgroundScheduler()
    scheduler.add_job(run_all_scrapers_sync, "interval", minutes=30, id="scrape_cycle")
    scheduler.start()
    logger.info("⏰ Scraper scheduled every 30 minutes")

    # Run initial scrape in background
    import asyncio
    asyncio.create_task(run_all_scrapers())

    yield
    scheduler.shutdown()


app = FastAPI(
    title="AI Pulse 2026 API",
    version="3.0.0",
    description="Multi-source AI intelligence: news + benchmarks + bookmarks + trends + compare + digest",
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
app.include_router(bookmarks_router, prefix="/api/bookmarks", tags=["bookmarks"])
app.include_router(trends_router, prefix="/api/trends", tags=["trends"])
app.include_router(compare_router, prefix="/api/compare", tags=["compare"])
app.include_router(user_links_router, prefix="/api/user-links", tags=["user-links"])
app.include_router(digest_router, prefix="/api/digest", tags=["digest"])


@app.get("/api/health")
def health():
    return {"status": "ok", "app": "AI Pulse 2026", "version": "3.0.0"}
