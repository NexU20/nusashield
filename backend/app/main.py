"""FastAPI application entry point for SHARK-Fin."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import alerts, audit, reports, stats, threats
from app.models import audit as audit_model  # noqa: F401 — register table
from app.models import webhook  # noqa: F401 — register table
from app import cache
from app.config import settings
from app.database import init_db
from app.scheduler import start_scheduler, stop_scheduler


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Startup / shutdown lifecycle hook."""
    await init_db()
    start_scheduler()
    yield
    stop_scheduler()
    await cache.close()


app = FastAPI(
    title="SHARK-Fin",
    description="Source Hunting Alert and Risk Knowledge for Financial Intelligence",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(threats.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(alerts.router, prefix="/api/v1")
app.include_router(stats.router, prefix="/api/v1")
app.include_router(audit.router, prefix="/api/v1")


@app.get("/health")
async def health() -> dict:
    """Liveness/readiness probe reporting per-dependency status."""
    from sqlalchemy import text

    from app.database import async_session

    db_ok = False
    try:
        async with async_session() as session:
            await session.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    redis_ok = await cache.ping()

    return {
        "status": "ok" if db_ok else "degraded",
        "service": "shark-fin",
        "dependencies": {
            "database": "ok" if db_ok else "down",
            "redis": "ok" if redis_ok else "down",
        },
    }
