# SHARK-Fin — Progress Log Tahap 2

**Source Hunting Alert and Risk Knowledge for Financial Intelligence**
Tim 418 — Muhammad Rifqi Haikal (solo developer)

| Item | Nilai |
|---|---|
| Problem Statement | PS1 Cyber Security & Data Protection (primer) + Regtech/Suptech (sekunder), tema Manajemen Risiko |
| Status saat ini | Prototype fungsional menuju pilot (belum pilot) |
| Demo live | https://shark-fin-zeta.vercel.app/ |
| Repositori | https://github.com/0xNoramiya/shark-fin |
| Suite tes | 102 tes otomatis lulus (`102 passed in 3.57s`) |
| Tanggal dokumen | 30 Mei 2026 |

Dokumen ini adalah catatan teknis terperinci ("changelog") yang merinci setiap perbaikan yang dikerjakan sejak submission Tahap 1. Setiap butir disertai kondisi *sebelum* dan *sesudah*, bukti di repositori, dan dampaknya terhadap klaim proposal. Seluruh isi dasar pada fakta yang telah diverifikasi langsung di codebase dan pada layanan yang berjalan; setiap angka proyeksi/asumsi ditandai eksplisit sebagai "estimasi".

---

## 1. Ringkasan Eksekutif Perubahan

Fokus Tahap 2 adalah **mengubah klaim arsitektur Tahap 1 menjadi kapabilitas yang benar-benar terbukti di kode dan teruji otomatis**, sekaligus mengoreksi *overclaim* agar proposal jujur dan dapat diaudit. Delapan perbaikan utama dirangkum berikut, lalu diuraikan satu per satu pada Bagian 3.

| # | Perbaikan | Dampak ringkas pada klaim proposal |
|---|---|---|
| 1 | Webhook dispatch terhubung ke pipeline | Klaim "webhook dispatch ke SOC" berubah dari *belum dipanggil* menjadi *live & teruji* |
| 2 | Audit log: model + endpoint + fingerprint actor | Klaim "audit log immutable & traceability" yang dulu belum terbukti kini nyata & teruji |
| 3 | Redis dedup fast-path + `/health` | Klaim pemanfaatan Redis berubah dari asumsi menjadi terverifikasi pada layanan hidup |
| 4 | Privasi: `STORE_RAW_CONTENT` default `False` | Memperkuat klaim minimisasi data UU PDP — mode hash-only menjadi default |
| 5 | Bugfix `env_ignore_empty` | Menghapus *crash* boot dengan `.env` default — kelayakan deploy/CI |
| 6 | CI backend (GitHub Actions) | Klaim "teruji" menjadi dapat-diverifikasi otomatis tiap push/PR |
| 7 | Demo seed (webhook + audit) | Demo live menampilkan jejak audit & subscriber webhook, bukan sekadar threat |
| 8 | Suite tes 93 → 102 | Pembuktian kuantitatif penambahan cakupan (webhook + audit) |

Selain delapan butir di atas, dilakukan satu **koreksi kejujuran teknis** yang sudah berjalan sejak penajaman: istilah "NLP classifier" (Tahap 1) dikoreksi menjadi **deteksi deterministik tervalidasi (regex + validasi algoritmik)** — bukan ML. Koreksi ini bukan penambahan fitur, melainkan penyelarasan klaim dengan kode aktual (lihat Bagian 4).

---

## 2. Metode Verifikasi

Seluruh fakta pada dokumen ini diverifikasi dengan:

1. **Menjalankan suite tes** di dalam container backend yang aktif terhadap PostgreSQL 16 nyata:
   `pytest -q` → **`102 passed in 3.57s`**.
2. **Memeriksa endpoint `/health` yang hidup**:
   `{"status":"ok","service":"shark-fin","dependencies":{"database":"ok","redis":"ok"}}`.
3. **Inspeksi kode sumber** untuk setiap klaim wiring (scheduler, services, api, models, config) dan **riwayat commit** (`FIXES.md` + git log).

Breakdown tes (terverifikasi via hitung fungsi `def test_` per berkas):

