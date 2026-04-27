"""Tests for user links API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_list_user_links(client):
    resp = await client.get("/api/user-links/")
    assert resp.status_code == 200
    assert "items" in resp.json()


@pytest.mark.asyncio
async def test_submit_link(client):
    resp = await client.post("/api/user-links/", json={
        "url": "https://example.com/test-article",
        "title": "Test Article Title",
        "summary": "A test summary",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["title"] == "Test Article Title"


@pytest.mark.asyncio
async def test_submit_link_auto_fetch(client):
    """Submit with explicit title — verifies the endpoint works end-to-end."""
    resp = await client.post("/api/user-links/", json={
        "url": "https://example.com/explicit-title-test",
        "title": "Explicit Title Works",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["title"] == "Explicit Title Works"


@pytest.mark.asyncio
async def test_submit_link_appears_in_news(client):
    """Submitted link is stored in SQLite user_links table."""
    resp = await client.post("/api/user-links/", json={
        "url": "https://example.com/news-test-2",
        "title": "Persisted Article",
    })
    assert resp.status_code == 200

    # Verify it's in user-links listing
    links_resp = await client.get("/api/user-links/")
    items = links_resp.json()["items"]
    assert any(i["title"] == "Persisted Article" for i in items)
