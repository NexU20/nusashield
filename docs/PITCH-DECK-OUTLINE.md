# Pitch Deck Outline — SHARK-Fin (Tahap 2)

**Digdaya x Hackathon 2026 / PIDI**
**Tim 418 — Source Hunting Alert and Risk Knowledge for Financial Intelligence**

---

## Catatan Penyaji (Speaker Notes — baca dulu sebelum menyusun slide)

- **Durasi target:** 13 slide untuk pitch ~8-10 menit (≈40-45 detik/slide), dengan Slide Demo (6) sebagai puncak yang boleh memakan waktu lebih panjang.
- **Aturan kejujuran (wajib dipatuhi seluruh slide):** classifier adalah **deteksi deterministik tervalidasi (regex + validasi algoritmik), bukan NLP/ML**. Setiap angka adopsi, harga, pasar, dampak, dan MTTD ditandai **"estimasi"**. Window deteksi `<24 jam` adalah **target rancangan**, bukan hasil terukur — data demo berasal dari **seed (20 threat)** karena collector live butuh kredensial produksi.
- **Klaim yang sudah LIVE dan teruji (boleh diklaim tegas):** pipeline Collection → Intelligence → Action, classifier 8 entitas, risk scorer 0-100, masking dua-lapis UU PDP, webhook dispatch ke SOC, audit-log, draft SEOJK 29/2022 siap-tinjau, 102 tes otomatis lulus.
- **Klaim yang masih ROADMAP (sebut sebagai visi, bukan kapabilitas saat ini):** feed pengawasan lintas-lembaga (Suptech / FS-ISAC), multi-tenant penuh, Alembic migration, deployment multi-worker, enkripsi at-rest, RBAC.
- **Bukti tertaut:** demo live `https://shark-fin-zeta.vercel.app/`, repo + CI `https://github.com/0xNoramiya/shark-fin`.

---

## Slide 1 — Judul & Positioning

**SHARK-Fin — Deteksi Dini Kebocoran Data Keuangan & Otomasi Pelaporan SEOJK**

- **Tim 418** — Muhammad Rifqi Haikal (founder/solo dev). Latar: keamanan siber, blockchain, CTF (1-3 tahun) — relevan langsung dengan threat-intelligence & OSINT.
- **Kepanjangan:** Source Hunting Alert and Risk Knowledge for Financial Intelligence.
- **Problem Statement:** PS1 **Cyber Security & Data Protection** (primer) + **Regtech & Suptech** (sekunder); tema makro **Manajemen Risiko**.
- **Satu kalimat:** Platform intelijen ancaman OSINT yang memantau sumber publik untuk kebocoran data keuangan Indonesia, mengklasifikasi & memberi skor risiko, lalu menjembatani temuan ke kewajiban lapor regulasi.
- **Bukti hidup:** demo `shark-fin-zeta.vercel.app` + repo ber-CI `github.com/0xNoramiya/shark-fin`.
- *Akronim, sub-problem, dan positioning konsisten dengan Tahap-1 — pematangan, bukan rebrand.*

---

## Slide 2 — Problem

**Lembaga keuangan kalah cepat dari peneliti eksternal saat datanya bocor**

- Kebocoran data keuangan Indonesia umumnya **baru disadari setelah berbulan-bulan**, dan kerap **pertama kali diungkap peneliti eksternal — bukan lembaga itu sendiri**.
- Pola berulang (semua diungkap pihak eksternal lebih dulu):

| Kasus | Skala | Tahun | Pengungkap awal |
|---|---|---|---|
| BRI Life | ~2 juta nasabah + 463.000 dokumen | 2021 | Akun eksternal @UnderTheBreach |
| BPJS Kesehatan | 279 juta data penduduk | 2021 | User "Kotz" di RaidForums |
| Paspor RI | 34,9 juta data | 2023 | Peneliti eksternal (Teguh Aprianto) |
| Data Dukcapil | 337 juta data kependudukan | 2023 | Peneliti eksternal |

