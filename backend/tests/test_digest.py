"""Tests for digest API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_daily_digest(client):
    resp = await client.get("/api/digest/daily")
    assert resp.status_code == 200
    data = resp.json()
    assert "date" in data
    assert "news" in data
    assert "top_models" in data
    assert isinstance(data["news"], list)
    assert isinstance(data["top_models"], list)


@pytest.mark.asyncio
async def test_daily_digest_custom_date(client):
    resp = await client.get("/api/digest/daily?date=2026-04-01")
    assert resp.status_code == 200
    data = resp.json()
    assert data["date"] == "2026-04-01"


@pytest.mark.asyncio
async def test_weekly_digest(client):
    resp = await client.get("/api/digest/weekly")
    assert resp.status_code == 200
    data = resp.json()
    assert "period" in data
    assert "total_articles" in data
    assert "by_category" in data
    assert "news" in data


@pytest.mark.asyncio
async def test_telegram_digest(client):
    resp = await client.get("/api/digest/telegram")
    assert resp.status_code == 200
    data = resp.json()
    assert "text" in data
    assert "AI Pulse" in data["text"]


@pytest.mark.asyncio
async def test_telegram_digest_full(client):
    resp = await client.get("/api/digest/telegram?format=full")
    assert resp.status_code == 200
    assert "text" in resp.json()
