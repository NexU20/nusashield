"""Environment-based application settings using pydantic-settings."""

from typing import List

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration loaded from environment variables / .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        # Treat empty env vars (e.g. `TELEGRAM_CHANNELS=` in .env.example) as unset
        # so optional/complex fields fall back to their defaults instead of failing
        # to JSON-parse an empty string.
        env_ignore_empty=True,
    )

    # ── Database ──
    DATABASE_URL: str = "postgresql+asyncpg://siakfin:siakfin@postgres:5432/siakfin"
    DB_ECHO: bool = False
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    # ── Redis ──
    REDIS_URL: str = "redis://redis:6379/0"

    # ── Telegram ──
    TELEGRAM_API_ID: int | str = 0

    @field_validator("TELEGRAM_API_ID", mode="before")
    @classmethod
    def parse_api_id(cls, v: object) -> int:
        if isinstance(v, str) and not v.strip():
            return 0
        return int(v)  # type: ignore[arg-type]
    TELEGRAM_API_HASH: str = ""
    TELEGRAM_CHANNELS: List[str] = []

    @field_validator("TELEGRAM_CHANNELS", mode="before")
    @classmethod
    def parse_channels(cls, v: object) -> List[str]:
        if isinstance(v, str):
            if not v.strip():
                return []
            return [ch.strip() for ch in v.split(",") if ch.strip()]
        return v  # type: ignore[return-value]

    # ── GitHub ──
    GITHUB_TOKEN: str = ""
    GITHUB_POLL_INTERVAL: int = 1800  # 30 minutes

    # ── Google Dork (Custom Search) ──
    GOOGLE_CSE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""
    GOOGLE_DORK_INTERVAL: int = 3600  # 1 hour

    # ── HaveIBeenPwned ──
    HIBP_API_KEY: str = ""

    # ── Auth ──
    API_KEYS: str = "sharkfin-demo-key-2026"

    # ── Data Protection (UU PDP No. 27/2022) ──
    # When False (recommended for production), the original collected content is
    # never persisted — only the masked content_preview and the SHA-256 hash are
    # stored. The full text is still used in-memory for classification and dedup.
    STORE_RAW_CONTENT: bool = False

    # ── App ──
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    CORS_ORIGINS: List[str] = ["http://localhost:5173"]


settings = Settings()
