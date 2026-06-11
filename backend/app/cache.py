"""Redis-backed cache for the collection hot path.

Redis is an optional accelerator, never a source of truth: PostgreSQL remains
authoritative for dedup. If Redis is unavailable every operation degrades
gracefully to a no-op so the pipeline keeps working. This is what lets the
platform scale collection horizontally — workers share the recent-hash set
instead of each hammering the database.
"""

from __future__ import annotations

import logging
from typing import Optional

from app.config import settings

logger = logging.getLogger(__name__)

_SEEN_KEY = "sharkfin:seen_hashes"
_SEEN_TTL = 60 * 60 * 24 * 7  # 7 days

try:
    import redis.asyncio as aioredis
except Exception:  # pragma: no cover - redis lib always present in prod
    aioredis = None  # type: ignore[assignment]

_client = None
_unavailable = False


def _get_client():
    """Lazily create a single shared async Redis client."""
    global _client, _unavailable
    if _unavailable or aioredis is None:
        return None
    if _client is None:
        try:
            _client = aioredis.from_url(
                settings.REDIS_URL, decode_responses=True,
                socket_connect_timeout=2, socket_timeout=2,
            )
        except Exception:
            _unavailable = True
            return None
    return _client


async def ping() -> bool:
    """Return True if Redis is reachable."""
    client = _get_client()
    if client is None:
        return False
    try:
        return bool(await client.ping())
    except Exception:
        return False


async def seen_recently(content_hash: str) -> bool:
    """Best-effort check whether a hash was processed recently."""
    client = _get_client()
    if client is None:
        return False
    try:
        return bool(await client.sismember(_SEEN_KEY, content_hash))
    except Exception:
        return False


async def remember(content_hash: str) -> None:
    """Record a processed hash in the shared recent-hash set."""
    client = _get_client()
    if client is None:
        return
    try:
        await client.sadd(_SEEN_KEY, content_hash)
        await client.expire(_SEEN_KEY, _SEEN_TTL)
    except Exception:
        pass


async def close() -> None:
    """Close the shared client (used on shutdown)."""
    global _client
    if _client is not None:
        try:
            await _client.aclose()
        except Exception:
            pass
        _client = None
