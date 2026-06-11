"""Audit log model — immutable record of privileged actions.

Every write/export on a protected endpoint is recorded here so that status
changes and report exports are fully traceable (SEOJK 29/2022 & POJK 11/2022
expect auditability of incident handling). The actor is stored as a one-way
fingerprint of the API key, never the key itself.
"""

import hashlib
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def fingerprint(api_key: str | None) -> str:
    """Return a short, non-reversible fingerprint of an API key."""
    if not api_key:
        return "anonymous"
    return "key:" + hashlib.sha256(api_key.encode()).hexdigest()[:12]


class AuditLog(Base):
    """A single audited action on a protected endpoint."""

    __tablename__ = "audit_logs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    action: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True,
        comment="e.g. threat.status_update, report.export, webhook.register",
    )
    actor: Mapped[str] = mapped_column(
        String(80), nullable=False,
        comment="Fingerprint of the API key that performed the action",
    )
    target_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), nullable=True,
        comment="Affected resource id (e.g. threat id), if any",
    )
    detail: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True
    )
