"""SQLAlchemy ORM models for persistent storage."""

from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from db import Base


class NewsItemDB(Base):
    __tablename__ = "news_items"

    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    summary = Column(Text, default="")
    url = Column(String, nullable=False)
    source = Column(String, nullable=False)
    category = Column(String, default="other")
    sentiment = Column(String, default="neutral")  # positive/negative/neutral/launch/update/funding/research
    published = Column(String, default="")
    scraped_at = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())


class LeaderboardEntryDB(Base):
    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    rank = Column(Integer, nullable=False)
    model = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    mmlu_score = Column(Float, nullable=True)
    elo_score = Column(Float, nullable=True)
    arena_elo = Column(Float, nullable=True)
    pricing_input = Column(String, nullable=True)
    pricing_output = Column(String, nullable=True)
    speed_tps = Column(Float, nullable=True)
    source = Column(String, default="")
    released = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    scraped_at = Column(DateTime, server_default=func.now())
    snapshot_date = Column(String, default="")  # YYYY-MM-DD for trend tracking


class BookmarkDB(Base):
    __tablename__ = "bookmarks"

    id = Column(String, primary_key=True)
    news_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    source = Column(String, default="")
    category = Column(String, default="other")
    note = Column(Text, default="")
    created_at = Column(DateTime, server_default=func.now())


class UserLinkDB(Base):
    __tablename__ = "user_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    title = Column(String, default="")
    summary = Column(Text, default="")
    source = Column(String, default="User Submitted")
    category = Column(String, default="other")
    sentiment = Column(String, default="neutral")
    status = Column(String, default="pending")  # pending/approved/rejected
    created_at = Column(DateTime, server_default=func.now())


class ModelSnapshotDB(Base):
    """Daily snapshots for trend charts."""
    __tablename__ = "model_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=False)  # YYYY-MM-DD
    model = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    mmlu_score = Column(Float, nullable=True)
    elo_score = Column(Float, nullable=True)
    pricing_input = Column(String, nullable=True)
    pricing_output = Column(String, nullable=True)
    speed_tps = Column(Float, nullable=True)
    source = Column(String, default="")
    created_at = Column(DateTime, server_default=func.now())
