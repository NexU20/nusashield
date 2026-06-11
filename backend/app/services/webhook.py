"""Webhook dispatch service — fire-and-forget alert delivery."""

from __future__ import annotations

import logging
from typing import Any

import httpx
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook import WebhookSubscription

logger = logging.getLogger(__name__)

_SEVERITY_ORDER = {"LOW": 0, "MEDIUM": 1, "HIGH": 2, "CRITICAL": 3}


async def dispatch_webhooks(
    threat_data: dict[str, Any],
    severity: str,
    db: AsyncSession,
) -> int:
    """Send threat alert to all matching webhook subscribers.

    Returns the number of successfully dispatched webhooks.
    """
    threat_level = _SEVERITY_ORDER.get(severity, 0)

    stmt = select(WebhookSubscription).where(WebhookSubscription.active == True)
    result = await db.execute(stmt)
    subs = list(result.scalars().all())

    if not subs:
        return 0

    dispatched = 0
    async with httpx.AsyncClient(timeout=10.0) as client:
        for sub in subs:
            sub_level = _SEVERITY_ORDER.get(sub.min_severity, 0)
            if sub_level > threat_level:
                continue

            payload = {
                "event": "threat.detected",
                **threat_data,
            }

            try:
                resp = await client.post(
                    sub.url,
                    json=payload,
                    headers={"X-SHARK-Fin-Key": sub.api_key},
                )
                if resp.status_code < 400:
                    dispatched += 1
                else:
                    logger.warning(
                        "Webhook %s returned %d", sub.url, resp.status_code
                    )
            except Exception as exc:
                logger.warning("Webhook dispatch failed for %s: %s", sub.url, exc)

    return dispatched
