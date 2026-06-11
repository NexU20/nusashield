"""Risk scoring engine — computes a 0-100 composite score for a threat.

Considers entity types, volume multiplier, freshness, and source
credibility to produce a severity-rated risk score.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional

from app.classifier.patterns import EntityType, IndonesianFinancialEntity


class Severity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class RiskScore:
    """Result of risk scoring."""
    score: int
    severity: Severity
    factors: List[str] = field(default_factory=list)


# ── Base weights per entity type ──

BASE_WEIGHTS: dict[EntityType, int] = {
    EntityType.CREDIT_CARD:     40,
    EntityType.NIK:             25,
    EntityType.CREDENTIAL:      35,
    EntityType.NPWP:            20,
    EntityType.ACCOUNT_NUMBER:  30,
    EntityType.CVV:             15,
    EntityType.BANK_NAME:       3,
    EntityType.BANKING_KEYWORD: 2,
}

# ── Source credibility multipliers ──

SOURCE_CREDIBILITY: dict[str, float] = {
    "carding_forum": 1.4,
    "telegram":      1.2,
    "paste":         1.0,
    "github":        0.8,
    "hibp":          1.1,
    "google_dork":   0.9,
}


def _volume_multiplier(record_count: int) -> tuple[float, str | None]:
    """Return (multiplier, factor_label) based on record volume."""
    if record_count >= 1000:
        return 2.0, f"volume_extreme ({record_count} records)"
    if record_count >= 100:
        return 1.5, f"volume_high ({record_count} records)"
    return 1.0, None


def _freshness_multiplier(
    posted_at: Optional[datetime],
) -> tuple[float, str | None]:
    """Return (multiplier, factor_label) based on how recent the post is."""
    if posted_at is None:
        return 1.0, None
    now = datetime.now(timezone.utc)
    if posted_at.tzinfo is None:
        posted_at = posted_at.replace(tzinfo=timezone.utc)
    age_hours = (now - posted_at).total_seconds() / 3600
    if age_hours < 1:
        return 1.3, "freshness_critical (<1h)"
    if age_hours < 24:
        return 1.1, "freshness_recent (<24h)"
    return 1.0, None


def _score_to_severity(score: int) -> Severity:
    if score >= 86:
        return Severity.CRITICAL
    if score >= 61:
        return Severity.HIGH
    if score >= 31:
        return Severity.MEDIUM
    return Severity.LOW


class RiskScorer:
    """Score a collection of detected entities into a 0-100 risk score."""

    def score(
        self,
        entities: List[IndonesianFinancialEntity],
        *,
        record_count: int = 1,
        posted_at: Optional[datetime] = None,
        source_label: str = "paste",
    ) -> RiskScore:
        """Compute composite risk score with multipliers.

        Args:
            entities: Entities detected by PatternScanner.
            record_count: Estimated number of records in the leak.
            posted_at: When the content was originally posted (UTC).
            source_label: Source category key for credibility multiplier.

        Returns:
            RiskScore with score clamped to [0, 100], severity, and factors.
        """
        if not entities:
            return RiskScore(score=0, severity=Severity.LOW, factors=["no_entities"])

        factors: List[str] = []

        # 1. Sum base weights, adjusted by per-entity confidence
        raw = 0.0
        entity_type_counts: dict[EntityType, int] = {}
        for ent in entities:
            base = BASE_WEIGHTS.get(ent.pattern_type, 1)
            raw += base * ent.confidence
            entity_type_counts[ent.pattern_type] = (
                entity_type_counts.get(ent.pattern_type, 0) + 1
            )

        for etype, count in entity_type_counts.items():
            factors.append(f"{etype.value}x{count}")

        # 2. Volume multiplier
        vol_mult, vol_factor = _volume_multiplier(record_count)
        if vol_factor:
            raw *= vol_mult
            factors.append(vol_factor)

        # 3. Freshness multiplier
        fresh_mult, fresh_factor = _freshness_multiplier(posted_at)
        if fresh_factor:
            raw *= fresh_mult
            factors.append(fresh_factor)

        # 4. Source credibility multiplier
        src_mult = SOURCE_CREDIBILITY.get(source_label, 1.0)
        if src_mult != 1.0:
            raw *= src_mult
            factors.append(f"source_{source_label} (x{src_mult})")

        # 5. Clamp to [0, 100]
        final = max(0, min(100, int(raw)))
        severity = _score_to_severity(final)

        return RiskScore(score=final, severity=severity, factors=factors)
