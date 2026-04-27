"""Wired AI — RSS + HTML scraper."""

from .rss_base import RSSScraper, make_id, classify, clean_text
from datetime import datetime, timezone


class WiredScraper(RSSScraper):
    name = "Wired"
    scraper_type = "news"
    URL = "https://www.wired.com/tag/artificial-intelligence/"
    rss_url = "https://www.wired.com/feed/tag/ai/latest/rss"

    async def scrape(self) -> list[dict]:
        items = await self.fetch_rss()
        if items:
            return items[:20]

        # Fallback HTML
        html = await self.fetch(self.URL)
        soup = self.soup(html)
        items = []

        for article in soup.select("article, div[class*='card'], li[class*='item']"):
            title_el = article.select_one("h2 a, h3 a, a[data-testid*='title']")
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            url = title_el.get("href", "")
            if not url.startswith("http"):
                url = f"https://www.wired.com{url}"

            if not title or len(title) < 10:
                continue

            path = url.replace("https://www.wired.com", "").rstrip("/")
            if not path or path == "/tag/artificial-intelligence":
                continue

            summary_el = article.select_one("p, div[class*='desc'], div[class*='excerpt']")
            summary = self.extract_text(summary_el, 280)

            time_el = article.select_one("time")
            published = time_el.get("datetime", "") if time_el else ""

            items.append({
                "id": make_id(url),
                "title": title,
                "summary": summary or f"Wired: {title}",
                "url": url,
                "source": "Wired",
                "category": classify(title),
                "sentiment": self._classify_sentiment(title, summary),
                "published": published,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        return items[:20]
