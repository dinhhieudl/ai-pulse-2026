"""
AI Pulse 2026 — FastAPI Backend
Multi-source AI news + leaderboard aggregator with SQLite persistence.

API Documentation:
  - Swagger UI:  http://localhost:8000/docs
  - ReDoc:       http://localhost:8000/redoc
  - OpenAPI JSON: http://localhost:8000/openapi.json
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
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

TAGS_METADATA = [
    {
        "name": "health",
        "description": "Service health check.",
    },
    {
        "name": "news",
        "description": "AI news articles from 5 sources (The Rundown AI, MIT Technology Review, Wired, VentureBeat, ArXiv). "
                       "Supports filtering by category, source, and full-text search.",
    },
    {
        "name": "leaderboard",
        "description": "AI model leaderboard aggregated from LMSYS Chatbot Arena, Vellum LLM Leaderboard, "
                       "and HuggingFace Open LLM Leaderboard. Includes ELO scores, MMLU benchmarks, pricing, and speed.",
    },
    {
        "name": "scrape",
        "description": "Trigger manual scrape cycles. Scrapers run automatically every 30 minutes.",
    },
    {
        "name": "bookmarks",
        "description": "Save and manage bookmarked articles. Bookmarks persist in SQLite.",
    },
    {
        "name": "trends",
        "description": "Model performance trends over time (daily snapshots) and provider coverage statistics.",
    },
    {
        "name": "compare",
        "description": "Side-by-side comparison of 2–4 AI models across ELO, MMLU, pricing, and speed.",
    },
    {
        "name": "user-links",
        "description": "Submit external article URLs. Auto-fetches title and description metadata.",
    },
    {
        "name": "digest",
        "description": "Daily and weekly AI news digests. Includes a Telegram-formatted endpoint for push notifications.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 AI Pulse 2026 backend starting...")
    await init_db()
    logger.info("✅ SQLite database initialized")

    scheduler = BackgroundScheduler()
    scheduler.add_job(run_all_scrapers_sync, "interval", minutes=30, id="scrape_cycle")
    scheduler.start()
    logger.info("⏰ Scraper scheduled every 30 minutes")

    import asyncio
    asyncio.create_task(run_all_scrapers())

    yield
    scheduler.shutdown()


app = FastAPI(
    title="AI Pulse 2026 API",
    description=(
        "🤖 **AI Pulse 2026** — Multi-source AI intelligence platform.\n\n"
        "Aggregates AI news from 5 sources and model benchmarks from 3 leaderboards. "
        "Includes bookmarks, model comparison, price calculator, trend charts, "
        "sentiment analysis, and daily/weekly digests.\n\n"
        "### Features\n"
        "- 📰 **News Feed** — 5 sources, auto-classified by category & sentiment\n"
        "- 🏆 **Leaderboard** — ELO, MMLU, pricing, speed from LMSYS/Vellum/HuggingFace\n"
        "- ⭐ **Bookmarks** — Save articles for later\n"
        "- 📊 **Trends** — Model score tracking over time\n"
        "- 🔄 **Compare** — Side-by-side model comparison\n"
        "- 💰 **Price Calculator** — Estimate API costs\n"
        "- 📬 **Digest** — Daily/weekly summaries, Telegram-ready\n"
        "- 🔗 **User Links** — Submit articles with auto-metadata\n"
    ),
    version="3.0.0",
    openapi_tags=TAGS_METADATA,
    contact={
        "name": "AI Pulse 2026",
        "url": "https://github.com/dinhhieudl/ai-pulse-2026",
    },
    license_info={
        "name": "MIT",
    },
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


@app.get("/api/health", tags=["health"], summary="Health check")
def health():
    """Return service health status and version."""
    return {"status": "ok", "app": "AI Pulse 2026", "version": "3.0.0"}
