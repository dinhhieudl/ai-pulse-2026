"""Scrapers for AI news and benchmark sources (2026 updated)."""

from .rundown import RundownScraper
from .mit_tech import MITTechScraper
from .wired import WiredScraper
from .venturebeat import VentureBeatScraper
from .arxiv import ArXivScraper
from .lmsys import LMSYSScraper
from .vellum import VellumScraper
from .huggingface import HFLeaderboardScraper

__all__ = [
    "RundownScraper",
    "MITTechScraper",
    "WiredScraper",
    "VentureBeatScraper",
    "ArXivScraper",
    "LMSYSScraper",
    "VellumScraper",
    "HFLeaderboardScraper",
]
