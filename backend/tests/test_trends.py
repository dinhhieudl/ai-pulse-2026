"""Tests for trends API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_model_trends(client):
    resp = await client.get("/api/trends/models")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_model_trends_filter(client):
    resp = await client.get("/api/trends/models?model=GPT&days=7")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_provider_stats(client):
    resp = await client.get("/api/trends/providers")
    assert resp.status_code == 200
    data = resp.json()
    assert "by_source" in data
    assert "by_category" in data
    assert "by_sentiment" in data
    assert isinstance(data["by_source"], list)
    assert isinstance(data["by_category"], list)
    assert isinstance(data["by_sentiment"], list)


@pytest.mark.asyncio
async def test_provider_stats_days_filter(client):
    resp = await client.get("/api/trends/providers?days=7")
    assert resp.status_code == 200
    assert "by_source" in resp.json()