- **Akar masalah:** belum ada pemantauan OSINT proaktif **berbahasa Indonesia**, dan tidak ada otomasi yang menjembatani temuan ke kewajiban regulasi.
- **Benturan langsung:** rata-rata waktu identifikasi breach sektor keuangan **168 hari** (IBM 2024) vs kewajiban notifikasi awal **24 jam** (SEOJK 29/2022) dan **3x24 jam** (UU PDP 27/2022).

---

## Slide 3 — Urgensi & Data

**Pasar "must-have" yang didorong regulasi, bukan "nice-to-have"**

- **Skala ancaman (terverifikasi, dengan sumber):**

| Indikator | Angka | Sumber |
|---|---|---|
| Peringkat dunia jumlah akun bocor (2020-2024) | ke-8 | Surfshark |
| Data terverifikasi di dark web (Sep 2024) | 7 juta akun dari 450+ instansi | OJK mengutip BSSN (Nov 2024) |
| Indikator paparan sepanjang 2024 | 56,1 juta dari 461 instansi (3,58% sektor keuangan) | Laporan BSSN via Prosperita (Okt 2025) |
| Pengaduan external fraud 2024 | 2.688 | OJK (Feb 2025) |
| Rata-rata kerugian breach sektor keuangan | USD 5,9 juta (acuan, bukan jaminan) | IBM 2023 |

- **Tekanan kepatuhan (demand struktural):** SEOJK 29/2022 (notifikasi 24 jam), POJK 11/2022 (mitigasi risiko TI), **POJK 12/2024 (anti-fraud seluruh LJK, bukan hanya bank)**, Peraturan BSSN 1&2/2024 (CIRT/krisis).
- **Celah kelembagaan:** UU PDP berlaku penuh Okt 2024, tetapi **Lembaga PDP belum operasional** hingga awal 2026 (Perpres masih harmonisasi) — peluang positioning sebagai pengisi celah.
- *Konsekuensi tak diselesaikan: gagal lapor → sanksi & reputasi, kerugian finansial, erosi kepercayaan publik atas digitalisasi keuangan.*

---

## Slide 4 — Solusi

**Pipeline OSINT tiga-lapis: dari sumber publik → kepatuhan terstruktur**

- **Collection** — 4 collector ber-poll memantau **sumber publik & legal** (Telegram publik 5 mnt, Pastebin/Rentry 15 mnt, GitHub default 30 mnt, Google Dork default 1 jam). *Bukan akses ilegal dark web.*
- **Intelligence** — classifier **deterministik tervalidasi** (8 tipe entitas) + risk scorer 0-100 → LOW/MEDIUM/HIGH/CRITICAL; deduplikasi SHA-256; masking sebelum simpan.
- **Action** — feed dashboard analis, **webhook ke SOC** (terfilter `min_severity`), **draft notifikasi SEOJK 29/2022 Bab IX siap-tinjau**, dan audit-log tertelusur.
- **Satu pipeline, bukan dua produk:** temuan ancaman siber langsung dikonversi menjadi keluaran kepatuhan — inilah irisan PS1 (Cyber/Data Protection) × Regtech/Suptech.
- **Pemetaan masalah → fitur → outcome:**

| Masalah | Fitur | Outcome (estimasi) |
|---|---|---|
| Deteksi terlambat 168 hari | Collection poll 5 mnt-1 jam | Jendela deteksi → skala menit-jam |
| False positive membanjiri analis | Classifier validasi algoritmik + scorer 0-100 | Triase terprioritaskan, tiap skor dapat dijelaskan |
| Gagal lapor 24 jam | Draft SEOJK 29/2022 + webhook + audit-log | Kepatuhan dapat dibuktikan & tertelusur |
| Data bocor saat ditangani | Masking dua-lapis + dedup SHA-256 + mode hash-only | `raw_content` tak pernah keluar via API |

---

## Slide 5 — Demo (Live Walkthrough)

