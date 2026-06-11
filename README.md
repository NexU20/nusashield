# SHARK-Fin

<p align="center">
  <strong>Platform intelijen ancaman siber keuangan berbasis OSINT untuk ekosistem keuangan digital Indonesia</strong>
</p>

---

### Landing Page
![Landing Page](docs/screenshots/landing.png?v=2)

### Dashboard Analis
![Dashboard](docs/screenshots/dashboard.png?v=2)

## Masalah

Menurut data BSSN, Indonesia mengalami lebih dari 400 juta anomali trafik siber pada tahun 2023, dengan sektor keuangan menjadi target utama. OJK mencatat peningkatan 53% kasus kebocoran data nasabah di industri perbankan dan fintech sepanjang 2024-2025. Data kartu kredit, NIK, NPWP, dan kredensial internet banking Indonesia secara rutin diperjualbelikan di kanal Telegram, paste site, dan dark web — seringkali terdeteksi oleh pelaku kejahatan lebih cepat daripada oleh lembaga keuangan itu sendiri.

Saat ini, tidak ada platform terpusat yang secara proaktif memonitor sumber-sumber publik (OSINT) untuk mendeteksi kebocoran data keuangan Indonesia secara real-time. Lembaga keuangan dan regulator (BI, OJK, BSSN) membutuhkan early warning system yang mampu mendeteksi, mengklasifikasi, dan melaporkan ancaman siber keuangan sebelum data yang bocor disalahgunakan secara masif.

## Solusi

SHARK-Fin adalah platform intelijen ancaman siber yang secara otomatis:
1. **Mengumpulkan** data dari 4 sumber publik (Telegram, Pastebin, GitHub Code Search, Google Custom Search)
2. **Mengklasifikasi** konten menggunakan regex pattern khusus Indonesia (kartu kredit dengan validasi Luhn + BIN 30+ bank, NIK dengan validasi tanggal + provinsi, NPWP dengan checksum)
3. **Menilai risiko** dengan scoring engine multi-faktor (0-100) berdasarkan volume, freshness, kredibilitas sumber, dan tipe data
4. **Menyamarkan data** sensitif sebelum penyimpanan sesuai prinsip minimisasi data (UU PDP Pasal 16)
5. **Menyiapkan draft** notifikasi awal mengacu SEOJK 29/SEOJK.03/2022 Bab IX untuk membantu bank memenuhi kewajiban notifikasi 24 jam ke OJK
6. **Mengirim alert** ke webhook subscriber (SOC, CSIRT) berdasarkan filter severity

## Arsitektur

```
                    SUMBER DATA (OSINT)
          +----------+----------+----------+--------------+
          | Telegram | Pastebin |  GitHub  | Google Dork  |
          +----+-----+----+-----+----+-----+------+-------+
               |          |          |            |
               v          v          v            v
         +----------------------------------------------------+
         |              COLLECTOR LAYER                        |
         |  Telethon  |  httpx   |  httpx     |  httpx        |
         |  (channels)|  (paste) |  (code API)|  (CSE API)    |
         +------------------------+---+------------------------+
                                  |
                                  v
         +----------------------------------------------------+
         |           CLASSIFIER + SCORER                       |
         |  Regex Patterns (ID-specific)  |  Risk Scorer       |
         |  - Kartu Kredit (Luhn+BIN)     |  - Base weight     |
         |  - NIK (date+province valid.)  |  - Volume mult     |
         |  - NPWP (checksum)             |  - Freshness mult  |
         |  - Kredensial, CVV, Rekening   |  - Source credib.  |
         |  - Dedup (SHA-256)             |                    |
         +------------------------+---+------------------------+
                                  |
                                  v
         +----------------------------------------------------+
         |  DATA MASKING (mask_sensitive)                       |
         |  CC: 4539 •••• •••• 1234 | NIK: 320101•••••••07    |
         |  Password: [TERSEMBUNYI] | Truncate 200 char        |
         +------------------------+---+------------------------+
                                  |
                                  v
         +----------------------------------------------------+
         |              DATABASE LAYER                         |
         |         PostgreSQL  |  Redis (queue/cache)          |
         +------------------------+---+------------------------+
                                  |
               +------------------+------------------+
               v                                     v
    +--------------------------+         +--------------------------+
    |    REST API (FastAPI)    |         |   Dashboard (React 18)   |
    |  /threats (public)       |<------->|   Landing page           |
    |  /threats/{id} (public)  |         |   ThreatFeed + Detail    |
    |  /threats/{id}/status 🔒 |         |   StatCards + Charts     |
    |  /threats/{id}/report 🔒 |         |   Lazy loading + split   |
    |  /stats/summary          |         |   Dark/Light mode        |
    |  /alerts/webhook/* 🔒    |         +--------------------------+
    +--------------------------+
               |
               v
    +--------------------------+       +--------------------------+
    | Draft Notifikasi OJK     |       | Webhook Dispatch         |
    | (SEOJK 29/2022 Bab IX)   |       | POST to subscriber SOC   |
    +--------------------------+       +--------------------------+

    🔒 = Memerlukan X-API-Key header
```

