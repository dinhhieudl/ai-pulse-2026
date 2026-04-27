"""Shared test fixtures for AI Pulse 2026."""

import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from db import Base, get_session
from main import app


# ── In-memory SQLite for tests ────────────────────────────────────
TEST_DB_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DB_URL, echo=False)
TestSession = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


async def override_get_session():
    async with TestSession() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="session")
def event_loop():
    """Use a single event loop for all async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def setup_db():
    """Create all tables once per test session."""
    async with test_engine.begin() as conn:
        from db_models import NewsItemDB, LeaderboardEntryDB, BookmarkDB, UserLinkDB, ModelSnapshotDB
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """Async HTTP test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def db_session():
    """Direct DB session for seeding test data."""
    async with TestSession() as session:
        yield session
