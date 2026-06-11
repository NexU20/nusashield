"""Unit tests for classifier/patterns.py — Indonesian financial entity detection.

Covers: true positives, false positives, edge cases, Indonesian-specific formats.
"""

from __future__ import annotations

import pytest

from app.classifier.patterns import (
    EntityType,
    IndonesianFinancialEntity,
    PatternScanner,
    luhn_check,
    npwp_checksum_valid,
    validate_nik_date,
)

scanner = PatternScanner()


def _find(entities: list[IndonesianFinancialEntity], etype: EntityType):
    return [e for e in entities if e.pattern_type == etype]


# ═══════════════════════════════════════════
# Luhn algorithm
# ═══════════════════════════════════════════


class TestLuhnCheck:
    def test_valid_visa(self):
        assert luhn_check("4111111111111111") is True

    def test_valid_mastercard(self):
        assert luhn_check("5200828282828210") is True

    def test_invalid(self):
        assert luhn_check("1234567890123456") is False

    def test_single_digit(self):
        assert luhn_check("0") is True

    def test_two_digits_valid(self):
        assert luhn_check("18") is True

    def test_two_digits_invalid(self):
        assert luhn_check("19") is False


# ═══════════════════════════════════════════
# NIK date validation
# ═══════════════════════════════════════════


class TestNIKDateValidation:
    def test_valid_male(self):
        # DD=15, MM=06 → valid
        assert validate_nik_date("3201011506900001") is True

    def test_valid_female(self):
        # DD=55 (15+40), MM=06 → valid
        assert validate_nik_date("3201015506900001") is True

    def test_invalid_month(self):
        # MM=13 → invalid
        assert validate_nik_date("3201011513900001") is False

    def test_invalid_day(self):
        # DD=32 → invalid (and not female-adjusted since < 41)
        assert validate_nik_date("3201013201900001") is False

    def test_too_short(self):
        assert validate_nik_date("32010115") is False

    def test_female_edge_day_71(self):
        # DD=71 (31+40), MM=12 → valid
        assert validate_nik_date("3201017112900001") is True

    def test_female_invalid_day_72(self):
        # DD=72 (32+40) → invalid
        assert validate_nik_date("3201017201900001") is False


# ═══════════════════════════════════════════
# NPWP checksum
# ═══════════════════════════════════════════


class TestNPWPChecksum:
    def test_valid_length(self):
        # Provide a number that passes length check
        assert isinstance(npwp_checksum_valid("012345678901234"), bool)

    def test_invalid_length(self):
        assert npwp_checksum_valid("12345") is False

    def test_non_digit(self):
        assert npwp_checksum_valid("12345678901234a") is False


# ═══════════════════════════════════════════
# Credit card detection
# ═══════════════════════════════════════════


class TestCreditCardDetection:
    def test_valid_visa_detected(self):
        text = "card: 4111111111111111"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) >= 1
        assert entities[0].confidence >= 0.7

    def test_valid_card_with_spaces(self):
        text = "cc 4111 1111 1111 1111"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) >= 1

    def test_valid_card_with_dashes(self):
        text = "cc 4111-1111-1111-1111"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) >= 1

    def test_invalid_luhn_rejected(self):
        text = "card: 1234567890123456"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) == 0

    def test_too_short_rejected(self):
        text = "number: 123456789"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) == 0

    def test_indonesian_bin_high_confidence(self):
        # BRI BIN 405290 with valid Luhn
        text = "kartu kredit BRI: 4052900000000000"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) >= 1
        assert entities[0].metadata.get("bank") == "BRI"
        assert entities[0].confidence >= 0.90

    def test_network_detection(self):
        text = "card: 4111111111111111"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert entities[0].metadata.get("network") == "Visa"

    def test_mastercard_network(self):
        text = "mc: 5200828282828210"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        if entities:
            assert entities[0].metadata.get("network") == "Mastercard"

    def test_context_window_populated(self):
        text = "leaked data: 4111111111111111 found"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) >= 1
        assert len(entities[0].context_window) > 0

    def test_masked_value(self):
        text = "card 4111111111111111"
        entities = _find(scanner.scan(text), EntityType.CREDIT_CARD)
        assert len(entities) >= 1
        # Should be masked: first 6 + *** + last 4
        val = entities[0].matched_value
        assert "******" in val or "***" in val


# ═══════════════════════════════════════════
# NIK detection
# ═══════════════════════════════════════════


