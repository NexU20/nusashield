# Dokumentasi Tahap 2 — SHARK-Fin

Paket dokumen ini disusun untuk **2nd Submission Proposal (Digdaya x Hackathon 2026 / PIDI)**, mengikuti template resmi *Panduan Tahap 2* dan menjawab fokus penilaian: **perbaikan problem, validasi pasar, desain solusi, prototype, model bisnis, partnership, dan kesiapan implementasi.**

| Dokumen | Untuk apa | Memetakan ke kriteria juri |
|---|---|---|
| **[PROPOSAL-TAHAP-2.md](PROPOSAL-TAHAP-2.md)** | **Proposal final** — seluruh bagian A–H template resmi, dalam batas kata, Bahasa Indonesia formal | Keenam kriteria |
| [MARKET-VALIDATION.md](MARKET-VALIDATION.md) | TAM/SAM/SOM (metode bottom-up), segmentasi, peta kompetitor, problem–market fit, rencana eksperimen validasi, tabel verifikasi statistik | Market Needs, Business Model |
| [BUSINESS-MODEL-CANVAS.md](BUSINESS-MODEL-CANVAS.md) | Business Model Canvas 9-blok, paket harga 3-tier, unit economics & break-even, asumsi yang perlu divalidasi | Business Model Feasibility |
| [SYSTEM-ARCHITECTURE.md](SYSTEM-ARCHITECTURE.md) | Arsitektur riil (diagram ASCII + mermaid), pipeline end-to-end, postur keamanan/kepatuhan, keterbatasan yang diakui | Technical Quality |
| [PITCH-DECK-OUTLINE.md](PITCH-DECK-OUTLINE.md) | Kerangka pitch deck 13 slide + catatan pembicara | Presentasi / semua kriteria |
| [PROGRESS-LOG.md](PROGRESS-LOG.md) | Changelog "Progress Since 1st Submission": perubahan stage-2 dengan before/after, koreksi kejujuran, keterbatasan, daftar lampiran | Progress Update |

## Cara membaca

- **Juri bisnis/strategi** → `PROPOSAL-TAHAP-2.md` bagian F–G, lalu `MARKET-VALIDATION.md` + `BUSINESS-MODEL-CANVAS.md`.
- **Juri teknis** → `PROPOSAL-TAHAP-2.md` bagian E, lalu `SYSTEM-ARCHITECTURE.md`, lalu kode di `backend/` & `frontend/`.
- **Demo cepat** → ikuti [Quick Start di README utama](../README.md#quick-start); demo live: https://shark-fin-zeta.vercel.app/.

## Prinsip penyusunan

1. **Tidak ada overclaim.** Setiap klaim teknis diverifikasi terhadap kode (102 tes lulus). Fitur yang belum ada ditandai *roadmap*.
2. **Angka jujur.** Statistik pasar/finansial yang merupakan perkiraan ditandai **`(estimasi)`**; statistik faktual diberi sumber + tahun (lihat REFERENCES di proposal dan tabel verifikasi di `MARKET-VALIDATION.md`). Beberapa angka Tahap-1 dikoreksi setelah verifikasi ulang.
3. **Sumber:** brief asli ada pada PDF di root repo (`Proposal Tahap 1.pdf`, `Panduan Tahap 2.pdf`).
