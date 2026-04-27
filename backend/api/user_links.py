"""User Links API — submit and manage user-contributed articles."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db_models import UserLinkDB, NewsItemDB
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone
from scrapers.base import make_id, classify
import httpx
import re

router = APIRouter()


class UserLinkCreate(BaseModel):
    url: str
    title: Optional[str] = None
    summary: Optional[str] = None
    category: Optional[str] = None


@router.get(
    "/",
    summary="List user-submitted links",
    description="Return user-submitted article links, filtered by status.",
    responses={
        200: {
            "description": "List of user-submitted links",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": 1,
                                "url": "https://example.com/ai-article",
                                "title": "New AI Breakthrough",
                                "summary": "Researchers achieved...",
                                "source": "User Submitted",
                                "category": "llm",
                                "sentiment": "neutral",
                                "status": "approved",
                                "created_at": "2026-04-25 12:00:00",
                            }
                        ]
                    }
                }
            },
        }
    },
)
async def list_user_links(
    status: str = Query("approved", description="Filter by status: pending, approved, rejected"),
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(
        select(UserLinkDB)
        .where(UserLinkDB.status == status)
        .order_by(UserLinkDB.created_at.desc())
    )
    links = result.scalars().all()
    return {
        "items": [
            {
                "id": l.id,
                "url": l.url,
                "title": l.title,
                "summary": l.summary,
                "source": l.source,
                "category": l.category,
                "sentiment": l.sentiment,
                "status": l.status,
                "created_at": str(l.created_at),
            }
            for l in links
        ]
    }


@router.post(
    "/",
    summary="Submit article link",
    description="Submit a URL to the news feed. If title/summary are not provided, "
                "they are auto-fetched from the page's `<title>` and `<meta description>` tags. "
                "The article is immediately added to the news feed with status=approved.",
    responses={
        200: {
            "description": "Link submitted and added to news feed",
            "content": {
                "application/json": {
                    "example": {"status": "ok", "id": 1, "title": "Auto-fetched title"}
                }
            },
        }
    },
)
async def submit_link(data: UserLinkCreate, session: AsyncSession = Depends(get_session)):
    """Submit a URL. Auto-fetches metadata if title/summary not provided."""
    title = data.title or ""
    summary = data.summary or ""

    # Auto-fetch metadata if not provided
    if not title:
        try:
            async with httpx.AsyncClient(
                headers={"User-Agent": "AI-Pulse-2026/1.0"},
                follow_redirects=True, timeout=15,
            ) as client:
                resp = await client.get(data.url)
                resp.raise_for_status()
                html = resp.text

                title_match = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
                if title_match:
                    title = title_match.group(1).strip()[:200]

                desc_match = re.search(
                    r'<meta[^>]*name=["\']description["\'][^>]*content=["\'](.*?)["\']',
                    html, re.IGNORECASE,
                )
                if desc_match:
                    summary = desc_match.group(1).strip()[:300]

                if not title:
                    og_match = re.search(
                        r'<meta[^>]*property=["\']og:title["\'][^>]*content=["\'](.*?)["\']',
                        html, re.IGNORECASE,
                    )
                    if og_match:
                        title = og_match.group(1).strip()[:200]
        except Exception:
            title = data.url

    category = data.category or classify(title)
    link = UserLinkDB(
        url=data.url,
        title=title,
        summary=summary,
        source="User Submitted",
        category=category,
        sentiment="neutral",
        status="approved",
    )
    session.add(link)

    news_item = NewsItemDB(
        id=make_id(data.url),
        title=title,
        summary=summary or f"User submitted: {title}",
        url=data.url,
        source="User Submitted",
        category=category,
        sentiment="neutral",
        published=datetime.now(timezone.utc).isoformat(),
    )
    session.add(news_item)
    await session.commit()

    return {"status": "ok", "id": link.id, "title": title}