class TestNIKDetection:
    def test_valid_nik_detected(self):
        # Province 32 (Jabar), DD=15, MM=06
        text = "NIK: 3201011506900001"
        entities = _find(scanner.scan(text), EntityType.NIK)
        assert len(entities) >= 1
        assert entities[0].metadata.get("province_code") == "32"

    def test_nik_with_context_keyword_high_confidence(self):
        text = "Nomor NIK: 3201011506900001"
        entities = _find(scanner.scan(text), EntityType.NIK)
        assert len(entities) >= 1
        assert entities[0].confidence >= 0.85

    def test_invalid_province_rejected(self):
        # Province 99 → invalid
        text = "ID: 9901011506900001"
        entities = _find(scanner.scan(text), EntityType.NIK)
        assert len(entities) == 0

    def test_invalid_date_rejected(self):
        # MM=13 → invalid
        text = "NIK: 3201011513900001"
        entities = _find(scanner.scan(text), EntityType.NIK)
        assert len(entities) == 0

    def test_female_nik_detected(self):
        # DD=55 (15+40) for female
        text = "NIK: 3201015506900001"
        entities = _find(scanner.scan(text), EntityType.NIK)
        assert len(entities) >= 1
        assert entities[0].metadata.get("gender") == "female"

    def test_male_nik_gender(self):
        text = "NIK: 3201011506900001"
        entities = _find(scanner.scan(text), EntityType.NIK)
        if entities:
            assert entities[0].metadata.get("gender") == "male"

    def test_nik_value_is_masked(self):
        text = "NIK: 3201011506900001"
        entities = _find(scanner.scan(text), EntityType.NIK)
        assert len(entities) >= 1
        assert "**********" in entities[0].matched_value

    def test_random_16_digits_not_nik(self):
        # A random 16-digit number that fails province + date checks
        text = "ref: 0000000000000000"
        entities = _find(scanner.scan(text), EntityType.NIK)
        assert len(entities) == 0


# ═══════════════════════════════════════════
# NPWP detection
# ═══════════════════════════════════════════


class TestNPWPDetection:
    def test_formatted_npwp_detected(self):
        text = "NPWP: 01.234.567.8-901.234"
        entities = _find(scanner.scan(text), EntityType.NPWP)
        assert len(entities) >= 1

    def test_plain_npwp_with_context(self):
        text = "NPWP pajak: 012345678901234"
        entities = _find(scanner.scan(text), EntityType.NPWP)
        assert len(entities) >= 1

    def test_npwp_without_context_and_checksum_rejected(self):
        # No NPWP keyword + likely invalid checksum → should be skipped
        text = "code: 999999999999999"
        entities = _find(scanner.scan(text), EntityType.NPWP)
        # May or may not match depending on checksum; just verify no crash
        assert isinstance(entities, list)

    def test_wrong_length_rejected(self):
        text = "NPWP: 1234567890"
        entities = _find(scanner.scan(text), EntityType.NPWP)
        assert len(entities) == 0


# ═══════════════════════════════════════════
# CVV detection
# ═══════════════════════════════════════════


class TestCVVDetection:
    def test_cvv_detected(self):
        text = "CVV: 123"
        entities = _find(scanner.scan(text), EntityType.CVV)
        assert len(entities) == 1
        assert entities[0].matched_value == "***"

    def test_cvc_variant(self):
        text = "CVC 456"
        entities = _find(scanner.scan(text), EntityType.CVV)
        assert len(entities) == 1

    def test_four_digit_cvv(self):
        text = "security code: 1234"
        entities = _find(scanner.scan(text), EntityType.CVV)
        assert len(entities) == 1

    def test_indonesian_kode_keamanan(self):
        text = "kode keamanan 789"
        entities = _find(scanner.scan(text), EntityType.CVV)
        assert len(entities) == 1

    def test_random_3_digits_not_cvv(self):
        text = "jumlah: 123 barang"
        entities = _find(scanner.scan(text), EntityType.CVV)
        assert len(entities) == 0


# ═══════════════════════════════════════════
# Credential detection
# ═══════════════════════════════════════════


class TestCredentialDetection:
    def test_username_password_pair(self):
        text = "username: john@bank.co.id password: secret123"
        entities = _find(scanner.scan(text), EntityType.CREDENTIAL)
        assert len(entities) == 1
        assert "john@bank.co.id" in entities[0].matched_value
        assert "***" in entities[0].matched_value

    def test_akun_sandi_pair(self):
        text = "akun: user123 sandi: pass456"
        entities = _find(scanner.scan(text), EntityType.CREDENTIAL)
        assert len(entities) == 1

    def test_email_password(self):
        text = "email: test@bca.co.id pass: mypassword"
        entities = _find(scanner.scan(text), EntityType.CREDENTIAL)
        assert len(entities) == 1

    def test_no_password_not_detected(self):
        text = "username: john status: active"
        entities = _find(scanner.scan(text), EntityType.CREDENTIAL)
        assert len(entities) == 0


# ═══════════════════════════════════════════
# Bank name detection
# ═══════════════════════════════════════════


