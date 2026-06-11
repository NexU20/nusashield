"""Paste site scraper — monitors Pastebin public archive.

Polls the Pastebin public archive at a configurable interval, fetches
new pastes, and yields those containing Indonesian financial entities.
Respects rate limits (max 1 req/sec) and filters by relevance.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import AsyncIterator
from urllib.parse import urljoin

import httpx

from app.classifier.dedup import content_hash
from app.classifier.patterns import PatternScanner
from app.collectors.base import BaseCollector, RawIntel

logger = logging.getLogger(__name__)

PASTEBIN_SCRAPE_URL = "https://scrape.pastebin.com/api_scraping.php"
PASTEBIN_RAW_URL = "https://scrape.pastebin.com/api_scrape_item.php"

# Max 1 request per second to respect rate limits
REQUEST_DELAY = 1.0
# Max pastes to fetch per poll
MAX_PASTES_PER_POLL = 100

# Pre-filter keywords — skip full classification if none match
_PREFILTER_KEYWORDS = [
    "nik", "npwp", "bri", "bni", "bca", "mandiri", "bsi",
    "rekening", "kartu kredit", "credit card", "cvv", "dump",
    "combolist", "leak", "bocor", "data nasabah", "fullz",
    "carding", "pin", "otp", "saldo", "tabungan",
    "indonesia", "rupiah", "idr",
]


class PasteSiteCollector(BaseCollector):
    """Scrape Pastebin public archive for Indonesian financial data leaks."""

    def __init__(self) -> None:
        self._seen_hashes: set[str] = set()
        self._scanner = PatternScanner()

    async def collect(self) -> AsyncIterator[RawIntel]:
        """Fetch recent public pastes and yield those with financial data."""
        async with httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": "SHARK-Fin/0.1 (threat-intel)"},
        ) as client:
            paste_list = await self._fetch_paste_list(client)
            for paste_meta in paste_list:
                await asyncio.sleep(REQUEST_DELAY)
                async for intel in self._process_paste(client, paste_meta):
                    yield intel

    async def _fetch_paste_list(
        self, client: httpx.AsyncClient
    ) -> list[dict]:
        """Fetch the most recent paste metadata from Pastebin scrape API."""
        try:
            resp = await client.get(
                PASTEBIN_SCRAPE_URL,
                params={"limit": MAX_PASTES_PER_POLL},
            )
            resp.raise_for_status()
            data = resp.json()
            if isinstance(data, list):
                return data
            logger.warning("Unexpected paste list format: %s", type(data))
            return []
        except httpx.HTTPStatusError as e:
            logger.warning("Pastebin API error: %s", e.response.status_code)
            return []
        except Exception:
            logger.exception("Failed to fetch paste list")
            return []

    async def _process_paste(
        self, client: httpx.AsyncClient, meta: dict
    ) -> AsyncIterator[RawIntel]:
        """Fetch a single paste and yield it if it contains financial data."""
        paste_key = meta.get("key", "")
        if not paste_key:
            return

        try:
            resp = await client.get(
                PASTEBIN_RAW_URL,
                params={"i": paste_key},
            )
            resp.raise_for_status()
            content = resp.text
        except Exception:
            logger.debug("Failed to fetch paste %s", paste_key)
            return

        if not content:
            return

        # Dedup
        h = content_hash(content)
        if h in self._seen_hashes:
            return
        self._seen_hashes.add(h)

        # Pre-filter: quick keyword check before full scan
        content_lower = content.lower()
        if not any(kw in content_lower for kw in _PREFILTER_KEYWORDS):
            return

        # Full classification
        entities = self._scanner.scan(content)
        if not entities:
            return

        # Parse timestamp
        paste_date = meta.get("date")
        posted_at = (
            datetime.fromtimestamp(int(paste_date), tz=timezone.utc)
            if paste_date
            else datetime.now(timezone.utc)
        )

        yield RawIntel(
            source_url=f"https://pastebin.com/{paste_key}",
            content=content,
            source_type="PASTE",
            posted_at=posted_at,
            metadata={
                "paste_key": paste_key,
                "title": meta.get("title", ""),
                "size": meta.get("size", 0),
                "syntax": meta.get("syntax", ""),
                "user": meta.get("user", "anonymous"),
                "entity_count": len(entities),
            },
        )