| Berkas | Jumlah tes | Cakupan |
|---|---|---|
| `tests/test_patterns.py` | 63 | Classifier: Luhn, validasi NIK, checksum NPWP, tabel BIN |
| `tests/test_scorer.py` | 16 | Risk scorer 0–100, tier severity, multiplier |
| `tests/test_api.py` | 14 | Endpoint API, auth (401 saat tanpa kunci) |
| `tests/test_webhook.py` | 5 | CRUD subscriber, filter severity, skip inactive, no-subscribers=0 |
| `tests/test_audit.py` | 4 | Pencatatan audit, auth wajib, fingerprint non-reversibel |
| **Total** | **102** | — |

> Catatan teknis: tes API/webhook/audit menggunakan PostgreSQL nyata (bukan SQLite) dan httpx `ASGITransport`. Dispatch webhook di-*mock* dengan `httpx.AsyncClient` palsu sehingga tidak ada panggilan jaringan nyata saat tes.

---

## 3. Changelog Perbaikan Tahap 2 (Before / After)

### Perbaikan 1 — Webhook dispatch terhubung ke pipeline koleksi

**Sebelum.** Endpoint webhook hanya berupa *placeholder* dan dispatch belum dipanggil dari pipeline; klaim Tahap 1 "webhook dispatch ke SOC" belum dapat dibuktikan berjalan.

**Sesudah.** `scheduler._process_intel` memanggil `services.webhook.dispatch_webhooks` setelah setiap threat dipersistensi. Karakteristik yang terverifikasi di kode (`backend/app/services/webhook.py`, `backend/app/scheduler.py`):

- Filter per-subscriber berdasarkan `min_severity` melalui peta `_SEVERITY_ORDER` (LOW < MEDIUM < HIGH < CRITICAL).
- Header `X-SHARK-Fin-Key` dikirim ke endpoint subscriber.
- Payload **hanya tersamar**: `content_preview` (sudah di-mask) + `entity_counts` per tipe — tidak ada konten mentah.
- `httpx.AsyncClient(timeout=10.0)`.
- Dibungkus `try/except` di scheduler sehingga kegagalan webhook **tidak pernah** menghentikan pipeline koleksi.

**Bukti.** `tests/test_webhook.py` (5 tes): filter severity, skip subscriber non-aktif, dan kasus tanpa subscriber (mengembalikan 0).

**Dampak pada klaim proposal.** Memperkuat Bagian D (Solution Approach), E4 (Creativity in Implementation — distribusi *webhook-native*), dan G6 (Adoption Readiness — integrasi SOC). Klaim berubah dari *direncanakan* menjadi *terimplementasi & teruji*.

---

### Perbaikan 2 — Audit log penuh: model + endpoint + fingerprint actor

**Sebelum.** Tahap 1 mengklaim "audit log immutable" dan traceability, namun belum ada model/endpoint/aktor yang terbukti di repo.

**Sesudah.** Audit log terimplementasi end-to-end:

- **Model** `backend/app/models/audit.py` — `AuditLog(action, actor, target_id, detail JSONB, created_at)`, kolom `action` dan `created_at` ter-indeks.
- **Aktor non-reversibel** — fungsi `fingerprint()` menyimpan `"key:" + sha256(key)[:12]` (atau `"anonymous"`), bukan kunci asli.
- **Service** `backend/app/services/audit.py` — `record_audit()` bersifat *best-effort* dengan commit sendiri sehingga tidak mematahkan request pemanggil.
- **Endpoint** `GET /api/v1/audit` (auth `X-API-Key`), `backend/app/api/audit.py`, mendukung filter `action` dan `limit` (1–500).

**Aksi yang benar-benar dicatat saat runtime (terverifikasi di kode):**

| Aksi | Lokasi pemanggilan | Status runtime |
|---|---|---|
| `threat.status_update` | `api/threats.py` (PATCH status) | Dicatat |
| `report.export` | `api/reports.py` (ekspor laporan) | Dicatat |
| `webhook.register` | `api/alerts.py` (registrasi) | Dicatat |
| `webhook.delete` | `api/alerts.py` (nonaktifkan) | Dicatat |

**Bukti.** `tests/test_audit.py` (4 tes): pencatatan berhasil, endpoint memerlukan auth (401 tanpa kunci), dan fingerprint non-reversibel; registrasi/penghapusan webhook diverifikasi mencatat audit secara live.

**Dampak pada klaim proposal.** Mendukung E6 (Security & Compliance — traceability selaras SEOJK 29/2022 & POJK 11/2022) dan D3 (Impact Measurement — entri audit per insiden). Seluruh aksi tulis (status, ekspor laporan, registrasi/penghapusan webhook) kini tertelusur di audit-log runtime.