**Lihat sendiri: `shark-fin-zeta.vercel.app`**

- **Alur demo (live):**
  1. **Landing → Dashboard** — feed ancaman dengan filter severity/source/status.
  2. **Threat detail** — entitas terdeteksi sudah **tersamar** (mis. kartu kredit `405290******0000`, NIK `121212**`, kredensial `***`) + skor risiko + faktor penilaian.
  3. **Status workflow** — analis: `NEW → VERIFIED → MITIGATED` (ber-audit, butuh `X-API-Key`).
  4. **Ekspor laporan** — `GET /threats/{id}/report?format=ojk` menghasilkan **draft SEOJK 29/2022 Bab IX** siap-tinjau (Bahasa Indonesia).
  5. **Webhook & audit** — registrasi subscriber SOC + jejak audit `report.export` / `threat.status_update`.
- **Pengakuan jujur (disampaikan saat demo):** data yang tampil berasal dari **seed (20 threat: 3 CRITICAL / 5 HIGH / 8 MEDIUM / 4 LOW)** karena collector live memerlukan kredensial produksi (Telegram/GitHub/Google CSE). Pipeline & UI **nyata berjalan**; efektivitas deteksi real-world diuji pada pilot.
- *Lampiran: screenshot `docs/screenshots/dashboard.png`, `landing.png`; contoh draft SEOJK yang dihasilkan.*

---

## Slide 6 — Diferensiasi (Classifier ID-native + Compliance OJK)

**Dua moat yang tidak dimiliki kompetitor: classifier Indonesia + jembatan regulasi**

- **Moat 1 — Classifier Indonesia-native (deterministik, explainable, auditable):**
  - **NIK** — validasi tanggal lahir + kode provinsi.
  - **NPWP** — checksum weighted-sum mod-10.
  - **Kartu kredit** — Luhn + tabel **10 BIN bank nasional** (BRI, BNI, Mandiri, BCA, BSI, CIMB, Permata, Danamon, Mega, BTN).
  - Plus nomor rekening, kredensial, CVV, nama bank, kata kunci perbankan Bahasa Indonesia.
  - Determinisme = keunggulan untuk konteks regulasi: setiap temuan **dapat dijelaskan & diaudit**, false-positive rendah pada entitas ber-checksum.
- **Moat 2 — Satu-satunya yang menjembatani deteksi → kewajiban regulasi:** draft notifikasi **SEOJK 29/2022 Bab IX** otomatis (siap-tinjau, bukan submission otomatis ke portal OJK).
- **Peta kompetitor:**

| Pemain | Fokus | Gap vs SHARK-Fin |
|---|---|---|
| CSIRTradar (Prosperita) | Dark web monitoring lokal | Generik; tanpa classifier NIK/NPWP/BIN; tanpa output SEOJK; tak menyasar BPR/fintech kecil |
| Telkomsigma DRP | DRP enterprise BUMN | Mahal/berat; tak terjangkau BPR & fintech kecil; tanpa output kepatuhan terstruktur |
| ITSEC Asia | MSSP/threat-intel APAC | Jasa konsultasi berbiaya tinggi; feed global; bukan SaaS swalayan murah |
| Recorded Future / Group-IB / Cyble | DRP/threat-intel global | Sangat mahal; tanpa native NIK/NPWP/BIN ID; tanpa output SEOJK |

- *Murni OSINT sumber publik. Indonesia belum punya padanan FS-ISAC sektor keuangan — gap inti yang dibidik.*

---

## Slide 7 — Arsitektur

**Monorepo, 4 layanan Docker Compose — sesuai kode, tanpa overclaim**

- **Tiga lapis:** Collection → Intelligence → Action.
- **Stack:** Python 3.11 / FastAPI (async) · React 18 / Vite 6 · **PostgreSQL 16 (sumber kebenaran + otoritas dedup)** · **Redis 7 (cache jalur-cepat, OPSIONAL, graceful degrade)** · APScheduler (4 job interval).
- **Aliran data (pipeline `scheduler._process_intel`):**

