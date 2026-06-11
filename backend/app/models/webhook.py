"""Webhook subscription model for alert delivery."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class WebhookSubscription(Base):
    """A registered webhook endpoint for threat alert delivery."""

    __tablename__ = "webhook_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    institution: Mapped[str] = mapped_column(String(255), nullable=False)
    min_severity: Mapped[str] = mapped_column(
        String(20), nullable=False, default="HIGH",
        comment="Minimum severity to trigger: LOW, MEDIUM, HIGH, CRITICAL",
    )
    api_key: Mapped[str] = mapped_column(
        String(255), nullable=False,
        comment="Subscriber's own key sent in X-SHARK-Fin-Key header",
    )
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