---

### Perbaikan 3 — Redis dedup fast-path + `/health` dependensi DB & Redis

**Sebelum.** Tahap 1 menyebut Redis (bahkan sempat diistilahkan "Redis queue") sebagai klaim infrastruktur yang belum terbukti.

**Sesudah.** Redis menjadi **akselerator dedup opsional**, bukan antrian dan bukan sumber kebenaran (`backend/app/cache.py`):

- `seen_recently()` / `remember()` beroperasi pada set bersama `sharkfin:seen_hashes` dengan TTL 7 hari.
- `scheduler._process_intel` mengecek **Redis fast-path** sebelum query dedup ke DB; PostgreSQL tetap otoritatif via *unique* `content_hash` (SHA-256).
- **Graceful degradation**: jika Redis tidak tersedia, seluruh operasi menjadi *no-op* dan pipeline tetap berjalan.
- `/health` memanggil `cache.ping()` dan melaporkan status `database` serta `redis`.

**Bukti.** `/health` pada layanan hidup mengembalikan `{"status":"ok","dependencies":{"database":"ok","redis":"ok"}}`.

**Dampak pada klaim proposal.** Menyelaraskan E1 (System Architecture) dan E3 (Method Innovation — *graceful degradation*) dengan kode. Redis dideskripsikan sebagai *cache hot-path*, bukan *queue*. **Catatan jujur:** manfaat "penskalaan horizontal lintas-worker via Redis" bersifat **arsitektural/laten** — deployment saat ini `uvicorn --reload` *single-worker* (dev), sehingga manfaat itu belum benar-benar dieksekusi (lihat Bagian 5).

---

### Perbaikan 4 — Privasi by default: `STORE_RAW_CONTENT` default `False`

**Sebelum.** `raw_content` berpotensi menyimpan teks asli; narasi minimisasi data belum diberlakukan sebagai default.

**Sesudah.** Dua lapis proteksi nyata dan terverifikasi:

1. **`mask_sensitive()`** (`models/threat.py`) menyamarkan kartu kredit (simpan 4+4), NIK (simpan 6+2), serta nilai password/pin/secret menjadi `[TERSEMBUNYI]`, lalu memotong ke 200 karakter (membangun `content_preview`).
2. **Flag `STORE_RAW_CONTENT`** (`config.py`, default **`False`**; `.env.example=false`). Dalam mode hash-only, `scheduler._process_intel` menetapkan `stored_raw = preview` sehingga kolom `raw_content` tidak pernah menerima teks asli; teks penuh hanya dipakai *in-memory* untuk klasifikasi/dedup.

Eksposur API: skema `ThreatResponse` **tidak** menyertakan `raw_content` — hanya `content_preview`, `detected_entities` (nilai sudah ter-mask, mis. `405290******0000`, `***`, `user=x pass=***`), dan `content_hash` (SHA-256). Aktor audit juga disimpan sebagai fingerprint SHA-256, bukan kunci.

**Dampak pada klaim proposal.** Memperkuat E6 (Security & Compliance) dan C (Ecosystem Alignment) — selaras Pasal 16 UU PDP (minimisasi data). Menjawab kelemahan Tahap 1 langsung di tingkat *default* konfigurasi.

---

### Perbaikan 5 — Bugfix `env_ignore_empty` pada parsing Settings

**Sebelum.** Nilai kosong di `.env.example` (mis. `TELEGRAM_CHANNELS=`) memicu kegagalan JSON-parse saat Settings dimuat — berpotensi men-*crash* boot aplikasi dan CI.

**Sesudah.** `config.py` menetapkan `SettingsConfigDict(env_ignore_empty=True)` plus `field_validator` untuk `TELEGRAM_API_ID` dan `TELEGRAM_CHANNELS`, sehingga nilai kosong jatuh ke default alih-alih gagal parse.

**Bukti.** Container boot dengan `.env` yang ter-commit; 102 tes memuat Settings tanpa error.

**Dampak pada klaim proposal.** Mendukung E5 (Data & Feasibility) dan E7 (MVP Readiness) — kelayakan menjalankan prototype dengan konfigurasi default (pilot ringan), tanpa harus mengisi seluruh kredensial.

---

### Perbaikan 6 — Continuous Integration backend (GitHub Actions)

**Sebelum.** Tidak ada CI; "teruji" hanya dapat dibuktikan manual.

