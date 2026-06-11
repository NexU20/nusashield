# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

SHARK-Fin is an OSINT cyber-threat-intelligence platform that monitors public sources for leaked Indonesian financial data (credit cards, NIK, NPWP, bank accounts, credentials), classifies and risk-scores findings, and helps banks draft OJK breach notifications. Backend = Python/FastAPI; frontend = React/Vite. The product UI and generated reports are in **Bahasa Indonesia** — keep user-facing strings in Indonesian; code, comments, and commits in English.

## Commands

All runtime commands assume Docker (4 services: `postgres`, `redis`, `backend`, `frontend`).

```bash
# Full demo setup from scratch (.env + build + init DB + seed 20 threats)
./scripts/demo_setup.sh

# Manual bring-up
cp .env.example .env && docker compose up -d --build
docker compose exec backend python -m scripts.seed_demo   # seed demo data

# Tests (102 total)
docker compose exec backend pytest -v                                    # all
docker compose exec backend pytest tests/test_patterns.py tests/test_scorer.py -v   # non-DB tests
docker compose exec backend pytest tests/test_api.py tests/test_webhook.py tests/test_audit.py -v  # DB tests (need Postgres)
docker compose exec backend pytest tests/test_patterns.py::test_name -v  # single test

# Tests outside Docker — point at the host-exposed Postgres (port 5433)
export TEST_DATABASE_URL="postgresql+asyncpg://siakfin:siakfin@localhost:5433/siakfin"
cd backend && pytest -v

# Frontend (host)
cd frontend && npm install && npm run dev    # dev server :5173, proxies /api → backend:8000
npm run build                                # build to frontend/dist
```

There is no linter/formatter configured. The frontend has no test suite.

### Ports (host → container)
- Frontend dev `5173`, Backend `8001 → 8000`, Postgres `5433 → 5432`, Redis `6379`.
- API docs at `http://localhost:8001/docs`.

## Architecture

### Collection pipeline (the core data flow)
This is the spine of the system and spans several files. A future change to detection/scoring almost always touches this chain:

```
collectors/*.collect() → yields RawIntel
        ↓  (scheduler._process_intel orchestrates everything below)
cache.seen_recently() Redis fast-path → content_hash() DB dedup → skip if duplicate
        ↓
PatternScanner.scan()  → list[IndonesianFinancialEntity]   (skip if empty)
        ↓
RiskScorer.score()     → RiskScore(score 0-100, severity, factors)
        ↓
mask_sensitive()       → content_preview
        ↓
Threat row persisted (raw_content-or-masked + preview + entities JSON + score)
        ↓
dispatch_webhooks()    → POST to severity-matched subscribers (best-effort)
```

- **Collectors** (`app/collectors/`) all subclass `BaseCollector` and `async`-yield `RawIntel`. Each is registered as an APScheduler interval job in `scheduler.py` (telegram 5m, paste 15m, github 30m, google_dork 1h). A collector with missing credentials logs a warning and returns immediately — it does not error.
- **`scheduler._process_intel`** is where classification, scoring, masking, and persistence are wired together. Start here when tracing how a finding becomes a `Threat`.

### Classifier (`app/classifier/`)
- `patterns.py` — `PatternScanner` runs regex detectors with **algorithmic validation**: Luhn for credit cards, date+province checks for NIK, weighted-sum checksum for NPWP, BIN/account-prefix lookups against `INDONESIAN_BINS`. Detected values are masked at detection time (`_mask_card`, NIK truncation, `***` for CVV/passwords) — the entity's `matched_value` is never the raw value.
  - **NIK/credit-card disambiguation:** a 16-digit number that passes Luhn is treated as a credit card and skipped by the NIK scanner. Keep this ordering in mind when editing either detector.
- `scorer.py` — base weight per entity type × confidence, then volume / freshness / source-credibility multipliers, clamped to 0–100.

### Two separate `Severity` enums — important gotcha
`classifier/scorer.py` and `models/threat.py` each define their own `Severity`. `scheduler.py` maps scorer-severity → model-severity by `.value`. If you add a severity tier, add it in **both** and update the map.