## Quick Start

```bash
# One-command demo setup
chmod +x scripts/demo_setup.sh
./scripts/demo_setup.sh

# Atau manual:
cp .env.example .env
docker compose up -d --build
docker compose exec backend python -c "import asyncio; from app.database import init_db; asyncio.run(init_db())"
docker compose exec backend python -m scripts.seed_demo
```

Akses:
- **Landing Page**: http://localhost:5173
- **Dashboard**: http://localhost:5173/dashboard
- **API Docs (Swagger)**: http://localhost:8001/docs
- **Health Check**: http://localhost:8001/health

## Authentication

Endpoint yang melakukan perubahan data dilindungi dengan API key. Sertakan header `X-API-Key` pada setiap request ke endpoint yang ditandai 🔒.

```bash
# Default demo key
X-API-Key: sharkfin-demo-key-2026

# Contoh: update status threat
curl -X PATCH http://localhost:8001/api/v1/threats/{id}/status \
     -H "X-API-Key: sharkfin-demo-key-2026" \
     -H "Content-Type: application/json" \
     -d '{"status": "VERIFIED"}'

# Contoh: download draft notifikasi OJK
curl -H "X-API-Key: sharkfin-demo-key-2026" \
     http://localhost:8001/api/v1/threats/{id}/report?format=ojk
```

Konfigurasi key di `.env`:
```
API_KEYS=sharkfin-demo-key-2026,production-key-here
```

## Fitur Utama

- **4 OSINT Collectors Aktif** — Telegram (Telethon), Paste Site (httpx), GitHub Code Search API, Google Custom Search API — semua berjalan otomatis via scheduler
- **Deteksi Data Keuangan Indonesia** — Pattern matching khusus untuk kartu kredit (BIN 30+ bank Indonesia + Luhn), NIK (validasi tanggal + provinsi + gender), NPWP (weighted-sum checksum), nomor rekening (prefix bank), kredensial, CVV
- **Risk Scoring Engine** — Skor 0-100 dengan multiplier volume (>100 record = 1.5x), freshness (<1 jam = 1.3x), dan kredibilitas sumber
- **Data Masking (UU PDP)** — Semua data sensitif disamarkan sebelum penyimpanan. Konten asli tidak pernah disimpan atau dikembalikan via API. Hash SHA-256 untuk verifikasi tanpa ekspos data
- **API Key Authentication** — Endpoint write/report dilindungi `X-API-Key`. Endpoint read (list, detail, stats) tetap publik untuk dashboard
- **Webhook Alert System** — Registrasi webhook subscriber dengan filter severity. Dispatch otomatis ke SOC/CSIRT saat threat terdeteksi
- **Draft Notifikasi OJK** — Generate draft notifikasi awal mengacu SEOJK 29/SEOJK.03/2022 Bab IX, membantu bank memenuhi kewajiban notifikasi 24 jam ke OJK
- **Laporan Intelijen Internal** — Laporan teknis lengkap dengan entity breakdown, confidence, indikator teknis (hash + preview tersamar), dan rekomendasi per tipe data
- **Dashboard Analis** — Interface Bahasa Indonesia dengan filter severity/sumber/status, detail ancaman, entity table, risk factors, dan export laporan
- **Dark/Light Mode** — Toggle tema dengan CSS variable system, persistent via localStorage
- **Status Workflow** — Alur kerja analis: Baru → Terverifikasi → Dimitigasi / Positif Palsu
- **Deduplication** — SHA-256 hash per konten untuk mencegah duplikasi
- **Code Splitting** — Frontend bundle di-split (chunk terbesar <400 KB), lazy loading halaman
- **93 Automated Tests** — Pattern matching, risk scoring, dan API integration tests

## API Endpoints

