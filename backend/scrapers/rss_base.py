"""RSS-based scraper base — more reliable than HTML scraping."""

import feedparser
import httpx
from datetime import datetime, timezone
from .base import BaseScraper, make_id, classify, clean_text
import logging
import re

logger = logging.getLogger("ai-pulse.rss")


class RSSScraper(BaseScraper):
    """Base class for RSS feed scrapers. Much more stable than HTML parsing."""

    rss_url: str = ""

    async def fetch_rss(self) -> list[dict]:
        """Fetch and parse RSS feed, return standardized items."""
        items = []
        try:
            async with httpx.AsyncClient(
                headers={"User-Agent": "AI-Pulse-2026/1.0"},
                follow_redirects=True,
                timeout=20,
            ) as client:
                resp = await client.get(self.rss_url)
                resp.raise_for_status()
                feed = feedparser.parse(resp.text)

            for entry in feed.entries[:25]:
                title = entry.get("title", "").strip()
                if not title or len(title) < 10:
                    continue

                url = entry.get("link", "")
                if not url:
                    continue

                # Clean up title (remove arXiv prefix patterns)
                title = re.sub(r"^arXiv:\d+\.\d+\s*\[.*?\]\s*", "", title)

                summary = entry.get("summary", entry.get("description", ""))
                # Strip HTML tags from summary
                summary = re.sub(r"<[^>]+>", "", summary)
                summary = clean_text(summary, 300)

                published = entry.get("published", entry.get("updated", ""))

                items.append({
                    "id": make_id(url),
                    "title": title,
                    "summary": summary or f"{self.name}: {title}",
                    "url": url,
                    "source": self.name,
                    "category": classify(title),
                    "sentiment": self._classify_sentiment(title, summary),
                    "published": published,
                    "scraped_at": datetime.now(timezone.utc).isoformat(),
                })

        except Exception as e:
            logger.error(f"[{self.name}] RSS fetch failed: {e}")

        return items

    def _classify_sentiment(self, title: str, summary: str) -> str:
        """Classify news sentiment based on keywords."""
        text = f"{title} {summary}".lower()
        if any(k in text for k in ["launch", "release", "announce", "unveil", "introduce", "debut"]):
            return "launch"
        if any(k in text for k in ["funding", "raise", "invest", "valuation", "ipo", "acquisition"]):
            return "funding"
        if any(k in text for k in ["update", "upgrade", "improve", "enhance", "new version"]):
            return "update"
        if any(k in text for k in ["paper", "research", "study", "benchmark", "arxiv", "findings"]):
            return "research"
        if any(k in text for k in ["controversy", "concern", "risk", "ban", "regulate", "lawsuit", "bias"]):
            return "negative"
        if any(k in text for k in ["partnership", "collaboration", "open-source", "free", "breakthrough"]):
            return "positive"
        return "neutral"
