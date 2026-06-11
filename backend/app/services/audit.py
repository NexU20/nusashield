"""Helper for writing audit-log entries."""

from __future__ import annotations

import logging
import uuid
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog, fingerprint

logger = logging.getLogger(__name__)


async def record_audit(
    session: AsyncSession,
    *,
    action: str,
    api_key: Optional[str],
    target_id: Optional[uuid.UUID] = None,
    detail: Optional[dict[str, Any]] = None,
) -> None:
    """Persist an audit entry. Best-effort: never breaks the calling request."""
    try:
        session.add(AuditLog(
            action=action,
            actor=fingerprint(api_key),
            target_id=target_id,
            detail=detail or {},
        ))
        await session.commit()
    except Exception:
        logger.exception("Failed to write audit log for action=%s", action)
