"""Unit tests for classifier/scorer.py — risk scoring engine."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.classifier.patterns import EntityType, IndonesianFinancialEntity
from app.classifier.scorer import RiskScorer, Severity


def _entity(
    etype: EntityType = EntityType.CREDIT_CARD,
    confidence: float = 0.9,
) -> IndonesianFinancialEntity:
    return IndonesianFinancialEntity(
        pattern_type=etype,
        matched_value="test",
        confidence=confidence,
        context_window="...test...",
        start=0,
        end=4,
    )


scorer = RiskScorer()


class TestRiskScorer:
    def test_empty_entities_returns_zero(self):
        result = scorer.score([])
        assert result.score == 0
        assert result.severity == Severity.LOW

    def test_single_credit_card(self):
        result = scorer.score([_entity(EntityType.CREDIT_CARD, 1.0)])
        assert result.score == 40
        assert result.severity == Severity.MEDIUM
        assert any("CREDIT_CARD" in f for f in result.factors)

    def test_multiple_entities_sum(self):
        entities = [
            _entity(EntityType.CREDIT_CARD, 1.0),
            _entity(EntityType.NIK, 1.0),
            _entity(EntityType.CREDENTIAL, 1.0),
        ]
        result = scorer.score(entities)
        # 40 + 25 + 35 = 100
        assert result.score == 100
        assert result.severity == Severity.CRITICAL

    def test_capped_at_100(self):
        entities = [
            _entity(EntityType.CREDIT_CARD, 1.0),
            _entity(EntityType.CREDIT_CARD, 1.0),
            _entity(EntityType.CREDIT_CARD, 1.0),
            _entity(EntityType.CREDIT_CARD, 1.0),
        ]
        result = scorer.score(entities)
        assert result.score == 100

    def test_confidence_scaling(self):
        full = scorer.score([_entity(EntityType.CREDIT_CARD, 1.0)])
        half = scorer.score([_entity(EntityType.CREDIT_CARD, 0.5)])
        assert full.score > half.score

    def test_volume_multiplier_high(self):
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            record_count=150,
        )
        # 40 * 1.5 = 60
        assert result.score == 60
        assert any("volume" in f for f in result.factors)

    def test_volume_multiplier_extreme(self):
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            record_count=1500,
        )
        # 40 * 2.0 = 80
        assert result.score == 80

    def test_freshness_critical(self):
        recent = datetime.now(timezone.utc) - timedelta(minutes=30)
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            posted_at=recent,
        )
        # 40 * 1.3 = 52
        assert result.score == 52
        assert any("freshness" in f for f in result.factors)

    def test_freshness_recent(self):
        recent = datetime.now(timezone.utc) - timedelta(hours=12)
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            posted_at=recent,
        )
        # 40 * 1.1 = 44
        assert result.score == 44

    def test_source_credibility_carding_forum(self):
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            source_label="carding_forum",
        )
        # 40 * 1.4 = 56
        assert result.score == 56

    def test_source_credibility_github(self):
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            source_label="github",
        )
        # 40 * 0.8 = 32
        assert result.score == 32

    def test_severity_mapping_low(self):
        result = scorer.score([_entity(EntityType.BANKING_KEYWORD, 1.0)])
        assert result.severity == Severity.LOW

    def test_severity_mapping_medium(self):
        result = scorer.score([_entity(EntityType.CREDIT_CARD, 1.0)])
        assert result.severity == Severity.MEDIUM

    def test_severity_mapping_high(self):
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            record_count=150,
        )
        assert result.score == 60
        assert result.severity == Severity.MEDIUM  # 31-60

    def test_severity_mapping_critical(self):
        result = scorer.score(
            [
                _entity(EntityType.CREDIT_CARD, 1.0),
                _entity(EntityType.NIK, 1.0),
                _entity(EntityType.CREDENTIAL, 1.0),
            ],
        )
        assert result.severity == Severity.CRITICAL

    def test_combined_multipliers(self):
        recent = datetime.now(timezone.utc) - timedelta(minutes=10)
        result = scorer.score(
            [_entity(EntityType.CREDIT_CARD, 1.0)],
            record_count=150,
            posted_at=recent,
            source_label="carding_forum",
        )
        # 40 * 1.5 * 1.3 * 1.4 = 109.2 → capped at 100
        assert result.score == 100
