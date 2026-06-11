#!/usr/bin/env bash
set -euo pipefail

# ── SHARK-Fin Demo Setup ──
# One-command setup for PIDI DIGDAYA x Hackathon 2026 demo

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

echo "============================================"
echo "  SHARK-Fin — Demo Setup"
echo "  Sistem Intelijen Ancaman Siber Keuangan"
echo "============================================"
echo ""

# 1. Create .env from example (safe demo values, no real API keys needed)
if [ ! -f .env ]; then
  echo "[1/5] Membuat file .env dari template..."
  cat > .env << 'ENVEOF'
# SHARK-Fin Demo Configuration (no external API keys needed)
DATABASE_URL=postgresql+asyncpg://siakfin:siakfin@postgres:5432/siakfin
REDIS_URL=redis://redis:6379/0
APP_ENV=development
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:5173"]
ENVEOF
  echo "      .env berhasil dibuat (mode demo, tanpa API key eksternal)"
else
  echo "[1/5] File .env sudah ada, dilewati."
fi

# 2. Build and start all services
echo "[2/5] Menjalankan docker compose up --build -d ..."
docker compose up --build -d 2>&1 | tail -5
echo "      Semua container dimulai."

# 3. Wait for postgres to be healthy
echo "[3/5] Menunggu PostgreSQL siap..."
RETRIES=30
until docker compose exec -T postgres pg_isready -U siakfin -q 2>/dev/null; do
  RETRIES=$((RETRIES - 1))
  if [ "$RETRIES" -le 0 ]; then
    echo "      ERROR: PostgreSQL tidak siap setelah 30 percobaan."
    exit 1
  fi
  sleep 1
done
echo "      PostgreSQL siap."

# 4. Initialize database tables (dev mode — creates tables directly)
echo "[4/5] Inisialisasi tabel database..."
docker compose exec -T backend python -c "
import asyncio
from app.database import init_db
asyncio.run(init_db())
print('      Tabel berhasil dibuat.')
"

# 5. Seed demo data
echo "[5/5] Mengisi data demo (20 ancaman)..."
docker compose exec -T backend python -m scripts.seed_demo

# Install React Query if needed (volume mount may override node_modules)
echo ""
echo "Memastikan dependensi frontend terinstal..."
docker compose exec -T frontend npm install --silent 2>/dev/null || true

echo ""
echo "============================================"
echo "  SHARK-Fin siap!"
echo ""
echo "  Dashboard  : http://localhost:5173"
echo "  API Docs   : http://localhost:8001/docs"
echo "  Health     : http://localhost:8001/health"
echo "============================================"
