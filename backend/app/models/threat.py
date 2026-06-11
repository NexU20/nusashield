"""Core threat-intelligence ORM models: Threat, Source, Alert."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

import re


def mask_sensitive(text: str) -> str:
    """Mask PII/financial data in text for safe storage and display."""
    # Credit card: keep first 4 + last 4
    text = re.sub(r'\b(\d{4})\d{8,12}(\d{4})\b', r'\1 •••• •••• \2', text)
    # NIK: keep first 6 + last 2
    text = re.sub(r'\b(\d{6})\d{8}(\d{2})\b', r'\1••••••••\2', text)
    # Passwords
    text = re.sub(
        r'(password|passwd|pwd|pin|secret)\s*[:=]\s*\S+',
        r'\1: [TERSEMBUNYI]', text, flags=re.IGNORECASE
    )
    # Truncate
    return text[:200] + ('...' if len(text) > 200 else '')


# ── Enums ──


class SourceType(str, enum.Enum):
    """Origin of the collected intelligence."""
    TELEGRAM = "TELEGRAM"
    PASTE = "PASTE"
    GITHUB = "GITHUB"
    HIBP = "HIBP"
    GOOGLE_DORK = "GOOGLE_DORK"


class Severity(str, enum.Enum):
    """Risk severity tier."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ThreatStatus(str, enum.Enum):
    """Lifecycle status of a threat entry."""
    NEW = "NEW"
    VERIFIED = "VERIFIED"
    MITIGATED = "MITIGATED"
    FALSE_POSITIVE = "FALSE_POSITIVE"


# ── Models ──


class Source(Base):
    """A monitored intelligence source (channel, repo, paste site, etc.)."""

    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    source_type: Mapped[SourceType] = mapped_column(
        Enum(SourceType, name="source_type_enum"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str | None] = mapped_column(String(2048))
    enabled: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    threats: Mapped[list["Threat"]] = relationship(back_populates="source")


class Threat(Base):
    """A single detected threat / data-leak event."""

    __tablename__ = "threats"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Source linkage
    source_type: Mapped[SourceType] = mapped_column(
        Enum(SourceType, name="source_type_enum", create_type=False),
        nullable=False,
    )
    source_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("sources.id")
    )
    source_url: Mapped[str | None] = mapped_column(String(2048))

    # Payload
    raw_content: Mapped[str] = mapped_column(Text, nullable=False)
    content_preview: Mapped[str | None] = mapped_column(
        Text, nullable=True,
        comment="First 200 chars of content with PII masked",
    )
    detected_entities: Mapped[dict] = mapped_column(JSONB, default=dict)
    content_hash: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True,
        comment="SHA-256 of raw_content for dedup",
    )

    # Scoring & classification
    risk_score: Mapped[int] = mapped_column(
        Integer, nullable=False, default=0,
        comment="0-100 composite risk score",
    )
    severity: Mapped[Severity] = mapped_column(
        Enum(Severity, name="severity_enum"), nullable=False, default=Severity.LOW
    )
    status: Mapped[ThreatStatus] = mapped_column(
        Enum(ThreatStatus, name="threat_status_enum"),
        nullable=False,
        default=ThreatStatus.NEW,
    )

    # Tagging
    institution_tags: Mapped[list[str] | None] = mapped_column(
        ARRAY(String(100)),
        comment="Financial institutions referenced (e.g. BRI, BCA)",
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    source: Mapped[Source | None] = relationship(back_populates="threats")
    alerts: Mapped[list["Alert"]] = relationship(back_populates="threat")


class Alert(Base):
    """Webhook/notification record dispatched for a threat."""

    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    threat_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("threats.id"), nullable=False
    )
    channel: Mapped[str] = mapped_column(
        String(50), nullable=False, comment="webhook | email | sms"
    )
    destination: Mapped[str] = mapped_column(String(2048), nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, default=dict)
    sent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    threat: Mapped[Threat] = relationship(back_populates="alerts")
