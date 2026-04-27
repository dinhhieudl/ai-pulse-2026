"""Shared data models and in-memory store."""

from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel


class NewsItem(BaseModel):
    id: str
    title: str
    summary: str
    url: str
    source: str
    category: str  # "llm" | "image_gen" | "robotics" | "other"
    published: Optional[str] = None
    scraped_at: str = datetime.now(timezone.utc).isoformat()


class LeaderboardEntry(BaseModel):
    rank: int
    model: str
    provider: str
    # Scores (different sources use different metrics)
    mmlu_score: Optional[float] = None
    elo_score: Optional[float] = None
    arena_elo: Optional[float] = None
    # Pricing
    pricing_input: Optional[str] = None
    pricing_output: Optional[str] = None
    # Performance
    speed_tps: Optional[float] = None  # tokens per second
    # Meta
    source: str = ""
    released: Optional[str] = None
    notes: Optional[str] = None
    scraped_at: str = datetime.now(timezone.utc).isoformat()


# ── In-memory stores ──────────────────────────────────────────────
NEWS_DB: list[dict] = []
LEADERBOARD_DB: list[dict] = [
    {
        "rank": 1, "model": "GPT-5.5", "provider": "OpenAI",
        "mmlu_score": 93.2, "elo_score": 1352, "arena_elo": 1352,
        "pricing_input": "$15.00", "pricing_output": "$45.00",
        "speed_tps": 85,
        "source": "Combined", "released": "2026-03",
        "notes": "Multimodal, native tool use, best overall",
    },
    {
        "rank": 2, "model": "Claude 4.7 Opus", "provider": "Anthropic",
        "mmlu_score": 92.8, "elo_score": 1348, "arena_elo": 1348,
        "pricing_input": "$20.00", "pricing_output": "$60.00",
        "speed_tps": 62,
        "source": "Combined", "released": "2026-02",
        "notes": "200K context, safety-first, best reasoning",
    },
    {
        "rank": 3, "model": "Gemini 2.5 Ultra", "provider": "Google",
        "mmlu_score": 92.5, "elo_score": 1341, "arena_elo": 1341,
        "pricing_input": "$12.00", "pricing_output": "$36.00",
        "speed_tps": 92,
        "source": "Combined", "released": "2026-01",
        "notes": "Native multimodal, fast inference",
    },
    {
        "rank": 4, "model": "MiMo-V2-Pro", "provider": "Xiaomi",
        "mmlu_score": 91.8, "elo_score": 1332, "arena_elo": 1332,
        "pricing_input": "$8.00", "pricing_output": "$24.00",
        "speed_tps": 78,
        "source": "Combined", "released": "2026-04",
        "notes": "Efficient reasoning, edge-ready, great value",
    },
    {
        "rank": 5, "model": "Grok-3", "provider": "xAI",
        "mmlu_score": 90.1, "elo_score": 1325, "arena_elo": 1325,
        "pricing_input": "$10.00", "pricing_output": "$30.00",
        "speed_tps": 88,
        "source": "Combined", "released": "2026-01",
        "notes": "Real-time web knowledge, X integrated",
    },
    {
        "rank": 6, "model": "Llama 4 405B", "provider": "Meta",
        "mmlu_score": 91.0, "elo_score": 1318, "arena_elo": 1318,
        "pricing_input": "Free (open)", "pricing_output": "Free (open)",
        "speed_tps": 45,
        "source": "Combined", "released": "2026-03",
        "notes": "Best open-weight, MoE architecture",
    },
    {
        "rank": 7, "model": "DeepSeek-V3", "provider": "DeepSeek",
        "mmlu_score": 89.7, "elo_score": 1310, "arena_elo": 1310,
        "pricing_input": "$2.00", "pricing_output": "$6.00",
        "speed_tps": 95,
        "source": "Combined", "released": "2025-12",
        "notes": "Ultra-low cost, strong coding",
    },
    {
        "rank": 8, "model": "Mistral Large 3", "provider": "Mistral AI",
        "mmlu_score": 90.5, "elo_score": 1305, "arena_elo": 1305,
        "pricing_input": "$6.00", "pricing_output": "$18.00",
        "speed_tps": 72,
        "source": "Combined", "released": "2026-02",
        "notes": "European sovereignty focus",
    },
    {
        "rank": 9, "model": "Qwen-3 72B", "provider": "Alibaba",
        "mmlu_score": 88.8, "elo_score": 1298, "arena_elo": 1298,
        "pricing_input": "$4.00", "pricing_output": "$12.00",
        "speed_tps": 68,
        "source": "Combined", "released": "2026-03",
        "notes": "Multilingual, open-weight",
    },
    {
        "rank": 10, "model": "Command R++", "provider": "Cohere",
        "mmlu_score": 89.2, "elo_score": 1290, "arena_elo": 1290,
        "pricing_input": "$5.00", "pricing_output": "$15.00",
        "speed_tps": 75,
        "source": "Combined", "released": "2026-01",
        "notes": "RAG-native, enterprise optimized",
    },
]
