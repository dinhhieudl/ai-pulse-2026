"""Tests for compare API endpoints."""

import pytest


@pytest.mark.asyncio
async def test_compare_two_models(client):
    resp = await client.get("/api/compare/?models=GPT-5.5,Claude 4.7 Opus")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 2
    models = {i["model"] for i in data["items"]}
    assert "GPT-5.5" in models
    assert any("Claude" in m for m in models)


@pytest.mark.asyncio
async def test_compare_case_insensitive(client):
    resp = await client.get("/api/compare/?models=gpt-5.5,deepseek-v3")
    data = resp.json()
    assert len(data["items"]) == 2


@pytest.mark.asyncio
async def test_compare_no_match(client):
    resp = await client.get("/api/compare/?models=NonExistentModel")
    data = resp.json()
    assert len(data["items"]) == 0


@pytest.mark.asyncio
async def test_compare_empty(client):
    resp = await client.get("/api/compare/?models=")
    data = resp.json()
    assert "items" in data


@pytest.mark.asyncio
async def test_list_all_models(client):
    resp = await client.get("/api/compare/all")
    assert resp.status_code == 200
    data = resp.json()
    assert "models" in data
    assert len(data["models"]) >= 10
    m = data["models"][0]
    assert "model" in m
    assert "provider" in m
    assert "elo_score" in m or "mmlu_score" in m
