"""Statistics / dashboard summary endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.threat import Severity, SourceType, Threat, ThreatStatus

router = APIRouter(prefix="/stats", tags=["stats"])


class SummaryResponse(BaseModel):
    """Dashboard summary statistics."""

    total_threats: int
    by_severity: dict[str, int]
    by_source: dict[str, int]
    by_status: dict[str, int]
    total_records_exposed_estimate: int
    institutions_mentioned: list[str]


@router.get("/summary", response_model=SummaryResponse)
async def summary(session: AsyncSession = Depends(get_session)) -> dict:
    """Return aggregate threat stats for the dashboard."""
    total = await session.scalar(select(func.count(Threat.id))) or 0

    severity_counts: dict[str, int] = {}
    for sev in Severity:
        count = await session.scalar(
            select(func.count(Threat.id)).where(Threat.severity == sev)
        )
        severity_counts[sev.value] = count or 0

    source_counts: dict[str, int] = {}
    for src in SourceType:
        count = await session.scalar(
            select(func.count(Threat.id)).where(Threat.source_type == src)
        )
        source_counts[src.value] = count or 0

    status_counts: dict[str, int] = {}
    for st in ThreatStatus:
        count = await session.scalar(
            select(func.count(Threat.id)).where(Threat.status == st)
        )
        status_counts[st.value] = count or 0

    exposed_estimate = total * 5

    result = await session.execute(
        select(func.unnest(Threat.institution_tags))
        .where(Threat.institution_tags.isnot(None))
        .distinct()
    )
    institutions = [row[0] for row in result.all()]

    return {
        "total_threats": total,
        "by_severity": severity_counts,
        "by_source": source_counts,
        "by_status": status_counts,
        "total_records_exposed_estimate": exposed_estimate,
        "institutions_mentioned": sorted(institutions),
    }
