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


@router.get("/")
async def list_bookmarks(session: AsyncSession = Depends(get_session)):
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


@router.post("/")
async def create_bookmark(data: BookmarkCreate, session: AsyncSession = Depends(get_session)):
    bm = BookmarkDB(
        id=f"bm_{data.news_id}",
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


@router.delete("/{bookmark_id}")
async def delete_bookmark(bookmark_id: str, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(BookmarkDB).where(BookmarkDB.id == bookmark_id))
    bm = result.scalar_one_or_none()
    if not bm:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    await session.delete(bm)
    await session.commit()
    return {"status": "ok"}