### Data protection model — read before touching storage/responses
- `STORE_RAW_CONTENT` (config, **default `false` = hash-only mode**): when off, `_process_intel` stores only the masked preview in `Threat.raw_content`, so the original text is never persisted (UU PDP Pasal 16). The full text is still used in-memory for classification + dedup. Set `true` only for local debugging / richer demo reports.
- `raw_content` is **never exposed via the API** regardless of the flag — `ThreatResponse` returns only `content_preview` (masked via `mask_sensitive`).
- There are **two** masking layers: `PatternScanner` masks entity values; `mask_sensitive()` (in `models/threat.py`) masks the stored preview / report output. Do not add `raw_content` to any response schema.

### API (`app/api/`, mounted under `/api/v1`)
- `threats.py` — feed list (filters + pagination), detail, status workflow (`NEW → VERIFIED → MITIGATED / FALSE_POSITIVE`).
- `reports.py` — generates the SEOJK 29/2022 OJK draft (`?format=ojk`) and internal intel report (`?format=intel`) as plain text.
- `alerts.py` — webhook subscription CRUD.
- `stats.py` — dashboard aggregates.
- `audit.py` — read the immutable audit trail (auth). `PATCH .../status` and `GET .../report` write entries via `services/audit.py::record_audit`; the actor is a non-reversible SHA-256 fingerprint of the API key, never the key itself.
- **Auth:** write/report/audit endpoints require `X-API-Key` via the `require_api_key` dependency (`middleware/auth.py`), validated against the comma-separated `API_KEYS` setting. Read endpoints (list, detail, stats) are public. The frontend sends the key on *every* request.
- `/health` reports per-dependency status (`database`, `redis`) — not a static OK.

### Webhook dispatch & Redis
- `services/webhook.py::dispatch_webhooks()` **is wired into `_process_intel`** (best-effort, never breaks the pipeline) and filters subscribers by `min_severity`. Payload is masked-only (no raw content).
- `app/cache.py` is an **optional** Redis accelerator (recent-hash dedup set + `/health` ping). Postgres stays authoritative; if Redis is down every cache op is a graceful no-op, so tests/CI run without it.

### Schema management
- **No Alembic migrations** despite `alembic` being in `requirements.txt`. Tables are created at startup via `init_db()` → `Base.metadata.create_all`. New models must be imported in `main.py` (and `tests/conftest.py`) to register on `Base.metadata`. Schema changes take effect only on a fresh DB (drop the `pgdata` volume or alter manually). `conftest.py` cleans `_CLEAN_TABLES` between tests — add new tables there.

### Frontend (`frontend/src/`)
- React 18 + Vite, two routes (`/` Landing, `/dashboard`), both `React.lazy`-loaded. State via `@tanstack/react-query` (30s auto-refresh). Charts via Recharts. Theme via CSS variables + `useTheme` (localStorage).
- API base URL: `VITE_API_URL` or `/api/v1`. Vite manual chunks keep the largest bundle <400 KB.

### Deployment
- **Vercel** (`vercel.json`): builds `frontend/`, SPA rewrite to `index.html`.
- **GitHub Pages** (`.github/workflows/deploy-pages.yml`): builds with `VITE_BASE_URL=/shark-fin/` and copies `index.html → 404.html` for SPA routing. The app reads `import.meta.env.BASE_URL` as the router basename, so both base-path and root deployments work.

## Configuration
Settings load from `.env` via pydantic-settings (`app/config.py`), with `env_ignore_empty=True` so blank `.env` lines (e.g. `TELEGRAM_CHANNELS=`) fall back to defaults instead of failing to parse. Collector credentials (`TELEGRAM_*`, `GITHUB_TOKEN`, `GOOGLE_CSE_*`) are optional — unset ones disable that collector. `TELEGRAM_CHANNELS` is a comma-separated string parsed into a list; `API_KEYS` is comma-separated. `STORE_RAW_CONTENT` (default `false`) toggles hash-only storage. Demo API key: `sharkfin-demo-key-2026`.

## Hackathon context (Stage 2)
This repo is a submission to **Digdaya x Hackathon 2026 (PIDI)**, Problem Statement **PS1 — Cyber Security & Data Protection**. The Stage-2 strategy/proposal deliverables live in `docs/` (see `docs/README.md`): the official-template proposal, business model canvas, market validation, system architecture, pitch outline, and progress log. The source briefs are the root PDFs (`Proposal Tahap 1.pdf`, `Panduan Tahap 2.pdf`). When editing proposal docs: Bahasa Indonesia, respect the template word limits, and never claim a capability the code doesn't have.