**Sesudah.** `.github/workflows/backend-tests.yml`:

- Menyalakan service `postgres:16-alpine` (user/db `siakfin`), Python 3.11, cache pip.
- Menjalankan `pytest -v` pada `push`/`pull_request` yang menyentuh `backend/**` (dan pada `workflow_dispatch`).
- `TEST_DATABASE_URL` diarahkan ke `localhost:5432` di CI (default `postgres:5432` di Docker, dapat di-*override*).

**Dampak pada klaim proposal.** Menjadikan klaim "102 tes lulus" **dapat diverifikasi otomatis** oleh panitia melalui status workflow — bukti integritas teknis (mendukung Bagian H Attachment butir CI).

---

### Perbaikan 7 — Demo seed: webhook subscriber + entri audit

**Sebelum.** Demo hanya menampilkan threat; jejak audit dan integrasi webhook tidak terlihat.

**Sesudah.** `backend/scripts/seed_demo.py` menyemai:

- **20 threat** dengan distribusi 3 CRITICAL / 5 HIGH / 8 MEDIUM / 4 LOW.
- **2 subscriber webhook**: BRI SOC (`min_severity=HIGH`) dan AFTECH CSIRT (`min_severity=CRITICAL`).
- **3 entri audit**: `threat.status_update`, `report.export`, dan `webhook.register`.

**Dampak pada klaim proposal.** Memperkuat H2 (Current Status) dan G6 (Adoption Readiness) — demo live mencerminkan alur operasional analis (status workflow, ekspor laporan, integrasi SOC). **Catatan jujur:** data demo berasal dari seed; efektivitas deteksi *real-world* belum terukur di produksi (collectors butuh kredensial yang kosong pada `.env.example` — lihat Bagian 5).

---

### Perbaikan 8 — Pertumbuhan suite tes: 93 → 102

**Sebelum.** Laporan suite Tahap 1 sebanyak 93 tes.

**Sesudah.** 102 tes, konsisten dengan penambahan dua berkas tes baru pada Tahap 2:

| Kelompok | Jumlah | Catatan |
|---|---|---|
| Inti (patterns 63 + scorer 16 + api 14) | 93 | Setara baseline Tahap 1 |
| `test_webhook.py` | +5 | Baru (Perbaikan 1) |
| `test_audit.py` | +4 | Baru (Perbaikan 2) |
| **Total** | **102** | Selisih +9 |

**Dampak pada klaim proposal.** Memberi bukti kuantitatif bahwa dua kapabilitas baru (webhook & audit) tidak sekadar ditambahkan tetapi juga **tercakup oleh tes** — mendukung E5/E7 dan Bagian H.

---

## 4. Koreksi Kejujuran Teknis (bukan fitur baru)

| Klaim Tahap 1 | Realitas terverifikasi | Tindakan |
|---|---|---|
| "NLP classifier" | Murni regex + validasi algoritmik: Luhn (kartu kredit), validasi NIK (tanggal lahir + kode provinsi), checksum NPWP (mod-10 berbobot), tabel `INDONESIAN_BINS` (10 bank); deterministik & explainable | Direframe menjadi "deteksi deterministik tervalidasi" |
| "Redis queue" | Redis = cache dedup hot-path (set bersama, TTL 7 hari), bukan antrian; Postgres otoritatif | Direframe menjadi "dedup-cache dengan graceful degradation" |

Koreksi ini diposisikan sebagai **keunggulan untuk explainability/audit regulasi** (E3), bukan kelemahan. Determinisme juga menjadi argumen *unit economics* (G3 — tanpa biaya GPU/ML).

---

## 5. Keterbatasan yang Diakui (transparansi)

Agar tidak *overclaim* di luar realitas teknis, keterbatasan berikut diakui eksplisit. Masing-masing berada dalam *roadmap*, bukan diklaim selesai:

