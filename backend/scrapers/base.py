"""Base scraper class with shared HTTP + parsing utilities."""

import httpx
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import logging
import hashlib
import re

logger = logging.getLogger("ai-pulse.scraper")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def make_id(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()[:12]


def classify(title: str) -> str:
    """Heuristic category classifier based on title keywords."""
    t = title.lower()
    if any(kw in t for kw in ["robot", "humanoid", "actuator", "boston dynamics", "figure", "1x", "embodied"]):
        return "robotics"
    if any(kw in t for kw in ["image", "dall-e", "midjourney", "stable diffusion", "sora",
                                "video gen", "flux", "imagen", "gen-3", "veo", "diffusion"]):
        return "image_gen"
    if any(kw in t for kw in ["llm", "gpt", "claude", "gemini", "llama", "mistral",
                                "language model", "reasoning", "mimo", "qwen", "deepseek",
                                "grok", "foundation model", "transformer", "benchmark",
                                "mmlu", "arena", "chatbot"]):
        return "llm"
    return "other"


def clean_text(text: str, max_len: int = 300) -> str:
    """Remove excess whitespace and truncate."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_len] if len(text) > max_len else text


class BaseScraper(ABC):
    """Every scraper inherits this. Implement `scrape()` returning list[dict]."""

    name: str = "base"
    scraper_type: str = "news"  # "news" or "leaderboard"

    async def fetch(self, url: str) -> str:
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=25) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.text

    async def fetch_json(self, url: str) -> dict:
        async with httpx.AsyncClient(headers=HEADERS, follow_redirects=True, timeout=25) as client:
            resp = await client.get(url)
            resp.raise_for_status()
            return resp.json()

    def soup(self, html: str) -> BeautifulSoup:
        return BeautifulSoup(html, "lxml")

    def extract_text(self, element, max_len: int = 300) -> str:
        if element is None:
            return ""
        return clean_text(element.get_text(separator=" ", strip=True), max_len)

    @abstractmethod
    async def scrape(self) -> list[dict]:
        """Return list of dicts matching either NewsItem or LeaderboardEntry schema."""
        ...

    async def run(self) -> list[dict]:
        logger.info(f"🕷️  [{self.name}] Starting scrape...")
        try:
            items = await self.scrape()
            logger.info(f"✅ [{self.name}] Got {len(items)} items")
            return items
        except Exception as e:
            logger.error(f"❌ [{self.name}] Failed: {e}")
            return []
