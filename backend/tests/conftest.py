"""Shared fixtures for integration tests."""

from __future__ import annotations

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.classifier.dedup import content_hash
from app.database import Base, get_session
from app.models.threat import Severity, SourceType, Threat, ThreatStatus
# Import side-tables so Base.metadata.create_all builds them for tests.
from app.models import audit as _audit  # noqa: F401
from app.models import webhook as _webhook  # noqa: F401

import os

# Tables cleaned between tests, child-before-parent for FK safety.
_CLEAN_TABLES = ["alerts", "audit_logs", "webhook_subscriptions", "threats"]

TEST_DB_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://siakfin:siakfin@postgres:5432/siakfin",
)


@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """Create a fresh async engine per test to avoid event-loop conflicts."""
    engine = create_async_engine(TEST_DB_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Clean before test
    async with engine.begin() as conn:
        for table in _CLEAN_TABLES:
            await conn.execute(text(f"DELETE FROM {table}"))
    yield engine
    # Clean after test
    async with engine.begin() as conn:
        for table in _CLEAN_TABLES:
            await conn.execute(text(f"DELETE FROM {table}"))
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(db_engine):
    """Provide a test DB session."""
    factory = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with factory() as session:
        yield session


@pytest_asyncio.fixture
async def client(db_engine):
    """HTTPX async client with overridden DB session dependency."""
    from app.main import app

    factory = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )

    async def _override() -> AsyncSession:  # type: ignore[misc]
        async with factory() as session:
            yield session

    app.dependency_overrides[get_session] = _override
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_threat(db_engine) -> Threat:
    """Insert a sample threat directly via ORM."""
    factory = async_sessionmaker(
        db_engine, class_=AsyncSession, expire_on_commit=False
    )
    raw = "Test leak: BRI credit card 4052900000000000"
    async with factory() as session:
        threat = Threat(
            source_type=SourceType.TELEGRAM,
            source_url="https://t.me/test/1",
            raw_content=raw,
            detected_entities={
                "entities": [
                    {
                        "type": "CREDIT_CARD",
                        "value": "405290******0000",
                        "confidence": 0.95,
                    }
                ],
                "count": 1,
            },
            content_hash=content_hash(raw),
            risk_score=65,
            severity=Severity.HIGH,
            status=ThreatStatus.NEW,
            institution_tags=["BRI"],
        )
        session.add(threat)
        await session.commit()
        await session.refresh(threat)
        return threat