1. **~~Registrasi webhook belum diaudit saat runtime~~ — SUDAH DIPERBAIKI.** `POST /alerts/webhook/register` dan `DELETE /alerts/webhook/{id}` (`api/alerts.py`) kini memanggil `record_audit` (`webhook.register` / `webhook.delete`), diverifikasi live. Seluruh aksi tulis kini tertelusur.
2. **`api_key` subscriber webhook disimpan plaintext** di kolom `webhook_subscriptions.api_key` (mis. seed `demo-bri-soc-key`). Fingerprinting hanya melindungi `X-API-Key` platform, bukan kunci yang dipasok subscriber. Skema `WebhookResponse` *tidak* mengembalikan field ini (baik), tetapi penyimpanan tetap plaintext.
3. **Auth statis.** `API_KEYS` adalah daftar dipisah-koma yang dibandingkan plaintext (`middleware/auth.py`, default `sharkfin-demo-key-2026`). Memadai untuk prototype; **belum** ada rate limiting, rotasi kunci, atau otorisasi per-scope.
4. **Tanpa migrasi Alembic.** `init_db` memakai `Base.metadata.create_all` (meski `alembic` ada di requirements). Wajar untuk prototype, ditandai untuk produksi.
5. **Deployment single-worker.** Dockerfile menjalankan `uvicorn --reload` (dev, satu proses), sehingga manfaat skalabilitas horizontal lintas-worker via Redis bersifat **laten**, belum dieksekusi.
6. **Collectors butuh kredensial.** Telegram/GitHub/Google Dork/Paste melakukan panggilan eksternal nyata namun memerlukan kredensial yang kosong di `.env.example`, sehingga dengan konfigurasi default collectors *early-return*. Data demo live berasal dari seed — konsisten dengan posisi "prototype + live demo".
7. **`total_records_exposed_estimate`** pada `/stats/summary` adalah heuristik naif (`total_threats × 5`), bukan turunan dari hitungan entitas terdeteksi. Ditandai sebagai **estimasi**.
8. **`raw_content` nullable=False.** Kolom selalu berisi minimal preview ter-mask; pada mode raw, *fallback* laporan intel `mask_sensitive(raw_content)[:200]` tetap menyamarkan — tidak ditemukan jalur kebocoran teks mentah via API.

---

## 6. Daftar Lampiran

Lampiran berlabel berikut dirujuk dari bagian proposal terkait dan dapat diakses panitia:

| # | Lampiran | Tautan / Lokasi | Bagian proposal terkait |
|---|---|---|---|
| 1 | Demo live | https://shark-fin-zeta.vercel.app/ | H2, E4, G6 |
| 2 | Repositori sumber + CI | https://github.com/0xNoramiya/shark-fin | H, E1, E5 |
| 3 | Video demo | *(tautan dilampirkan saat tersedia — estimasi)* | H3 |
| 4 | Workflow CI GitHub Actions | `.github/workflows/backend-tests.yml` | H3, E5 |
| 5 | Bukti 102 tes lulus | Output `pytest` (breakdown 63/16/14/5/4) | H1, E5 |
| 6 | Log perbaikan Tahap 2 | `FIXES.md` + riwayat commit + dokumen ini (`docs/PROGRESS-LOG.md`) | H1 |
| 7 | Diagram Arsitektur Sistem | Blok diagram pada Bagian E.System Architecture proposal | E1 |
| 8 | Screenshot dashboard & landing | `docs/screenshots/dashboard.png`, `docs/screenshots/landing.png` | H3 |
| 9 | Contoh output draft SEOJK 29/2022 Bab IX | Endpoint `GET /api/v1/threats/{id}/report?format=ojk` | H3, D, E6 |
| 10 | Tabel verifikasi statistik (sumber + tahun) | Lampiran proposal (Surfshark, BSSN/OJK, IBM, OJK fraud) | B3 |
| 11 | Worksheet TAM/SAM/SOM (asumsi eksplisit) | Lampiran proposal | G5 |
| 12 | Tabel komparasi kompetitor | Lampiran proposal | E2 |
| 13 | Hasil wawancara/survei pasar | *(dilampirkan saat tersedia — estimasi)* | G4 |

> Butir bertanda "estimasi" (3 dan 13) **belum** tersedia pada saat dokumen ini disusun dan ditandai jujur sebagai rencana lampiran, bukan klaim yang sudah dipenuhi.

---

## 7. Status Akhir

Seluruh perbaikan pada Bagian 3 telah **diverifikasi langsung** terhadap kode sumber dan layanan yang berjalan: suite tes mengembalikan `102 passed`, `/health` melaporkan `database: ok` dan `redis: ok`, serta wiring webhook/audit/dedup tampak persis pada berkas yang dirujuk. SHARK-Fin berstatus **prototype fungsional menuju pilot** — bukan pilot — dengan target uji efektivitas pertama pada pilot Jun–Sep 2026 (estimasi, sesuai roadmap Fase 3).
