"""Bookmarks API — save and manage bookmarked articles."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_session
from db_models import BookmarkDB
from pydantic import BaseModel
from typing import Optional

router = APIRouter()


class BookmarkCreate(BaseModel):
    news_id: str
    title: str
    url: str
    source: str = ""
    category: str = "other"
    note: str = ""


class BookmarkUpdate(BaseModel):
    note: Optional[str] = None


@router.get(
    "/",
    summary="List bookmarks",
    description="Return all bookmarked articles, ordered by most recently saved.",
    responses={
        200: {
            "description": "List of bookmarks",
            "content": {
                "application/json": {
                    "example": {
                        "items": [
                            {
                                "id": "bm_demo1",
                                "news_id": "demo1",
                                "title": "OpenAI Announces GPT-5.5",
                                "url": "https://openai.com/index/gpt-5-5",
                                "source": "The Rundown AI",
                                "category": "llm",
                                "note": "",
                                "created_at": "2026-04-25 12:00:00",
                            }
                        ]
                    }
                }
            },
        }
    },
)
async def list_bookmarks(session: AsyncSession = Depends(get_session)):
    """Return all bookmarks."""
    result = await session.execute(select(BookmarkDB).order_by(BookmarkDB.created_at.desc()))
    bookmarks = result.scalars().all()
    return {
        "items": [
            {
                "id": b.id,
                "news_id": b.news_id,
                "title": b.title,
                "url": b.url,
                "source": b.source,
                "category": b.category,
                "note": b.note,
                "created_at": str(b.created_at),
            }
            for b in bookmarks
        ]
    }


@router.post(
    "/",
    summary="Add bookmark",
    description="Bookmark a news article. The bookmark ID is auto-generated as `bm_{news_id}`.",
    responses={
        200: {"description": "Bookmark created"},
        409: {"description": "Already bookmarked"},
    },
)
async def create_bookmark(data: BookmarkCreate, session: AsyncSession = Depends(get_session)):
    """Create a new bookmark."""
    bm_id = f"bm_{data.news_id}"
    exists = await session.execute(select(BookmarkDB).where(BookmarkDB.id == bm_id))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Already bookmarked")

    bm = BookmarkDB(
        id=bm_id,
        news_id=data.news_id,
        title=data.title,
        url=data.url,
        source=data.source,
        category=data.category,
        note=data.note,
    )
    session.add(bm)
    await session.commit()
    return {"status": "ok", "id": bm.id}


@router.delete(
    "/{bookmark_id}",
    summary="Remove bookmark",
    description="Delete a bookmark by its ID (format: `bm_{news_id}`).",
    responses={
        200: {"description": "Bookmark deleted"},
        404: {"description": "Bookmark not found"},
    },
)
async def delete_bookmark(bookmark_id: str, session: AsyncSession = Depends(get_session)):
    """Delete a bookmark."""
    result = await session.execute(select(BookmarkDB).where(BookmarkDB.id == bookmark_id))
    bm = result.scalar_one_or_none()
    if not bm:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    await session.delete(bm)
    await session.commit()
    return {"status": "ok"}
