"""Abstract base class for all intelligence collectors."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import AsyncIterator

logger = logging.getLogger(__name__)


@dataclass
class RawIntel:
    """A single piece of raw intelligence from a source."""

    source_url: str
    content: str
    source_type: str = ""
    posted_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: dict = field(default_factory=dict)


class BaseCollector(ABC):
    """Every collector must implement ``collect``."""

    @abstractmethod
    async def collect(self) -> AsyncIterator[RawIntel]:
        """Yield raw intelligence items from the source."""
        ...  # pragma: no cover
