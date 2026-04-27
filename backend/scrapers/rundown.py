"""The Rundown AI — daily AI newsletter scraper."""

from .base import BaseScraper, make_id, classify, clean_text
from datetime import datetime, timezone


class RundownScraper(BaseScraper):
    name = "rundown"
    URL = "https://www.therundown.ai/"

    async def scrape(self) -> list[dict]:
        html = await self.fetch(self.URL)
        soup = self.soup(html)
        items = []

        # The Rundown uses article cards on homepage
        for article in soup.select("article, div[class*='post'], div[class*='article'], a[href*='/newsletter']"):
            title_el = article.select_one("h2, h3, h4, a[class*='title']")
            if not title_el:
                # Try if the element itself is an <a> with text
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

            summary_el = article.select_one("p, div[class*='excerpt'], div[class*='desc']")
            summary = self.extract_text(summary_el, 280)

            items.append({
                "id": make_id(url or title),
                "title": title,
                "summary": summary or f"The Rundown AI: {title}",
                "url": url or "https://www.therundown.ai",
                "source": "The Rundown AI",
                "category": classify(title),
                "published": "",
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        return items[:20]
