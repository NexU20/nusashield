"""SHA-256 based deduplication for incoming raw content."""

import hashlib


def content_hash(text: str) -> str:
    """Return the hex SHA-256 digest of *text* (UTF-8 encoded)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
