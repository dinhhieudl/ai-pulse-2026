"""The Rundown AI — RSS + HTML scraper."""

from .rss_base import RSSScraper, make_id, classify, clean_text
from datetime import datetime, timezone


class RundownScraper(RSSScraper):
    name = "The Rundown AI"
    scraper_type = "news"
    URL = "https://www.therundown.ai/"
    rss_url = "https://www.therundown.ai/feed"

    async def scrape(self) -> list[dict]:
        # Try RSS first
        items = await self.fetch_rss()
        if items:
            return items[:20]

        # Fallback to HTML
        html = await self.fetch(self.URL)
        soup = self.soup(html)
        items = []

        for article in soup.select("article, div[class*='post'], div[class*='article'], a[href*='/newsletter']"):
            title_el = article.select_one("h2, h3, h4, a[class*='title']")
            if not title_el:
                if article.name == "a":
                    title = article.get_text(strip=True)
                    url = article.get("href", "")
                else:
                    continue
            else:
                title = title_el.get_text(strip=True)
                link_el = title_el.find("a") or title_el.find_parent("a")
                url = link_el.get("href", "") if link_el else article.get("href", "")

            if not title or len(title) < 10:
                continue

            if url and not url.startswith("http"):
                url = f"https://www.therundown.ai{url}"

            if not url or url.rstrip("/") == "https://www.therundown.ai":
                continue
            path = url.replace("https://www.therundown.ai", "")
            if not path or path == "/":
                continue

            summary_el = article.select_one("p, div[class*='excerpt'], div[class*='desc']")
            summary = self.extract_text(summary_el, 280)

            items.append({
                "id": make_id(url),
                "title": title,
                "summary": summary or f"The Rundown AI: {title}",
                "url": url,
                "source": "The Rundown AI",
                "category": classify(title),
                "sentiment": self._classify_sentiment(title, summary),
                "published": "",
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        return items[:20]
