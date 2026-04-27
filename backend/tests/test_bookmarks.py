"""Tests for bookmarks API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_list_bookmarks_empty(client):
    resp = await client.get("/api/bookmarks/")
    assert resp.status_code == 200
    assert "items" in resp.json()


@pytest.mark.asyncio
async def test_create_bookmark(client):
    resp = await client.post("/api/bookmarks/", json={
        "news_id": "test_bm_1",
        "title": "Test Article",
        "url": "https://example.com/article",
        "source": "Test Source",
        "category": "llm",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["id"] == "bm_test_bm_1"


@pytest.mark.asyncio
async def test_create_duplicate_bookmark(client):
    """Should reject duplicate bookmarks."""
    payload = {
        "news_id": "test_bm_dup",
        "title": "Dup Article",
        "url": "https://example.com/dup",
    }
    resp1 = await client.post("/api/bookmarks/", json=payload)
    assert resp1.status_code == 200

    resp2 = await client.post("/api/bookmarks/", json=payload)
    assert resp2.status_code == 409


@pytest.mark.asyncio
async def test_delete_bookmark(client):
    # Create
    await client.post("/api/bookmarks/", json={
        "news_id": "test_bm_del",
        "title": "To Delete",
        "url": "https://example.com/delete",
    })

    # Delete
    resp = await client.delete("/api/bookmarks/bm_test_bm_del")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_delete_nonexistent_bookmark(client):
    resp = await client.delete("/api/bookmarks/bm_does_not_exist")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_bookmark_persists(client):
    await client.post("/api/bookmarks/", json={
        "news_id": "test_bm_persist",
        "title": "Persist Test",
        "url": "https://example.com/persist",
    })
    resp = await client.get("/api/bookmarks/")
    items = resp.json()["items"]
    assert any(i["news_id"] == "test_bm_persist" for i in items)
