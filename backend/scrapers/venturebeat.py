"""VentureBeat AI scraper."""

from .base import BaseScraper, make_id, classify, clean_text
from datetime import datetime, timezone


class VentureBeatScraper(BaseScraper):
    name = "venturebeat"
    URL = "https://venturebeat.com/category/ai/"

    async def scrape(self) -> list[dict]:
        html = await self.fetch(self.URL)
        soup = self.soup(html)
        items = []

        for article in soup.select("article, div.article-card, div.featured-post, div[class*='article']"):
            title_el = article.select_one("h2 a, h3 a, a.article-title, a[class*='title']")
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            url = title_el.get("href", "")
            if not url.startswith("http"):
                url = f"https://venturebeat.com{url}"

            if not title or len(title) < 10:
                continue

            # Skip items that just link to the category page
            path = url.replace("https://venturebeat.com", "").rstrip("/")
            if not path or path == "/category/ai":
                continue

            summary_el = article.select_one("p.article-excerpt, p.excerpt, div.entry-content p, p[class*='desc']")
            summary = self.extract_text(summary_el, 280)

            time_el = article.select_one("time")
            published = time_el.get("datetime", "") if time_el else ""

            items.append({
                "id": make_id(url),
                "title": title,
                "summary": summary or f"VentureBeat: {title}",
                "url": url,
                "source": "VentureBeat",
                "category": classify(title),
                "published": published,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        return items[:20]