```
collectors/*.collect() → RawIntel
  → content_hash SHA-256
  → dedup: Redis fast-path (set sharkfin:seen_hashes, TTL 7h) → fallback PostgreSQL
  → PatternScanner (8 entitas, validasi algoritmik)
  → RiskScorer 0-100 → severity
  → mask_sensitive() → content_preview
  → persist Threat (raw_content tak pernah keluar via API)
  → dispatch_webhooks() (best-effort, filter min_severity) + record_audit
```

- **API `/api/v1`:** threats (feed/detail/status), reports (draft OJK/intel), alerts (webhook CRUD), stats, audit. **Auth `X-API-Key`** pada endpoint tulis/ekspor/audit; baca bersifat publik. `/health` melaporkan status DB & Redis.
- **Keamanan & privasi (UU PDP Pasal 16):** masking dua-lapis; mode **hash-only (default)**; actor audit = **fingerprint SHA-256 kunci (non-reversibel)**.
- **Batas jujur (roadmap):** `Base.metadata.create_all` (belum Alembic), single-worker dev, enkripsi at-rest & RBAC belum ada.
- *Lampiran: Diagram Arsitektur Sistem (blok diagram pada bagian E proposal).*

---

## Slide 8 — Traksi & Progress Stage-2

**Dari klaim Tahap-1 → bukti terverifikasi Tahap-2**

| Aspek | Tahap-1 | Tahap-2 (terverifikasi di repo) |
|---|---|---|
| Sumber OSINT aktif | 2 | **4 collector** |
| Endpoint ber-auth | 0 | **5 (X-API-Key)** |
| Raw content via API | Ya | **Tidak (masked)** |
| Webhook dispatch | Placeholder | **LIVE, dipanggil di pipeline** |
| Redis dedup-cache | Klaim | **Nyata (set + TTL 7h) + /health** |
| Audit-log | Klaim | **Live (fingerprint actor, non-reversibel)** |
| Tes otomatis | (dilaporkan) | **102 lulus** |
| Bundle JS terbesar | ~695 KB | **382 KB** |

- **Breakdown 102 tes:** 63 patterns · 16 scorer · 14 API · 5 webhook · 4 audit. **CI GitHub Actions** jalan pada push/PR ke `backend/**` (Postgres 16 service).
- **Kejujuran sebagai integritas:** "NLP classifier" **dikoreksi** menjadi deteksi deterministik tervalidasi — dijadikan keunggulan explainability, bukan disembunyikan.
- **Bisnis:** TAM/SAM/SOM eksplisit + perhitungan inline ditambahkan; rencana validasi pasar primer (wawancara/survei praktisi) disiapkan.
- **Status saat ini:** **PROTOTYPE FUNGSIONAL menuju pilot** (belum pilot). Bukti tertaut: demo live + repo ber-CI + 102 tes lulus.

---

## Slide 9 — Market & TAM / SAM / SOM

**Bottom-up: jumlah lembaga × harga tier (semua estimasi, asumsi eksplisit)**

- **Denominator terverifikasi (OJK/BI 2024-2025):** ~105 bank umum · ~1.360 BPR · 97 fintech P2P/LPBBTI berizin · ~50 penerbit e-wallet · 3-4 regulator anchor.

| Lapisan | Nilai (estimasi/tahun) | Cakupan & dasar hitung |
|---|---|---|
| **TAM** | ~Rp 350-550 miliar | Seluruh LJK terawasi OJK + regulator jika semua berlangganan tier relevan |
| **SAM** | ~Rp 70-100 miliar | (45 bank Tier-2 × Rp 50 jt/bln × 12) + (350 BPR/fintech Tier-3 × Rp 10 jt/bln × 12) + 1 regulator ~Rp 0,4 M ≈ Rp 70 M |
| **SOM** | ~Rp 0,3-2,5 miliar (12-24 bln pasca-pilot) | Konservatif: 1 anchor + 2-3 Tier-3 · Optimis: 2 Tier-2 + 8 Tier-3 |

