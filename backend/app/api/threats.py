"""Threat feed API — full CRUD with filtering, pagination, and status workflow."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import require_api_key
from app.services.audit import record_audit
from pydantic import BaseModel, Field
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.threat import Severity, SourceType, Threat, ThreatStatus

router = APIRouter(prefix="/threats", tags=["threats"])


# ── Schemas ──


class ThreatResponse(BaseModel):
    """Full threat response schema."""

    id: uuid.UUID
    source_type: SourceType
    source_url: Optional[str] = None
    content_preview: Optional[str] = None
    detected_entities: dict
    content_hash: str
    risk_score: int
    severity: Severity
    status: ThreatStatus
    institution_tags: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ThreatListResponse(BaseModel):
    """Paginated threat list response."""

    items: List[ThreatResponse]
    total: int
    limit: int
    offset: int


class StatusUpdate(BaseModel):
    """Request body for status update."""

    status: ThreatStatus
    note: Optional[str] = None


class StatusUpdateResponse(BaseModel):
    """Response after status update."""

    id: uuid.UUID
    status: ThreatStatus
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Endpoints ──


@router.get("", response_model=ThreatListResponse)
async def list_threats(
    severity: Optional[Severity] = None,
    source_type: Optional[SourceType] = None,
    status: Optional[ThreatStatus] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    institution: Optional[str] = Query(
        default=None, description="Filter by institution tag (e.g. BRI)"
    ),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    session: AsyncSession = Depends(get_session),
) -> dict:
    """Return paginated threat feed with optional filters."""
    filters = []
    if severity:
        filters.append(Threat.severity == severity)
    if source_type:
        filters.append(Threat.source_type == source_type)
    if status:
        filters.append(Threat.status == status)
    if date_from:
        filters.append(Threat.created_at >= date_from)
    if date_to:
        filters.append(Threat.created_at <= date_to)
    if institution:
        filters.append(Threat.institution_tags.any(institution))

    where = and_(*filters) if filters else True

    total = await session.scalar(
        select(func.count(Threat.id)).where(where)
    )

    stmt = (
        select(Threat)
        .where(where)
        .order_by(Threat.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await session.execute(stmt)
    items = list(result.scalars().all())

    return {
        "items": items,
        "total": total or 0,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{threat_id}", response_model=ThreatResponse)
async def get_threat(
    threat_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
) -> Threat:
    """Return a single threat with full detail."""
    threat = await session.get(Threat, threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")
    return threat


@router.patch(
    "/{threat_id}/status",
    response_model=StatusUpdateResponse,
)
async def update_threat_status(
    threat_id: uuid.UUID,
    body: StatusUpdate,
    session: AsyncSession = Depends(get_session),
    api_key: str = Depends(require_api_key),
) -> Threat:
    """Update threat status (analyst workflow). Recorded in the audit log."""
    threat = await session.get(Threat, threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")

    previous = threat.status.value
    threat.status = body.status
    await session.commit()
    await session.refresh(threat)

    await record_audit(
        session,
        action="threat.status_update",
        api_key=api_key,
        target_id=threat_id,
        detail={"from": previous, "to": body.status.value, "note": body.note},
    )
    return threat
