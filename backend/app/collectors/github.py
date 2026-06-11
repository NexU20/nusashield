"""GitHub public code search collector for Indonesian financial data leaks."""

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

QUERIES = [
    '"NIK" "rekening" "BRI" OR "BCA" OR "Mandiri"',
    '"npwp" "password" filetype:txt',
    '"kartu kredit" "cvv" indonesia',
    '"combo list" "bank" indonesia',
    '"data nasabah" "bocor"',
    '"fullz" "indonesia"',
]

MAX_CONTENT_LENGTH = 2000
SEARCH_PER_PAGE = 5
DELAY_BETWEEN_QUERIES = 2


class GitHubCollector(BaseCollector):
    """Search GitHub code search API for Indonesian financial data leaks."""

    def __init__(self) -> None:
        self._seen: set[str] = set()

    async def collect(self) -> AsyncIterator[RawIntel]:
        token = settings.GITHUB_TOKEN
        if not token:
            logger.warning("GITHUB_TOKEN not set — skipping GitHub collector")
            return

        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
        }
        backoff = 2

        async with httpx.AsyncClient(timeout=15.0, headers=headers) as client:
            for query in QUERIES:
                try:
                    resp = await client.get(
                        "https://api.github.com/search/code",
                        params={"q": query, "per_page": SEARCH_PER_PAGE},
                    )

                    if resp.status_code in (403, 429):
                        logger.warning(
                            "GitHub rate limit hit (HTTP %d), backing off %ds",
                            resp.status_code, backoff,
                        )
                        await asyncio.sleep(backoff)
                        backoff = min(backoff * 2, 120)
                        continue

                    if resp.status_code != 200:
                        logger.warning("GitHub search returned %d", resp.status_code)
                        continue

                    backoff = 2  # reset on success
                    data = resp.json()

                    for item in data.get("items", []):
                        repo = item.get("repository", {})
                        full_name = repo.get("full_name", "")
                        path = item.get("path", "")
                        sha = item.get("sha", "")
                        html_url = item.get("html_url", "")

                        # Dedup
                        dedup_key = hashlib.sha256(
                            f"{full_name}:{path}:{sha}".encode()
                        ).hexdigest()
                        if dedup_key in self._seen:
                            continue
                        self._seen.add(dedup_key)

                        # Fetch raw content
                        default_branch = repo.get("default_branch", "main")
                        raw_url = (
                            f"https://raw.githubusercontent.com/"
                            f"{full_name}/{default_branch}/{path}"
                        )
                        try:
                            raw_resp = await client.get(raw_url)
                            if raw_resp.status_code != 200:
                                continue
                            content = raw_resp.text[:MAX_CONTENT_LENGTH]
                        except httpx.HTTPError:
                            continue

                        yield RawIntel(
                            source_url=html_url,
                            content=content,
                            source_type="GITHUB",
                            posted_at=datetime.now(timezone.utc),
                            metadata={
                                "repo": full_name,
                                "path": path,
                                "sha": sha,
                                "query": query,
                            },
                        )

                except httpx.HTTPError as exc:
                    logger.warning("GitHub request error: %s", exc)

                await asyncio.sleep(DELAY_BETWEEN_QUERIES)
