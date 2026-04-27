"""Tests for leaderboard API endpoints."""

import pytest
from models import LEADERBOARD_DB


@pytest.fixture(autouse=True)
def seed_leaderboard():
    """Ensure demo leaderboard is populated."""
    # LEADERBOARD_DB is pre-seeded in models.py with 10 entries
    yield


@pytest.mark.asyncio
async def test_list_leaderboard(client):
    resp = await client.get("/api/leaderboard/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 10
    assert len(data["items"]) >= 10


@pytest.mark.asyncio
async def test_filter_by_provider(client):
    resp = await client.get("/api/leaderboard/?provider=OpenAI")
    data = resp.json()
    assert data["total"] >= 1
    assert all("OpenAI" in i["provider"] for i in data["items"])


@pytest.mark.asyncio
async def test_search_model(client):
    resp = await client.get("/api/leaderboard/?q=GPT")
    data = resp.json()
    assert data["total"] >= 1
    assert any("GPT" in i["model"] for i in data["items"])


@pytest.mark.asyncio
async def test_sort_by_elo_desc(client):
    resp = await client.get("/api/leaderboard/?sort_by=elo_score&order=desc")
    data = resp.json()
    elos = [i.get("elo_score") or i.get("arena_elo") or 0 for i in data["items"]]
    assert elos == sorted(elos, reverse=True)


@pytest.mark.asyncio
async def test_leaderboard_providers(client):
    resp = await client.get("/api/leaderboard/providers")
    data = resp.json()
    assert "OpenAI" in data["providers"]
    assert "Anthropic" in data["providers"]


@pytest.mark.asyncio
async def test_leaderboard_sources(client):
    resp = await client.get("/api/leaderboard/sources")
    data = resp.json()
    assert len(data["sources"]) >= 1


@pytest.mark.asyncio
async def test_leaderboard_item_fields(client):
    resp = await client.get("/api/leaderboard/")
    item = resp.json()["items"][0]
    assert "rank" in item
    assert "model" in item
    assert "provider" in item
    # At least one score field present
    assert any(item.get(k) for k in ("mmlu_score", "elo_score", "arena_elo"))