- **Segmentasi:** Regulator (anchor) / LJK besar (BUKU 3-4, fintech menengah) / LJK kecil (BPR, fintech P2P kecil).
- **Filter SAM:** dari ~1.360 BPR, ~300-400 disaring berdasarkan aset & kanal digital aktif yang beranggaran TI memadai untuk Tier-3.
- *White space nyata: BPR/fintech kecil diabaikan vendor enterprise; Indonesia belum punya padanan FS-ISAC sektor keuangan — pasar terdefinisi & didorong regulasi.*

---

## Slide 10 — Model Bisnis & Harga

**SaaS B2B tiga tier + kontrak anchor-regulator**

| Tier | Segmen | Harga (estimasi) |
|---|---|---|
| **Tier-1 Regulator** | OJK / BI / BSSN | Negosiasi per lembaga; ~Rp 300-500 jt/tahun; feed lintas-lembaga + dashboard nasional |
| **Tier-2 Profesional** | Bank BUKU 3-4, bank digital, fintech menengah | ~Rp 30-75 jt/bln (~Rp 360-900 jt/tahun) |
| **Tier-3 Reguler** | BPR, fintech P2P kecil | ~Rp 8 jt/bln (rentang Rp 5-15 jt; ~Rp 60-180 jt/tahun) |

- **Mengapa Tier-3 terjangkau:** pipeline terotomasi penuh + deteksi **deterministik tanpa biaya GPU/ML** → marjin tinggi & biaya marginal per pelanggan rendah.
- **Break-even (estimasi):** 8 klien Tier-3 **ATAU** 2 klien Tier-2.
- **Proyeksi ARR (estimasi, dibatasi kapasitas solo):** Tahun-1 ~Rp 0,3-0,6 M (1 anchor pilot + 2-3 Tier-3) · Tahun-2 ~Rp 2-2,5 M (2 Tier-2 + 8 Tier-3) · Tahun-3 berkembang seiring penambahan tim.
- **Asumsi eksplisit:** siklus pilot → kontrak berbayar 6-9 bulan (pengadaan LJK diakui lambat); dari 3 pilot diasumsikan 1-2 konversi.
- **Funding:** hibah inovasi OJK/PIDI/BI sebagai bootstrap — **bukan prasyarat keberlanjutan**. ROI argumen: Tier-3 Rp 8 jt/bln proporsional vs eksposur sanksi UU PDP (hingga 2% pendapatan tahunan) + biaya notifikasi/remediasi.

---

## Slide 11 — Partnership & Distribusi

**Kemitraan = go-to-market utama, bukan penjualan satuan**

- **Key partners:**
  - **OJK** — anchor + jalur regulasi yang memicu adopsi turunan LJK terawasi.
  - **BSSN** — komplementer kerangka CIRT/krisis (Reg 1&2/2024) di sisi **hulu pra-insiden**.
  - **PPATK** — intelijen keuangan.
  - **Asosiasi industri** — **PERBARINDO** (BPR), **AFPI/AFTECH** (fintech P2P), **ASPI** (sistem pembayaran) sebagai kanal distribusi massal.
- **Jalur distribusi:**
  1. **Anchor-regulator** — feed/dashboard OJK mendorong lembaga terawasi mengadopsi.
  2. **Asosiasi** — satu demo Perbarindo menjangkau ~50 BPR sekaligus → menekan biaya akuisisi pada siklus pengadaan yang lambat.
  3. **Webhook-native** — onboarding ke SOC/SIEM eksisting **<1 hari**.
  4. **PIDI** — akselerator, jaringan mentor, kemungkinan sumber hibah.
- **Funnel awal:** demo publik live mengonversi calon pelanggan → pilot → langganan berjenjang.
- *Catatan: karena siklus regulator panjang, pendapatan Tahun-1 didahulukan via jalur Tier-3/asosiasi, bukan bergantung pada anchor.*