| Method | Endpoint | Auth | Deskripsi |
|--------|----------|------|-----------|
| GET | `/api/v1/threats` | Publik | Feed ancaman (filter severity, source, status, institution, paginasi) |
| GET | `/api/v1/threats/{id}` | Publik | Detail ancaman (content_preview, entities, risk score) |
| PATCH | `/api/v1/threats/{id}/status` | 🔒 API Key | Update status workflow analis |
| GET | `/api/v1/threats/{id}/report?format=ojk` | 🔒 API Key | Draft notifikasi awal SEOJK 29/2022 Bab IX |
| GET | `/api/v1/threats/{id}/report?format=intel` | 🔒 API Key | Laporan intelijen internal |
| GET | `/api/v1/stats/summary` | Publik | Statistik dashboard (by severity, source, status) |
| POST | `/api/v1/alerts/webhook/register` | 🔒 API Key | Registrasi webhook subscriber |
| GET | `/api/v1/alerts/webhook/subscriptions` | 🔒 API Key | List webhook aktif |
| DELETE | `/api/v1/alerts/webhook/{id}` | 🔒 API Key | Hapus webhook |
| GET | `/health` | Publik | Health check |

## Running Tests

```bash
# Inside Docker (recommended) — semua 93 tests
docker compose exec backend pytest -v

# Non-DB tests saja (79 tests, tanpa PostgreSQL)
docker compose exec backend pytest tests/test_patterns.py tests/test_scorer.py -v

# Outside Docker (perlu PostgreSQL lokal di port 5433)
export TEST_DATABASE_URL="postgresql+asyncpg://siakfin:siakfin@localhost:5433/siakfin"
cd backend && pytest -v
```

## Konfigurasi Collector

Konfigurasi via environment variable di `.env`:

| Variable | Default | Deskripsi |
|----------|---------|-----------|
| `TELEGRAM_API_ID` | — | Telegram API ID dari my.telegram.org |
| `TELEGRAM_API_HASH` | — | Telegram API Hash |
| `TELEGRAM_CHANNELS` | — | Comma-separated channel list |
| `GITHUB_TOKEN` | — | GitHub Personal Access Token (untuk Code Search API) |
| `GITHUB_POLL_INTERVAL` | `1800` | Interval polling GitHub (detik, default 30 menit) |
| `GOOGLE_CSE_API_KEY` | — | Google Custom Search API Key |
| `GOOGLE_CSE_ID` | — | Google Custom Search Engine ID |
| `GOOGLE_DORK_INTERVAL` | `3600` | Interval polling Google Dork (detik, default 1 jam) |
| `API_KEYS` | `sharkfin-demo-key-2026` | Comma-separated API keys yang valid |

Collector yang tidak dikonfigurasi (token/key kosong) akan di-skip dengan warning di log.

## Tech Stack

| Layer | Teknologi | Fungsi |
|-------|-----------|--------|
| Backend | Python 3.11, FastAPI, Uvicorn | REST API, classifier, scoring engine |
| Database | PostgreSQL 16 + asyncpg | Penyimpanan threat intelligence |
| Cache | Redis 7 | Queue dan caching |
| Scheduler | APScheduler | Orchestrasi 4 collector (5m/15m/30m/1h) |
| Collectors | Telethon, httpx | Telegram, Paste Site, GitHub, Google CSE |
| Classifier | Regex + validasi algoritmik | Luhn, NIK date, NPWP checksum, BIN matching |
| Auth | FastAPI Security (APIKeyHeader) | X-API-Key authentication |
| Data Protection | mask_sensitive() | PII masking sebelum storage (UU PDP) |
| Frontend | React 18, Vite, TailwindCSS | Landing page + dashboard analis |
| State | @tanstack/react-query | Server state dengan 30s auto-refresh |
| Visualisasi | Recharts | Bar chart sumber ancaman |
| Container | Docker + Docker Compose | 4 service: postgres, redis, backend, frontend |

## Catatan Legal & Etika

SHARK-Fin **hanya** memonitor sumber-sumber yang dapat diakses secara publik (publicly accessible sources). Platform ini:

- **Tidak** melakukan akses tidak sah ke sistem manapun
- **Tidak** menyimpan konten asli — semua nilai sensitif disamarkan (`mask_sensitive()`) sebelum penyimpanan ke database
- **Tidak** mendistribusikan data yang ditemukan ke pihak ketiga
- **Tidak** mengekspos data sensitif melalui API — response hanya berisi `content_preview` (tersamar)
- Digunakan **hanya** untuk tujuan defensif: melindungi nasabah dan lembaga keuangan
- Sesuai dengan prinsip minimisasi data (UU PDP Pasal 16) dan responsible disclosure
- Hash SHA-256 digunakan untuk verifikasi dan deduplication tanpa mengekspos data asli

---

*SHARK-Fin — Melindungi ekosistem keuangan digital Indonesia melalui intelijen ancaman siber proaktif.*
