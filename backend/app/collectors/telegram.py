"""Telegram public channel monitor using Telethon.

Monitors a configurable list of public Telegram channels for messages
containing Indonesian financial data. Uses exponential backoff on rate
limits and deduplicates via SHA-256 content hashing.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime, timezone
from typing import AsyncIterator

from telethon import TelegramClient
from telethon.errors import FloodWaitError
from telethon.tl.types import Message

from app.classifier.dedup import content_hash
from app.collectors.base import BaseCollector, RawIntel
from app.config import settings

logger = logging.getLogger(__name__)

# Default Indonesian financial threat channels (plausible dummies, configurable)
DEFAULT_CHANNELS = [
    "indo_leak_alert",
    "id_data_breach",
    "findata_id",
    "cc_dump_indo",
    "bank_leak_idn",
]

# Maximum number of messages to fetch per channel per poll
MAX_MESSAGES_PER_POLL = 100

# Exponential backoff settings
BASE_BACKOFF = 2
MAX_BACKOFF = 300  # 5 minutes


class TelegramCollector(BaseCollector):
    """Monitor configured public Telegram channels for financial data leaks."""

    def __init__(self) -> None:
        self._client: TelegramClient | None = None
        self._seen_hashes: set[str] = set()
        channels = settings.TELEGRAM_CHANNELS
        self._channels: list[str] = channels if channels else DEFAULT_CHANNELS

    async def _get_client(self) -> TelegramClient:
        """Lazily initialise and connect the Telethon client."""
        if self._client is None:
            api_id = settings.TELEGRAM_API_ID
            api_hash = settings.TELEGRAM_API_HASH
            if not api_id or not api_hash:
                raise RuntimeError(
                    "TELEGRAM_API_ID and TELEGRAM_API_HASH must be set"
                )
            self._client = TelegramClient(
                "shark_fin_bot", api_id, api_hash
            )
            await self._client.start()
            logger.info("Telethon client connected")
        return self._client

    async def collect(self) -> AsyncIterator[RawIntel]:
        """Poll all configured channels and yield new messages."""
        try:
            client = await self._get_client()
        except RuntimeError as exc:
            logger.warning("Telegram collector skipped: %s", exc)
            return

        for channel_name in self._channels:
            backoff = BASE_BACKOFF
            try:
                async for intel in self._poll_channel(client, channel_name):
                    yield intel
            except FloodWaitError as e:
                wait_seconds = min(e.seconds, MAX_BACKOFF)
                logger.warning(
                    "Telegram rate limited on %s, waiting %ds",
                    channel_name,
                    wait_seconds,
                )
                await asyncio.sleep(wait_seconds)
                backoff = min(backoff * 2, MAX_BACKOFF)
            except Exception:
                logger.exception(
                    "Error polling Telegram channel %s", channel_name
                )

    async def _poll_channel(
        self, client: TelegramClient, channel: str
    ) -> AsyncIterator[RawIntel]:
        """Fetch recent messages from a single channel."""
        try:
            entity = await client.get_entity(channel)
        except Exception:
            logger.warning("Cannot resolve channel: %s", channel)
            return

        messages: list[Message] = await client.get_messages(
            entity, limit=MAX_MESSAGES_PER_POLL
        )

        for msg in messages:
            if not msg.text:
                continue

            # Deduplicate
            h = content_hash(msg.text)
            if h in self._seen_hashes:
                continue
            self._seen_hashes.add(h)

            posted = msg.date
            if posted and posted.tzinfo is None:
                posted = posted.replace(tzinfo=timezone.utc)

            yield RawIntel(
                source_url=f"https://t.me/{channel}/{msg.id}",
                content=msg.text,
                source_type="TELEGRAM",
                posted_at=posted or datetime.now(timezone.utc),
                metadata={
                    "channel": channel,
                    "message_id": msg.id,
                    "sender_type": (
                        "bot" if getattr(msg.sender, "bot", False)
                        else "user"
                    ),
                    "views": getattr(msg, "views", None),
                    "forwards": getattr(msg, "forwards", None),
                },
            )

    async def disconnect(self) -> None:
        """Disconnect the Telethon client."""
        if self._client:
            await self._client.disconnect()
            self._client = None
