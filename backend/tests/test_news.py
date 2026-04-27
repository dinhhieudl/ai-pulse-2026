"""Tests for news API endpoints."""

import pytest
from models import NEWS_DB


@pytest.fixture(autouse=True)
def seed_news():
    """Seed demo news items into in-memory store."""
    NEWS_DB.clear()
    NEWS_DB.extend([
        {
            "id": "n1", "title": "GPT-5.5 Launch", "summary": "OpenAI releases GPT-5.5",
            "url": "https://openai.com/gpt-5", "source": "The Rundown AI",
            "category": "llm", "sentiment": "launch", "published": "2026-04-25",
        },
        {
            "id": "n2", "title": "Stable Diffusion 5 Open Source", "summary": "SD5 goes open-weight",
            "url": "https://stability.ai/sd5", "source": "VentureBeat",
            "category": "image_gen", "sentiment": "launch", "published": "2026-04-24",
        },
        {
            "id": "n3", "title": "Robot Learns Kitchen Tasks", "summary": "Figure 03 in the kitchen",
            "url": "https://figure.ai/03", "source": "Wired",
            "category": "robotics", "sentiment": "research", "published": "2026-04-23",
        },
    ])
    yield
    NEWS_DB.clear()


@pytest.mark.asyncio
async def test_list_news(client):
    resp = await client.get("/api/news/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3


@pytest.mark.asyncio
async def test_filter_by_category(client):
    resp = await client.get("/api/news/?category=llm")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["category"] == "llm"


@pytest.mark.asyncio
async def test_filter_by_source(client):
    resp = await client.get("/api/news/?source=wired")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["source"] == "Wired"


@pytest.mark.asyncio
async def test_search_news(client):
    resp = await client.get("/api/news/?q=robot")
    data = resp.json()
    assert data["total"] == 1
    assert "Robot" in data["items"][0]["title"]


@pytest.mark.asyncio
async def test_pagination(client):
    resp = await client.get("/api/news/?limit=1&offset=1")
    data = resp.json()
    assert data["total"] == 3
    assert len(data["items"]) == 1
    assert data["offset"] == 1


@pytest.mark.asyncio
async def test_news_sources(client):
    resp = await client.get("/api/news/sources")
    data = resp.json()
    assert "The Rundown AI" in data["sources"]
    assert "Wired" in data["sources"]


@pytest.mark.asyncio
async def test_news_categories(client):
    resp = await client.get("/api/news/categories")
    data = resp.json()
    assert data["categories"]["llm"] == 1
    assert data["categories"]["image_gen"] == 1
    assert data["categories"]["robotics"] == 1


@pytest.mark.asyncio
async def test_news_item_has_sentiment(client):
    resp = await client.get("/api/news/")
    items = resp.json()["items"]
    for item in items:
        assert "sentiment" in item
        assert item["sentiment"] in ("launch", "funding", "update", "research", "positive", "negative", "neutral")
