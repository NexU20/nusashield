"""Auto-generated SEOJK 29/2022 draft notifikasi and internal intel report."""

from __future__ import annotations

import uuid
from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from app.middleware.auth import require_api_key
from app.services.audit import record_audit
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.threat import Threat, mask_sensitive

router = APIRouter(prefix="/threats", tags=["reports"])

_SEV_ID = {
    "CRITICAL": "KRITIS",
    "HIGH": "TINGGI",
    "MEDIUM": "SEDANG",
    "LOW": "RENDAH",
}

_STATUS_ID = {
    "NEW": "Baru",
    "VERIFIED": "Terverifikasi",
    "MITIGATED": "Sudah Dimitigasi",
    "FALSE_POSITIVE": "Positif Palsu",
}

_SRC_ID = {
    "TELEGRAM": "Telegram (kanal publik)",
    "PASTE": "Paste site (Pastebin/Rentry)",
    "GITHUB": "Repositori GitHub publik",
    "HIBP": "HaveIBeenPwned",
    "GOOGLE_DORK": "Google Custom Search (dork)",
}

_BULAN = [
    "", "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]

_ENTITY_LABEL = {
    "CREDIT_CARD": "Nomor Kartu Kredit",
    "NIK": "Nomor Induk Kependudukan (NIK)",
    "NPWP": "Nomor Pokok Wajib Pajak (NPWP)",
    "CREDENTIAL": "Kredensial (username/password)",
    "ACCOUNT_NUMBER": "Nomor Rekening Bank",
    "CVV": "Kode CVV/CVC",
    "BANK_NAME": "Nama Lembaga Keuangan",
    "BANKING_KEYWORD": "Kata Kunci Perbankan",
}

_ENTITY_PLAIN = {
    "CREDIT_CARD": "nomor kartu kredit",
    "NIK": "Nomor Induk Kependudukan (NIK)",
    "NPWP": "Nomor Pokok Wajib Pajak (NPWP)",
    "CREDENTIAL": "kredensial akses (username/password)",
    "ACCOUNT_NUMBER": "nomor rekening bank",
    "CVV": "kode keamanan kartu (CVV/CVC)",
}

_REKOMENDASI: dict[str, list[str]] = {
    "CREDIT_CARD": [
        "Segera blokir kartu-kartu yang teridentifikasi dan terbitkan kartu pengganti.",
        "Aktifkan monitoring transaksi real-time untuk BIN yang terdampak.",
        "Koordinasi dengan principal (Visa/Mastercard) untuk fraud alert pada BIN terkait.",
    ],
    "NIK": [
        "Laporkan ke Dukcapil untuk penandaan NIK yang terekspos.",
        "Tingkatkan verifikasi identitas (multi-factor) untuk pembukaan rekening baru menggunakan NIK terdampak.",
        "Notifikasi nasabah terkait potensi penyalahgunaan identitas.",
    ],
    "NPWP": [
        "Koordinasi dengan Direktorat Jenderal Pajak terkait NPWP yang terekspos.",
        "Pantau aktivitas perpajakan mencurigakan dari NPWP terdampak.",
        "Edukasi wajib pajak terkait potensi penipuan menggunakan data NPWP mereka.",
    ],
    "CREDENTIAL": [
        "Paksa reset password untuk seluruh akun yang teridentifikasi.",
        "Aktifkan two-factor authentication (2FA) wajib untuk akun terdampak.",
        "Lakukan analisis log akses untuk mendeteksi unauthorized login.",
    ],
    "ACCOUNT_NUMBER": [
        "Tingkatkan monitoring transaksi pada rekening yang terekspos.",
        "Hubungi nasabah terkait untuk verifikasi aktivitas terakhir.",
        "Pertimbangkan penggantian nomor rekening jika terdapat indikasi penyalahgunaan.",
    ],
    "CVV": [
        "Segera blokir kartu dengan CVV yang terekspos.",
        "Terbitkan kartu pengganti dengan nomor baru.",
        "Aktifkan 3D Secure untuk seluruh transaksi online pada kartu terdampak.",
    ],
}

_DEFAULT_REKOMENDASI = [
    "Lakukan investigasi lebih lanjut terhadap sumber kebocoran data.",
    "Tingkatkan pemantauan pada sumber-sumber OSINT terkait.",
    "Koordinasi dengan BSSN dan pihak berwenang untuk tindak lanjut.",
]


def _format_date_wib(dt) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    from datetime import timedelta as td
    wib_dt = dt + td(hours=7)
    return (
        f"{wib_dt.day:02d} {_BULAN[wib_dt.month]} {wib_dt.year}, "
        f"{wib_dt.hour:02d}:{wib_dt.minute:02d} WIB"
    )


def _sensitive_entity_types(entities: list[dict]) -> list[str]:
    """Return entity types excluding BANK_NAME and BANKING_KEYWORD."""
    return list({
        e.get("type", "")
        for e in entities
        if e.get("type", "") not in ("BANK_NAME", "BANKING_KEYWORD", "")
    })


def _entity_types_plain(entities: list[dict]) -> str:
    types = _sensitive_entity_types(entities)
    names = [_ENTITY_PLAIN.get(t, _ENTITY_LABEL.get(t, t).lower()) for t in types]
    return ", ".join(names) if names else "data keuangan"


def _build_summary_ojk(
    entities: list[dict], tags: list[str], source_type: str, count: int,
) -> str:
    inst = ", ".join(tags) if tags else "lembaga keuangan"
    src = _SRC_ID.get(source_type, source_type)
    data_str = _entity_types_plain(entities)
    s1 = (
        f"Ditemukan indikasi kebocoran data {data_str} "
        f"nasabah {inst} sebanyak estimasi {count} entitas "
        f"yang dipublikasikan di {src}."
    )
    s2 = f"Data yang terekspos meliputi {data_str}."
    return f"{s1}\n   {s2}"


def _build_entity_table(entities: list[dict]) -> str:
    counts: dict[str, int] = {}
    for e in entities:
        t = e.get("type", "UNKNOWN")
        counts[t] = counts.get(t, 0) + 1
    lines = [f"   {'Tipe Data':<35} {'Jumlah':>8}", "   " + "-" * 45]
    for t, c in sorted(counts.items()):
        label = _ENTITY_LABEL.get(t, t)
        lines.append(f"   {label:<35} {c:>8}")
    lines.append("   " + "-" * 45)
    lines.append(f"   {'TOTAL':<35} {sum(counts.values()):>8}")
    return "\n".join(lines)


def _build_rekomendasi(entities: list[dict]) -> str:
    etypes = {e.get("type", "") for e in entities if e.get("type", "") in _REKOMENDASI}
    recs = [_REKOMENDASI[t][0] for t in list(etypes)[:3]]
    while len(recs) < 3:
        for fb in _DEFAULT_REKOMENDASI:
            if fb not in recs:
                recs.append(fb)
                if len(recs) >= 3:
                    break
    return "\n".join(f"   {i+1}. {r}" for i, r in enumerate(recs[:3]))


# ── Endpoint: Draft Notifikasi OJK (SEOJK 29/2022 Bab IX) ──

@router.get(
    "/{threat_id}/report",
    response_class=PlainTextResponse,
)
async def generate_notifikasi_ojk(
    threat_id: uuid.UUID,
    format: str = Query(default="ojk"),
    session: AsyncSession = Depends(get_session),
    api_key: str = Depends(require_api_key),
) -> str:
    """Generate draft notifikasi awal mengacu SEOJK 29/2022 Bab IX.

    Every export is written to the audit log.
    """
    threat = await session.get(Threat, threat_id)
    if not threat:
        raise HTTPException(status_code=404, detail="Threat not found")

    entities = threat.detected_entities.get("entities", [])
    tags = threat.institution_tags or []
    count = len(entities)
    nomor = f"DRAFT-SHARK-{str(threat.id)[:8].upper()}"

    await record_audit(
        session,
        action="report.export",
        api_key=api_key,
        target_id=threat_id,
        detail={"format": format},
    )

    if format == "intel":
        return _build_intel_report(threat, entities, tags)

    return f"""\
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
DRAFT NOTIFIKASI AWAL INSIDEN SIBER
[BELUM RESMI \u2014 Perlu ditinjau dan ditandatangani pejabat berwenang
 sebelum disampaikan ke OJK]
Mengacu: SEOJK No. 29/SEOJK.03/2022 Bab IX huruf (a)
Nomor Draft    : {nomor}
Dibuat oleh    : SHARK-Fin Threat Intelligence Platform
Tanggal draft  : {_format_date_wib(threat.created_at)}
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501

A. IDENTITAS BANK PELAPOR
   Nama Bank         : [ISI NAMA BANK]
   Kode Bank         : [ISI KODE BANK]
   Nama Penanggung   : [ISI NAMA PEJABAT]
   Jabatan           : [ISI JABATAN]
   Kontak            : [ISI EMAIL/TELEPON]

B. INFORMASI INSIDEN
   Tanggal/Waktu insiden pertama terdeteksi oleh SHARK-Fin:
     {_format_date_wib(threat.created_at)}

   Sumber deteksi    : {_SRC_ID.get(threat.source_type.value, threat.source_type.value)}
   URL sumber        : {threat.source_url or '-'}
   Risk score        : {threat.risk_score}/100 ({_SEV_ID.get(threat.severity.value, threat.severity.value)})

   Deskripsi singkat insiden:
   {_build_summary_ojk(entities, tags, threat.source_type.value, count)}

C. ESTIMASI DAMPAK AWAL
   Jenis data terekspos  : {_entity_types_plain(entities)}
{_build_entity_table(entities)}
   Lembaga terdampak     : {', '.join(tags) if tags else '(Perlu diverifikasi)'}

   CATATAN: Estimasi ini bersumber dari deteksi otomatis SHARK-Fin
   dan PERLU DIVERIFIKASI oleh tim keamanan internal sebelum
   dicantumkan dalam laporan resmi.

D. LANGKAH MITIGASI AWAL
   [Isi sesuai tindakan yang telah diambil oleh bank]

   Rekomendasi SHARK-Fin berdasarkan tipe data:
{_build_rekomendasi(entities)}

E. STATUS PELAPORAN
   Status saat ini   : {_STATUS_ID.get(threat.status.value, threat.status.value)}
   Diverifikasi oleh : [ISI NAMA ANALIS]
   Tanggal verifikasi: [ISI TANGGAL]

\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
DOKUMEN BERIKUTNYA YANG DIPERLUKAN:
Laporan Insiden Siber lengkap (SEOJK 29/2022 Bab IX huruf b)
wajib disampaikan melalui sistem pelaporan OJK dalam 5 hari kerja.
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
"""


# ── Internal intel report ──

def _build_intel_report(threat: object, entities: list[dict], tags: list[str]) -> str:
    counts: dict[str, int] = {}
    for e in entities:
        counts[e.get("type", "?")] = counts.get(e.get("type", "?"), 0) + 1

    entity_lines = []
    for i, e in enumerate(entities):
        conf = e.get("confidence", 0)
        entity_lines.append(
            f"   {i+1}. [{_ENTITY_LABEL.get(e['type'], e['type'])}] "
            f"{e.get('value', '-')} (confidence: {conf*100:.0f}%)"
        )

    rekomendasi = []
    seen = set()
    for e in entities:
        t = e.get("type", "")
        if t in _REKOMENDASI and t not in seen:
            seen.add(t)
            for r in _REKOMENDASI[t]:
                rekomendasi.append(r)

    rek_lines = "\n".join(
        f"   {i+1}. {r}" for i, r in enumerate(rekomendasi[:6])
    ) if rekomendasi else "   (Tidak ada rekomendasi spesifik)"

    return f"""\
LAPORAN INTELIJEN INTERNAL \u2014 SHARK-Fin
==========================================
Nomor          : INTEL-SHARK-{str(threat.id)[:8].upper()}
Tanggal        : {_format_date_wib(threat.created_at)}
Tingkat        : {_SEV_ID.get(threat.severity.value, threat.severity.value)}
Status         : {_STATUS_ID.get(threat.status.value, threat.status.value)}
Skor Risiko    : {threat.risk_score}/100
Sumber         : {_SRC_ID.get(threat.source_type.value, threat.source_type.value)}
URL            : {threat.source_url or '-'}
Lembaga Terkait: {', '.join(tags) if tags else '-'}

ENTITAS TERDETEKSI ({len(entities)})
------------------------------------
{chr(10).join(entity_lines)}

DISTRIBUSI TIPE
---------------
{chr(10).join(f'   {_ENTITY_LABEL.get(t, t)}: {c}' for t, c in sorted(counts.items()))}

REKOMENDASI TEKNIS
------------------
{rek_lines}

INDIKATOR TEKNIS
----------------
   Hash konten     : {threat.content_hash}
   Preview tersamar: {threat.content_preview or mask_sensitive(threat.raw_content or '')[:200]}

   CATATAN: Konten asli tidak disimpan sesuai prinsip minimisasi
   data (UU PDP Pasal 16). Hash SHA-256 dapat digunakan untuk
   verifikasi tanpa mengekspos data sensitif.

==========================================
Dokumen internal SHARK-Fin. Tidak untuk distribusi eksternal.
"""
