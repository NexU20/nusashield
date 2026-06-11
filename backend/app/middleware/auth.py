"""Simple API key authentication for write endpoints."""

from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

from app.config import settings

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def require_api_key(
    api_key: str = Security(api_key_header),
) -> str:
    """Validate X-API-Key header against configured keys."""
    valid_keys = settings.API_KEYS
    if not api_key or api_key not in valid_keys.split(","):
        raise HTTPException(
            status_code=401,
            detail="API key tidak valid. Sertakan header X-API-Key.",
        )
    return api_key
