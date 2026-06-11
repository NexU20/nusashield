"""Institution subscriber model — financial entities receiving threat feeds."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Institution(Base):
    """A subscribing financial institution or regulator."""

    __tablename__ = "institutions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    code: Mapped[str] = mapped_column(
        String(20), nullable=False, unique=True,
        comment="Short code, e.g. BRI, OJK, BSSN",
    )
    type: Mapped[str] = mapped_column(
        String(50), nullable=False,
        comment="bank | regulator | fintech",
    )
    webhook_url: Mapped[str | None] = mapped_column(String(2048))
    contact_email: Mapped[str | None] = mapped_column(String(255))
    keywords: Mapped[list[str] | None] = mapped_column(
        ARRAY(String(100)),
        comment="Custom keywords to trigger alerts for this institution",
    )
    config: Mapped[dict | None] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
