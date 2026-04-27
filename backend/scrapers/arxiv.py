"""ArXiv AI papers scraper (cs.AI via RSS)."""

from .base import BaseScraper, make_id, classify, clean_text
from datetime import datetime, timezone
import re


class ArXivScraper(BaseScraper):
    name = "arxiv"
    URL = "https://rss.arxiv.org/rss/cs.AI"

    async def scrape(self) -> list[dict]:
        html = await self.fetch(self.URL)
        soup = self.soup(html)
        items = []

        for item in soup.select("item")[:25]:
            title_el = item.select_one("title")
            link_el = item.select_one("link")
            desc_el = item.select_one("description")

            if not title_el:
                continue

            raw_title = title_el.get_text(strip=True)
            # ArXiv: "arXiv:XXXX.XXXXX [cs.AI] Actual Title"
            title_match = re.search(r'\]\s*(.+)$', raw_title)
            title = title_match.group(1) if title_match else raw_title

            url = ""
            if link_el:
                url = link_el.get_text(strip=True)
            # Also check <link> as tag content vs next sibling
            if not url:
                link_next = item.find("link")
                if link_next and link_next.next_sibling:
                    url = str(link_next.next_sibling).strip()
            if not url:
                url = f"https://arxiv.org/abs/{make_id(raw_title)}"

            summary = self.extract_text(desc_el, 300)
            summary = re.sub(r'^(Abstract:|arXiv:.*?)\s*', '', summary).strip()

            # Extract arXiv ID for URL
            arxiv_id = re.search(r'(\d{4}\.\d{4,5})', raw_title)
            if arxiv_id and "arxiv.org" not in url:
                url = f"https://arxiv.org/abs/{arxiv_id.group(1)}"

            items.append({
                "id": make_id(url),
                "title": title,
                "summary": summary or f"New paper: {title}",
                "url": url,
                "source": "ArXiv",
                "category": classify(title),
                "published": "",
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        return items
