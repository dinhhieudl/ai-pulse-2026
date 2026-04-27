"""MIT Technology Review — RSS + HTML scraper."""

from .rss_base import RSSScraper, make_id, classify, clean_text
from datetime import datetime, timezone


class MITTechScraper(RSSScraper):
    name = "MIT Technology Review"
    scraper_type = "news"
    URL = "https://www.technologyreview.com/topic/artificial-intelligence/"
    rss_url = "https://www.technologyreview.com/feed/"

    async def scrape(self) -> list[dict]:
        items = await self.fetch_rss()
        if items:
            return [i for i in items if "ai" in i["title"].lower() or "artificial" in i["title"].lower()
                    or "machine learning" in i["title"].lower() or "llm" in i["title"].lower()
                    or "gpt" in i["title"].lower() or "robot" in i["title"].lower()
                    or "model" in i["title"].lower() or "deepmind" in i["title"].lower()][:20] or items[:20]

        # Fallback HTML
        html = await self.fetch(self.URL)
        soup = self.soup(html)
        items = []

        for article in soup.select("article, div[class*='card'], div[class*='item'], a[data-testid*='link']"):
            title_el = article.select_one("h2 a, h3 a, a[class*='title'], h2, h3")
            if not title_el:
                continue

            if title_el.name == "a":
                title = title_el.get_text(strip=True)
                url = title_el.get("href", "")
            else:
                title = title_el.get_text(strip=True)
                link_el = title_el.find("a") or title_el.find_parent("a")
                url = link_el.get("href", "") if link_el else ""

            if not title or len(title) < 10:
                continue

            if url and not url.startswith("http"):
                url = f"https://www.technologyreview.com{url}"

            if not url:
                continue
            base = "https://www.technologyreview.com"
            path = url.replace(base, "").rstrip("/")
            if not path or path == "/topic/artificial-intelligence":
                continue

            summary_el = article.select_one("p, div[class*='desc'], div[class*='excerpt'], span[class*='dek']")
            summary = self.extract_text(summary_el, 280)

            time_el = article.select_one("time")
            published = time_el.get("datetime", "") if time_el else ""

            items.append({
                "id": make_id(url),
                "title": title,
                "summary": summary or f"MIT Technology Review: {title}",
                "url": url,
                "source": "MIT Technology Review",
                "category": classify(title),
                "sentiment": self._classify_sentiment(title, summary),
                "published": published,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        return items[:20]
