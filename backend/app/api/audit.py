"""Audit-trail read endpoint (auth-protected)."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.middleware.auth import require_api_key
from app.models.audit import AuditLog

router = APIRouter(prefix="/audit", tags=["audit"])


class AuditEntry(BaseModel):
    id: uuid.UUID
    action: str
    actor: str
    target_id: Optional[uuid.UUID] = None
    detail: dict
    created_at: datetime

    model_config = {"from_attributes": True}


@router.get(
    "",
    response_model=List[AuditEntry],
    dependencies=[Depends(require_api_key)],
)
async def list_audit(
    action: Optional[str] = None,
    limit: int = Query(default=100, ge=1, le=500),
    session: AsyncSession = Depends(get_session),
) -> list:
    """Return the most recent audit entries (newest first)."""
    stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
    if action:
        stmt = stmt.where(AuditLog.action == action)
    result = await session.execute(stmt)
    return list(result.scalars().all())
