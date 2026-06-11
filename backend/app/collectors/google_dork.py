"""Google Custom Search (dork) collector for Indonesian financial data leaks."""

from __future__ import annotations

import asyncio
import hashlib
import logging
from datetime import datetime, timezone
from typing import AsyncIterator

import httpx

from app.collectors.base import BaseCollector, RawIntel
from app.config import settings

logger = logging.getLogger(__name__)

DORKS = [
    '"NIK" "NPWP" "rekening" filetype:txt',
    '"nomor kartu" "cvv" "expired" indonesia',
    '"data nasabah" "bocor" filetype:csv',
    '"fullz" "indonesia" "bank" site:pastebin.com',
    '"combo list" "BRI" OR "BCA" OR "Mandiri"',
]

SEARCH_NUM = 5


class GoogleDorkCollector(BaseCollector):
    """Search Google Custom Search API for Indonesian financial data leaks."""

    def __init__(self) -> None:
        self._seen: set[str] = set()

    async def collect(self) -> AsyncIterator[RawIntel]:
        api_key = settings.GOOGLE_CSE_API_KEY
        cse_id = settings.GOOGLE_CSE_ID
        if not api_key or not cse_id:
            logger.warning(
                "GOOGLE_CSE_API_KEY or GOOGLE_CSE_ID not set — skipping Google Dork collector"
            )
            return

        async with httpx.AsyncClient(timeout=15.0) as client:
            for dork in DORKS:
                try:
                    resp = await client.get(
                        "https://www.googleapis.com/customsearch/v1",
                        params={
                            "key": api_key,
                            "cx": cse_id,
                            "q": dork,
                            "num": SEARCH_NUM,
                        },
                    )

                    if resp.status_code != 200:
                        logger.warning(
                            "Google CSE returned %d for dork: %s",
                            resp.status_code, dork,
                        )
                        continue

                    data = resp.json()

                    for item in data.get("items", []):
                        link = item.get("link", "")
                        snippet = item.get("snippet", "")
                        title = item.get("title", "")

                        if not snippet:
                            continue

                        dedup_key = hashlib.sha256(link.encode()).hexdigest()
                        if dedup_key in self._seen:
                            continue
                        self._seen.add(dedup_key)

                        content = f"{title}\n{snippet}"

                        yield RawIntel(
                            source_url=link,
                            content=content,
                            source_type="GOOGLE_DORK",
                            posted_at=datetime.now(timezone.utc),
                            metadata={
                                "title": title,
                                "snippet": snippet,
                                "dork_query": dork,
                            },
                        )

                except httpx.HTTPError as exc:
                    logger.warning("Google CSE request error: %s", exc)

                await asyncio.sleep(1)