---

## Slide 12 — Roadmap & Ask

**Prototype → Pilot → Feed Regulator**

- **Roadmap fase:**

| Fase | Periode (estimasi) | Fokus |
|---|---|---|
| Fase 1 — Prototype | Feb-Apr 2026 | **SELESAI** — pipeline 4-collector, dashboard, webhook, draft SEOJK, 102 tes |
| Fase 2 — Penguatan | Apr-Jun 2026 | **Berjalan** — hardening, validasi pasar primer (wawancara/survei), advisor compliance |
| Fase 3 — Pilot | Jun-Sep 2026 | **Pilot 2-3 lembaga** — uji efektivitas MTTD nyata pertama |

- **Roadmap teknis (di luar MVP):** Alembic migration (saat ini `create_all`), deployment multi-worker, multi-tenant penuh, enkripsi at-rest, RBAC, ekspansi entitas & sumber.
- **Visi Tahun-2:** feed pengawasan **lintas-lembaga (Suptech, analog FS-ISAC)** — network-effect: tiap lembaga baru menambah nilai feed bagi seluruh ekosistem.
- **The Ask:**
  - **Akses & endorsement** ke jalur anchor-regulator (OJK) dan asosiasi (PERBARINDO/AFPI) untuk 2-3 LoI / pilot.
  - **Mentorship & jaringan PIDI** + eksplorasi hibah inovasi sebagai bootstrap go-to-market.
  - **Dukungan untuk merekrut** 1 backend/data engineer + 1 advisor compliance (eks-OJK/PPATK).

---

## Slide 13 — Tim

**Tim 418 — solo dev dengan rencana mitigasi konkret**

- **Founder:** Muhammad Rifqi Haikal (`rhaikal91@gmail.com` · `github.com/0xNoramiya`). Latar keamanan siber, blockchain, CTF (1-3 tahun) — relevan langsung dengan threat-intelligence & OSINT.
- **Risiko diakui jujur:** tim solo = risiko bus-factor & kapasitas eksekusi.
- **Mitigasi teknis:** kodebase **modular** (collectors / classifier / API terpisah) + **102 tes otomatis** + **CI GitHub Actions** → onboarding kontributor cepat, ketergantungan pada satu orang menurun.
- **Mitigasi go-to-market:** rencana rekrut **1 backend/data engineer** + **1 advisor compliance (eks-OJK/PPATK)** yang sekaligus membuka pintu business development; jalur **asosiasi** menggantikan penjualan satuan; keterlibatan **mentor PIDI**.
- **Penutup:** SHARK-Fin = infrastruktur publik-privat untuk memperpendek jendela deteksi kebocoran data keuangan Indonesia dari ratusan hari menuju mendekati real-time — bukti, bukan klaim: demo live + 102 tes + repo ber-CI.

---

## Lampiran yang Dirujuk Deck

1. Demo live: `https://shark-fin-zeta.vercel.app/`
2. Repositori + CI: `https://github.com/0xNoramiya/shark-fin`
3. Diagram Arsitektur Sistem (tiga lapis + topologi 4 layanan).
4. Tabel Verifikasi Statistik (setiap angka + sumber + tahun: Surfshark, BSSN/OJK, IBM, OJK fraud).
5. `FIXES.md` + riwayat commit penajaman Tahap-2.
6. Output 102 tes lulus (breakdown 63/16/14/5/4) + workflow CI.
7. Tabel komparasi kompetitor (CSIRTradar / Telkomsigma / ITSEC / global vs SHARK-Fin).
8. Worksheet TAM/SAM/SOM (jumlah lembaga × harga tier, asumsi eksplisit).
9. Contoh output draft SEOJK 29/2022 Bab IX siap-tinjau.
10. Screenshot dashboard & landing (`docs/screenshots/`).
11. Hasil wawancara/survei pasar (dilampirkan saat tersedia).
