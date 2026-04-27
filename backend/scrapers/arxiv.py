"""ArXiv AI papers scraper (cs.AI via RSS)."""

from .rss_base import RSSScraper, make_id, classify, clean_text
from datetime import datetime, timezone
import re


class ArXivScraper(RSSScraper):
    name = "ArXiv"
    scraper_type = "news"
    rss_url = "https://rss.arxiv.org/rss/cs.AI"

    async def scrape(self) -> list[dict]:
        items = await self.fetch_rss()
        if items:
            return items

        # Fallback to raw parsing
        import feedparser
        import httpx

        async with httpx.AsyncClient(
            headers={"User-Agent": "AI-Pulse-2026/1.0"},
            follow_redirects=True, timeout=20,
        ) as client:
            resp = await client.get(self.rss_url)
            resp.raise_for_status()

        feed = feedparser.parse(resp.text)
        items = []

        for entry in feed.entries[:25]:
            raw_title = entry.get("title", "").strip()
            title_match = re.search(r'\]\s*(.+)$', raw_title)
            title = title_match.group(1) if title_match else raw_title

            url = entry.get("link", "")
            if not url:
                arxiv_id = re.search(r'(\d{4}\.\d{4,5})', raw_title)
                if arxiv_id:
                    url = f"https://arxiv.org/abs/{arxiv_id.group(1)}"

            summary = entry.get("summary", entry.get("description", ""))
            summary = re.sub(r"<[^>]+>", "", summary)
            summary = re.sub(r"^(Abstract:|arXiv:.*?)\s*", "", summary).strip()
            summary = clean_text(summary, 300)

            if not title or len(title) < 5:
                continue

            items.append({
                "id": make_id(url),
                "title": title,
                "summary": summary or f"New paper: {title}",
                "url": url,
                "source": "ArXiv",
                "category": classify(title),
                "sentiment": "research",
                "published": entry.get("published", entry.get("updated", "")),
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        return items