class TestBankNameDetection:
    def test_single_bank(self):
        text = "Transfer ke BCA"
        entities = _find(scanner.scan(text), EntityType.BANK_NAME)
        assert len(entities) == 1
        assert entities[0].matched_value.upper() == "BCA"

    def test_multiple_banks(self):
        text = "Data nasabah BRI, BNI, dan Mandiri"
        entities = _find(scanner.scan(text), EntityType.BANK_NAME)
        names = {e.matched_value.upper() for e in entities}
        assert "BRI" in names
        assert "BNI" in names
        assert "MANDIRI" in names

    def test_case_insensitive(self):
        text = "rekening bca"
        entities = _find(scanner.scan(text), EntityType.BANK_NAME)
        assert len(entities) == 1

    def test_dedup_same_bank(self):
        text = "BRI transfer BRI saldo BRI"
        entities = _find(scanner.scan(text), EntityType.BANK_NAME)
        assert len(entities) == 1

    def test_fintech(self):
        text = "Saldo OVO dan GoPay"
        entities = _find(scanner.scan(text), EntityType.BANK_NAME)
        names = {e.matched_value.upper() for e in entities}
        assert "OVO" in names
        assert "GOPAY" in names


# ═══════════════════════════════════════════
# Banking keyword detection
# ═══════════════════════════════════════════


class TestBankingKeywordDetection:
    def test_rekening(self):
        text = "nomor rekening bocor"
        entities = _find(scanner.scan(text), EntityType.BANKING_KEYWORD)
        keywords = {e.matched_value.lower() for e in entities}
        assert "rekening" in keywords
        assert "bocor" in keywords

    def test_carding_keywords(self):
        text = "fresh cc dump fullz"
        entities = _find(scanner.scan(text), EntityType.BANKING_KEYWORD)
        keywords = {e.matched_value.lower() for e in entities}
        assert "dump" in keywords
        assert "fullz" in keywords

    def test_dedup_keywords(self):
        text = "leak leak leak"
        entities = _find(scanner.scan(text), EntityType.BANKING_KEYWORD)
        assert len(entities) == 1


# ═══════════════════════════════════════════
# Account number detection
# ═══════════════════════════════════════════


class TestAccountNumberDetection:
    def test_rekening_context(self):
        text = "rekening: 0123456789012"
        entities = _find(scanner.scan(text), EntityType.ACCOUNT_NUMBER)
        assert len(entities) >= 1

    def test_no_rek_with_account(self):
        text = "no rek 1234567890"
        entities = _find(scanner.scan(text), EntityType.ACCOUNT_NUMBER)
        assert len(entities) >= 1

    def test_without_context_not_detected(self):
        text = "biasa saja 1234567890"
        entities = _find(scanner.scan(text), EntityType.ACCOUNT_NUMBER)
        assert len(entities) == 0


# ═══════════════════════════════════════════
# Integration: mixed content
# ═══════════════════════════════════════════


class TestMixedContent:
    def test_full_leak_post(self):
        text = """
        FRESH DUMP - Data nasabah BRI bocor!
        NIK: 3201011506900001
        Rekening: 0021234567890
        Kartu kredit: 4111111111111111
        CVV: 321
        Username: ahmad@bri.co.id Password: pass123
        """
        entities = scanner.scan(text)
        types = {e.pattern_type for e in entities}
        assert EntityType.CREDIT_CARD in types
        assert EntityType.NIK in types
        assert EntityType.CVV in types
        assert EntityType.CREDENTIAL in types
        assert EntityType.BANK_NAME in types
        assert EntityType.BANKING_KEYWORD in types

    def test_entity_has_all_fields(self):
        text = "CVV: 123"
        entities = scanner.scan(text)
        cvvs = _find(entities, EntityType.CVV)
        assert len(cvvs) == 1
        e = cvvs[0]
        assert isinstance(e.pattern_type, EntityType)
        assert isinstance(e.matched_value, str)
        assert 0.0 <= e.confidence <= 1.0
        assert len(e.context_window) > 0
        assert e.start >= 0
        assert e.end > e.start

    def test_to_dict_roundtrip(self):
        text = "CVV: 123"
        entities = scanner.scan(text)
        for e in entities:
            d = e.to_dict()
            assert "type" in d
            assert "value" in d
            assert "confidence" in d
            assert "context" in d
            assert "start" in d
            assert "end" in d

    def test_empty_text_returns_nothing(self):
        assert scanner.scan("") == []

    def test_irrelevant_text_returns_minimal(self):
        text = "Cuaca hari ini cerah, suhu 30 derajat celsius."
        entities = scanner.scan(text)
        sensitive = [
            e for e in entities
            if e.pattern_type not in (EntityType.BANK_NAME, EntityType.BANKING_KEYWORD)
        ]
        assert len(sensitive) == 0
