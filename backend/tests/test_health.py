"""Tests for health endpoint."""

import pytest


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["app"] == "AI Pulse 2026"
    assert "version" in data


@pytest.mark.asyncio
async def test_openapi_schema(client):
    """Verify OpenAPI schema is generated."""
    resp = await client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["info"]["title"] == "AI Pulse 2026 API"
    assert "3.0.0" in schema["info"]["version"]
    # All tag groups present
    tag_names = {t["name"] for t in schema.get("tags", [])}
    expected = {"health", "news", "leaderboard", "scrape", "bookmarks", "trends", "compare", "user-links", "digest"}
    assert expected.issubset(tag_names)


@pytest.mark.asyncio
async def test_swagger_ui(client):
    """Verify Swagger UI loads."""
    resp = await client.get("/docs", follow_redirects=True)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_redoc(client):
    """Verify ReDoc loads."""
    resp = await client.get("/redoc", follow_redirects=True)
    assert resp.status_code == 200
