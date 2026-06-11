"""Production-grade Indonesian financial data regex patterns with validation.

Detects: credit cards (with Luhn), NIK (with date validation), NPWP (with
checksum), bank accounts, credentials, CVV, and bank name mentions.
All patterns are compiled once at module level for performance.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass, field
from typing import List


# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────

class EntityType(str, enum.Enum):
    CREDIT_CARD = "CREDIT_CARD"
    NIK = "NIK"
    NPWP = "NPWP"
    ACCOUNT_NUMBER = "ACCOUNT_NUMBER"
    CREDENTIAL = "CREDENTIAL"
    CVV = "CVV"
    BANK_NAME = "BANK_NAME"
    BANKING_KEYWORD = "BANKING_KEYWORD"


# ─────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────

@dataclass
class IndonesianFinancialEntity:
    """A single financial entity detected in text."""

    pattern_type: EntityType
    matched_value: str
    confidence: float
    context_window: str
    start: int
    end: int
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "type": self.pattern_type.value,
            "value": self.matched_value,
            "confidence": self.confidence,
            "context": self.context_window,
            "start": self.start,
            "end": self.end,
            "metadata": self.metadata,
        }


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _context_window(text: str, start: int, end: int, size: int = 50) -> str:
    """Return *size* chars around the match, clamped to text boundaries."""
    ctx_start = max(0, start - size)
    ctx_end = min(len(text), end + size)
    return text[ctx_start:ctx_end]


def luhn_check(number: str) -> bool:
    """Validate a numeric string with the Luhn algorithm."""
    digits = [int(d) for d in number]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for d in even_digits:
        total += sum(divmod(d * 2, 10))
    return total % 10 == 0


def validate_nik_date(nik: str) -> bool:
    """Check that digits 7-12 of a NIK encode a valid date (DDMMYY).

    Female citizens have 40 added to the DD part, so DD can be 01-31
    or 41-71.
    """
    if len(nik) < 12:
        return False
    try:
        dd = int(nik[6:8])
        mm = int(nik[8:10])
    except ValueError:
        return False
    if dd > 40:
        dd -= 40
    return 1 <= dd <= 31 and 1 <= mm <= 12


def npwp_checksum_valid(digits: str) -> bool:
    """Validate NPWP using weighted-sum mod-10 checksum.

    NPWP format: XX.XXX.XXX.X-XXX.XXX (15 digits).
    Weights cycle: [4, 3, 2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2].
    The weighted sum mod 10 should equal 0 for a valid NPWP.
    """
    if len(digits) != 15 or not digits.isdigit():
        return False
    weights = [4, 3, 2, 7, 6, 5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    total = sum(int(d) * w for d, w in zip(digits, weights))
    return total % 10 == 0


# ─────────────────────────────────────────────
# Indonesian bank BIN prefixes (first 6 digits)
# ─────────────────────────────────────────────

INDONESIAN_BINS: dict[str, list[str]] = {
    "BRI":     ["405290", "405291", "405292", "520082", "530314", "455633"],
    "BNI":     ["410505", "410506", "521264", "547609"],
    "Mandiri": ["413718", "413719", "461700", "461701", "526422"],
    "BCA":     ["540078", "517562", "455032", "455033"],
    "BSI":     ["427022", "427023"],
    "CIMB":    ["525429", "525430", "405582"],
    "Permata": ["431420", "431421"],
    "Danamon": ["520080", "520081"],
    "Mega":    ["426504", "426505"],
    "BTN":     ["485470", "485471"],
}

_ALL_BINS: set[str] = set()
for _bins in INDONESIAN_BINS.values():
    _ALL_BINS.update(_bins)

# Known Indonesian bank account prefixes (for account number detection)
_BANK_ACCOUNT_PREFIXES: dict[str, list[str]] = {
    "BCA":     ["012", "013", "235"],
    "Mandiri": ["100", "130", "155"],
    "BRI":     ["002", "003", "033"],
    "BNI":     ["009", "015", "018"],
    "BSI":     ["700", "701"],
}


# ─────────────────────────────────────────────
# Compiled regex patterns
# ─────────────────────────────────────────────

# Credit card: 13-19 digit sequences (may contain spaces/dashes)
RE_CREDIT_CARD = re.compile(
    r"(?<!\d)(\d(?:[ -]*\d){12,18})(?!\d)"
)

# NIK: exactly 16 digits (Indonesian National ID)
RE_NIK = re.compile(
    r"(?<!\d)(\d{16})(?!\d)"
)

# NPWP: XX.XXX.XXX.X-XXX.XXX or plain 15-digit
RE_NPWP = re.compile(
    r"(?<!\d)(\d{2}[.]?\d{3}[.]?\d{3}[.]?\d[-]?\d{3}[.]?\d{3})(?!\d)"
)

# Indonesian bank account: 10-16 digits (contextual — near bank keywords)
RE_BANK_ACCOUNT = re.compile(
    r"(?i)(?:rek(?:ening)?|no\.?\s*rek|account|acct|a/c|tabungan|giro)"
    r"[:\s.#]*"
    r"(\d[\d .-]{8,18}\d)"
)

# CVV: 3-4 digit code near card context words
RE_CVV = re.compile(
    r"(?i)(?:cvv|cvc|cv2|cvn|security\s*code|kode\s*keamanan)[:\s]*(\d{3,4})\b"
)

# Credential pairs: username/email + password on same or adjacent lines
RE_CREDENTIALS = re.compile(
    r"(?i)(?:user(?:name)?|email|akun|login|id)[:\s=]+(\S+)"
    r"[\s|,;]{0,80}?"
    r"(?:pass(?:word)?|sandi|pin|pwd)[:\s=]+(\S+)"
)

# Expiry date near card context
RE_EXPIRY = re.compile(
    r"(?i)(?:exp(?:iry)?|valid\s*(?:thru|until)|berlaku)[:\s]*"
    r"(\d{2}[/\-]\d{2,4})"
)

# Indonesian bank name mentions
BANK_NAMES = [
    "BRI", "BNI", "Mandiri", "BCA", "BSI", "CIMB Niaga", "CIMB",
    "Permata", "Danamon", "Mega", "BTN", "BTPN", "OCBC NISP",
    "Maybank", "Panin", "Sinarmas", "Bukopin", "Muamalat",
    "Bank Jago", "Bank Neo", "Jenius", "DANA", "OVO", "GoPay",
    "ShopeePay", "LinkAja", "Bank DKI", "Bank Jatim", "Bank Jateng",
    "Bank BJB",
]
RE_BANK_NAMES = re.compile(
    r"(?i)\b(" + "|".join(re.escape(b) for b in BANK_NAMES) + r")\b"
)

# Common Indonesian banking / threat keywords
BANKING_KEYWORDS = [
    "rekening", "tabungan", "kartu kredit", "kartu debit",
    "internet banking", "mobile banking", "m-banking",
    "transfer", "mutasi", "saldo", "ATM", "PIN",
    "token listrik", "nomor kartu", "kode OTP",
    "data nasabah", "bocor", "leak", "dump", "fullz",
    "combolist", "log bank", "carding", "cc live",
    "fresh cc", "valid cc", "credit card",
]
RE_BANKING_KEYWORDS = re.compile(
    r"(?i)\b(" + "|".join(re.escape(k) for k in BANKING_KEYWORDS) + r")\b"
)


# ─────────────────────────────────────────────
# Scanner
# ─────────────────────────────────────────────

class PatternScanner:
    """Scan text and return all detected Indonesian financial entities."""

    def scan(self, text: str) -> List[IndonesianFinancialEntity]:
        """Run all pattern detectors against *text* and return findings."""
        entities: List[IndonesianFinancialEntity] = []
        entities.extend(self._scan_credit_cards(text))
        entities.extend(self._scan_nik(text))
        entities.extend(self._scan_npwp(text))
        entities.extend(self._scan_account_numbers(text))
        entities.extend(self._scan_cvv(text))
        entities.extend(self._scan_credentials(text))
        entities.extend(self._scan_bank_names(text))
        entities.extend(self._scan_banking_keywords(text))
        return entities

    # ── Credit cards ──

    def _scan_credit_cards(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        for m in RE_CREDIT_CARD.finditer(text):
            digits = re.sub(r"[ -]", "", m.group(1))
            if not digits.isdigit() or len(digits) < 13 or len(digits) > 19:
                continue
            if not luhn_check(digits):
                continue
            bin6 = digits[:6]
            bank = self._bin_to_bank(bin6)
            # Higher confidence for known Indonesian BINs
            confidence = 0.95 if bank else 0.70
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.CREDIT_CARD,
                matched_value=self._mask_card(digits),
                confidence=confidence,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
                metadata={
                    "bank": bank,
                    "bin": bin6,
                    "card_length": len(digits),
                    "network": self._detect_network(digits),
                },
            ))
        return results

    @staticmethod
    def _bin_to_bank(bin6: str) -> str | None:
        for bank, bins in INDONESIAN_BINS.items():
            if bin6 in bins:
                return bank
        return None

    @staticmethod
    def _detect_network(digits: str) -> str:
        first = int(digits[0])
        first2 = int(digits[:2])
        if first == 4:
            return "Visa"
        if 51 <= first2 <= 55:
            return "Mastercard"
        if first2 in (34, 37):
            return "Amex"
        if first2 == 62:
            return "UnionPay"
        if first2 == 36:
            return "Diners"
        if first2 == 35:
            return "JCB"
        return "Unknown"

    @staticmethod
    def _mask_card(digits: str) -> str:
        """Mask all but first 6 and last 4 digits."""
        if len(digits) <= 10:
            return digits[:4] + "*" * (len(digits) - 4)
        return digits[:6] + "*" * (len(digits) - 10) + digits[-4:]

    # ── NIK ──

    def _scan_nik(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        for m in RE_NIK.finditer(text):
            nik = m.group(1)
            # Skip if already captured as a credit card (Luhn-valid 16-digit)
            if luhn_check(nik):
                continue
            if not validate_nik_date(nik):
                continue
            province = int(nik[:2])
            if province < 1 or province > 92:
                continue
            # Check context for NIK-related keywords to boost confidence
            ctx = _context_window(text, m.start(), m.end(), 80).lower()
            has_context = any(kw in ctx for kw in [
                "nik", "ktp", "identitas", "penduduk", "dukcapil",
            ])
            confidence = 0.90 if has_context else 0.70
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.NIK,
                matched_value=nik[:6] + "**********",
                confidence=confidence,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
                metadata={
                    "province_code": nik[:2],
                    "district_code": nik[2:4],
                    "subdistrict_code": nik[4:6],
                    "gender": "female" if int(nik[6:8]) > 40 else "male",
                },
            ))
        return results

    # ── NPWP ──

    def _scan_npwp(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        for m in RE_NPWP.finditer(text):
            raw = m.group(1)
            digits = re.sub(r"[.\- ]", "", raw)
            if len(digits) != 15:
                continue
            has_checksum = npwp_checksum_valid(digits)
            # Check context for NPWP-related keywords
            ctx = _context_window(text, m.start(), m.end(), 80).lower()
            has_context = any(kw in ctx for kw in [
                "npwp", "pajak", "tax", "wajib pajak",
            ])
            if not has_checksum and not has_context:
                continue
            confidence = 0.90 if has_checksum and has_context else (
                0.80 if has_checksum else 0.60
            )
            formatted = (
                f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}.{digits[8]}"
                f"-{digits[9:12]}.{digits[12:]}"
            )
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.NPWP,
                matched_value=formatted,
                confidence=confidence,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
                metadata={
                    "checksum_valid": has_checksum,
                    "taxpayer_code": digits[0:2],
                },
            ))
        return results

    # ── Account numbers ──

    def _scan_account_numbers(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        for m in RE_BANK_ACCOUNT.finditer(text):
            raw = m.group(1)
            digits = re.sub(r"[ .-]", "", raw)
            if not digits.isdigit():
                continue
            if len(digits) < 10 or len(digits) > 16:
                continue
            bank = self._account_to_bank(digits)
            confidence = 0.80 if bank else 0.60
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.ACCOUNT_NUMBER,
                matched_value=digits[:3] + "*" * (len(digits) - 6) + digits[-3:],
                confidence=confidence,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
                metadata={"bank": bank, "length": len(digits)},
            ))
        return results

    @staticmethod
    def _account_to_bank(digits: str) -> str | None:
        prefix3 = digits[:3]
        for bank, prefixes in _BANK_ACCOUNT_PREFIXES.items():
            if prefix3 in prefixes:
                return bank
        return None

    # ── CVV ──

    def _scan_cvv(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        for m in RE_CVV.finditer(text):
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.CVV,
                matched_value="***",
                confidence=0.75,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
            ))
        return results

    # ── Credentials ──

    def _scan_credentials(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        for m in RE_CREDENTIALS.finditer(text):
            username = m.group(1)
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.CREDENTIAL,
                matched_value=f"user={username} pass=***",
                confidence=0.85,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
                metadata={"username": username},
            ))
        return results

    # ── Bank names ──

    def _scan_bank_names(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        seen: set[str] = set()
        for m in RE_BANK_NAMES.finditer(text):
            name = m.group(1).upper()
            if name in seen:
                continue
            seen.add(name)
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.BANK_NAME,
                matched_value=m.group(1),
                confidence=1.0,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
            ))
        return results

    # ── Banking keywords ──

    def _scan_banking_keywords(self, text: str) -> List[IndonesianFinancialEntity]:
        results: List[IndonesianFinancialEntity] = []
        seen: set[str] = set()
        for m in RE_BANKING_KEYWORDS.finditer(text):
            kw = m.group(1).lower()
            if kw in seen:
                continue
            seen.add(kw)
            results.append(IndonesianFinancialEntity(
                pattern_type=EntityType.BANKING_KEYWORD,
                matched_value=m.group(1),
                confidence=1.0,
                context_window=_context_window(text, m.start(), m.end()),
                start=m.start(),
                end=m.end(),
            ))
        return results
