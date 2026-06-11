# Business Model Canvas — SHARK-Fin

**Tim 418 — SHARK-Fin (Source Hunting Alert and Risk Knowledge for Financial Intelligence)**
Platform intelijen ancaman OSINT untuk deteksi dini kebocoran data keuangan Indonesia & otomasi pelaporan SEOJK 29/2022.

> **Catatan penggunaan angka.** Seluruh angka pasar, harga, dan finansial dalam dokumen ini adalah **estimasi** kecuali statistik regulasi/otoritas yang diberi sumber eksplisit. Estimasi memakai metode *bottom-up* (jumlah lembaga × harga tier) dengan denominator dari data resmi OJK/BI 2024-2025. Angka pasar konsisten dengan Bagian G Proposal Tahap-2 (`docs/PROPOSAL-TAHAP-2.md`). Klaim teknis dibatasi pada apa yang benar-benar terimplementasi dan teruji (102 tes otomatis lulus; lihat `FIXES.md` dan riwayat commit). SHARK-Fin saat ini berstatus **prototype fungsional menuju pilot** — bukan produk berbayar yang sudah berjalan; efektivitas deteksi *real-world* belum terukur di produksi.

---

## 1. Ringkasan Model Bisnis

SHARK-Fin adalah **SaaS B2B berjenjang (3 tier) ditambah kontrak anchor regulator**. Produk memonitor sumber publik (OSINT) untuk mendeteksi kebocoran data keuangan Indonesia, mengklasifikasi dan memberi skor risiko secara **deterministik (regex + validasi algoritmik, bukan ML)**, lalu menjembatani temuan ke kewajiban kepatuhan (draft notifikasi SEOJK 29/2022, webhook ke SOC, audit-log). Marjin tinggi karena pipeline terotomasi penuh dan deteksi deterministik tidak menanggung biaya GPU/training/inferensi ML.

Strategi masuk pasar adalah **land-and-expand**: menyasar segmen yang diabaikan kompetitor enterprise (BPR & fintech P2P kecil, Tier-3), lalu naik ke bank menengah (Tier-2) dan kontrak regulator (Tier-1). Kemitraan asosiasi (PERBARINDO, AFPI/AFTECH, ASPI) dan jalur anchor-regulator (OJK) menjadi kanal distribusi utama, bukan penjualan satuan.

---

## 2. Business Model Canvas (9 Blok)

### Blok 1 — Customer Segments (Segmen Pelanggan)

Tiga segmen utama, dipetakan ke tiga tier harga:

| Segmen | Profil | Tier | Mengapa membeli |
|--------|--------|------|-----------------|
| **Regulator / quasi-anchor** | OJK, BI, BSSN, PPATK (≈4 lembaga) | Tier-1 (negosiasi) | Visibilitas pengawasan makro (Suptech) atas kebocoran lintas-lembaga; early-warning sistemik di sisi hulu (pra-insiden), melengkapi kerangka CIRT BSSN Reg 1&2/2024 |
| **LJK besar-menengah** | Bank umum BUKU 3-4, bank digital, fintech menengah (estimasi ≈40-50 lembaga relevan) | Tier-2 | Pemangkasan window deteksi, otomasi draft SEOJK 29/2022 Bab IX, integrasi SOC/SIEM via webhook, hindari komponen kerugian *dwell-time* |
| **LJK kecil** | BPR (≈1.356-1.369 per OJK Okt-Des 2024) & fintech P2P/LPBBTI berizin (97 per Des 2024/Jan 2025) | Tier-3 | Proteksi setara enterprise dengan harga terjangkau — segmen yang diabaikan kompetitor enterprise & global; tekanan kepatuhan POJK 12/2024 anti-fraud (seluruh LJK) |

Segmen kecil (BPR/fintech) adalah titik masuk yang sengaja dipilih karena **tidak terlayani**: kompetitor enterprise (Telkomsigma, ITSEC Asia) dan global (Recorded Future, Group-IB, Cyble, CSIRTradar/Prosperita) berharga tinggi dan/atau tidak punya classifier yang memvalidasi format identitas/keuangan Indonesia.

### Blok 2 — Value Propositions (Proposisi Nilai)

Nilai inti yang **tidak dimiliki kompetitor terdekat** (terverifikasi dari peta kompetitor):

1. **Classifier Indonesia-native, deterministik & explainable.** Validasi NIK (tanggal lahir + kode provinsi), checksum NPWP *weighted-sum* mod-10, Luhn + pencocokan 10 tabel BIN bank lokal (BRI, BNI, Mandiri, BCA, BSI, CIMB, Permata, Danamon, Mega, BTN), serta keyword perbankan Bahasa Indonesia. Setiap temuan dapat dijelaskan dan diaudit — kritis bagi konteks regulasi (bukan ML *black-box*). Teruji oleh 63 tes pola.
2. **Jembatan langsung deteksi → kepatuhan.** Draft notifikasi SEOJK 29/2022 Bab IX dan laporan intel internal dihasilkan otomatis (PlainText, Bahasa Indonesia), plus audit-log non-reversibel — mendukung kewajiban lapor awal 24 jam ke OJK.
3. **Privacy-by-design (UU PDP).** Masking dua-lapis + mode hash-only (`STORE_RAW_CONTENT=false` default) + dedup SHA-256; `raw_content` tidak pernah diekspos via API. SHARK-Fin tidak menjadi penampung data bocor.
4. **Integrasi rendah-friksi.** Webhook-native ke SOC/SIEM (payload masked-only, filter `min_severity` per pelanggan), Docker-compose 4-service, mode *degraded* tanpa Redis (graceful no-op).
5. **Harga terjangkau untuk segmen terabaikan** + visi intelijen-bersama lintas-lembaga (analog FS-ISAC; belum ada padanannya di Indonesia — gap nyata).

**Nilai per segmen:**

| Segmen | Proposisi nilai utama |
|--------|----------------------|
| Regulator | Suptech: peta makro paparan sektor keuangan; early-warning sistemik (visi Tahun-2 setelah multi-tenant) |
| LJK besar-menengah | MTTD turun (target <24 jam pada lembaga terpasang — *estimasi*); otomasi kepatuhan; rujukan biaya breach IBM USD 5,9 juta (acuan, bukan jaminan) |
| LJK kecil | Proteksi terjangkau (Tier-3) + draft kepatuhan yang sebelumnya tak terjangkau |

### Blok 3 — Channels (Saluran)

- **Anchor-regulator (OJK):** feed/dashboard pengawasan mendorong adopsi turunan oleh lembaga terawasi.
- **Asosiasi industri:** PERBARINDO (BPR), AFPI/AFTECH (fintech P2P berizin), ASPI (sistem pembayaran) — satu demo asosiasi menjangkau puluhan lembaga sekaligus, menekan *Customer Acquisition Cost*.
- **Webhook-native / integrasi teknis:** daya tarik onboarding cepat ke SOC/SIEM eksisting.
- **Demo publik live** (`https://shark-fin-zeta.vercel.app/`) + repo + CI publik (`https://github.com/0xNoramiya/shark-fin`) sebagai funnel awal dan bukti transparansi.
- **PIDI** sebagai akselerator, jaringan mentor, dan kemungkinan sumber hibah inovasi.

### Blok 4 — Customer Relationships (Hubungan Pelanggan)

- **Self-serve onboarding** via API key + seed demo (20 threat) + dokumentasi OpenAPI (`/docs`, 9 rute) untuk pilot ringan.
- **Pilot terbimbing** (2-3 lembaga, roadmap Jun-Sep 2026) dengan dukungan langsung pendiri.
- **Kontrak berbasis kepatuhan** (Tier-1/Tier-2): hubungan jangka panjang berbasis langganan + SLA + add-on.
- **Transparansi & kepercayaan** untuk mengatasi keraguan terhadap vendor solo: 102 tes lulus, repo + CI publik, rencana advisor compliance (eks-OJK/PPATK).

### Blok 5 — Revenue Streams (Aliran Pendapatan)

1. **Langganan SaaS berjenjang** (lihat tabel paket harga, Bagian 3) — sumber pendapatan utama.
2. **Kontrak anchor regulator** (Tier-1, negosiasi per lembaga).
3. **Add-on:** ekspor laporan kepatuhan, integrasi SOC kustom, feed premium.
4. **Hibah/funding bootstrap** (OJK/PIDI/BI) — *mempercepat runway awal, bukan prasyarat keberlanjutan*. Bukan aliran pendapatan berulang.

### Blok 6 — Key Resources (Sumber Daya Kunci)

- **Aset teknologi (terimplementasi):** pipeline OSINT 4-collector (Telegram, Pastebin/Rentry, GitHub, Google Dork); classifier deterministik tervalidasi; risk scorer 0-100; backend FastAPI + PostgreSQL 16 (authoritative) + Redis 7 (cache opsional); frontend React/Vite; webhook dispatch; audit-log; 102 tes otomatis + CI GitHub Actions.
- **Aset kekayaan intelektual:** logika validasi format identitas/keuangan Indonesia (NIK/NPWP/Luhn-BIN) + template laporan SEOJK 29/2022 Bahasa Indonesia.
- **Sumber data publik legal:** kanal Telegram publik, paste site, GitHub Code Search, Google Custom Search (gratis ~100 query/hari).
- **Sumber daya manusia:** pendiri/solo dev (Muhammad Rifqi Haikal, latar CTF/keamanan siber & blockchain) — *risiko bus-factor diakui*; rencana mitigasi: rekrut data/backend engineer + advisor compliance, mentor PIDI, modularitas codebase untuk onboarding cepat.
- **Aset reputasi:** demo live + transparansi repo/CI sebagai bukti kredibilitas.

### Blok 7 — Key Activities (Aktivitas Kunci)

- Pengembangan & pemeliharaan collectors/classifier/scorer/pipeline.
- Pemeliharaan akurasi deteksi (presisi/recall pada test-set berlabel) dan penambahan sumber/entitas.
- Penyusunan & pembaruan template kepatuhan (SEOJK/OJK) seiring perubahan regulasi.
- Akuisisi & onboarding pelanggan (pilot, integrasi webhook, dukungan).
- Validasi pasar primer (wawancara/survei CISO & IT manager; pengejaran LoI pilot).
- Penguatan keamanan/kepatuhan (roadmap: enkripsi at-rest, RBAC, migrasi Alembic, deployment multi-worker).

### Blok 8 — Key Partnerships (Kemitraan Kunci)

| Partner | Peran |
|---------|-------|
| **OJK** | Anchor regulator + jalur regulasi yang memicu adopsi turunan LJK terawasi |
| **BSSN** | Komplementer kerangka CIRT/krisis siber (Reg 1&2/2024) di sisi hulu (pra-insiden) |
| **PPATK** | Intelijen keuangan |
| **PERBARINDO / AFPI / AFTECH / ASPI** | Kanal distribusi massal ke BPR, fintech P2P, dan penyelenggara sistem pembayaran |
| **PIDI** | Akselerator, mentor, kemungkinan hibah inovasi |
| **Penyedia infra** (hosting, Vercel) + penyedia API sumber data | Operasional teknis; sebagian besar API gratis |

### Blok 9 — Cost Structure (Struktur Biaya)

Struktur biaya ringan; model **value-driven dengan efisiensi biaya tinggi**:

1. **Infrastruktur** — hosting backend/PostgreSQL/Redis + Vercel (saat ini ringan, serverless-friendly).
2. **API sumber data** — sebagian besar gratis (Google CSE ~100 query/hari, Telegram/GitHub publik); HIBP berbayar opsional di luar MVP.
3. **Gaji tim kecil** (pasca-rekrutmen: data/backend engineer + advisor compliance) — *komponen biaya terbesar di masa depan*.
4. **Biaya legal/kepatuhan.**

**Keunggulan ekonomi kunci:** deteksi deterministik (tanpa GPU/training/inferensi ML) → marjin SaaS tinggi, biaya marginal per pelanggan tambahan rendah. Arsitektur multi-tenant ringan berarti menambah pelanggan tidak menambah biaya infra secara signifikan.

---

## 3. Paket Harga 3-Tier

> Semua harga adalah **estimasi** dan akan divalidasi melalui wawancara/survei praktisi (kesediaan-bayar). Rentang konsisten dengan Tahap-1 dan Bagian G Proposal Tahap-2.

| Aspek | **Tier-1 — Regulator** | **Tier-2 — Profesional** | **Tier-3 — Reguler** |
|-------|------------------------|--------------------------|----------------------|
| **Target** | OJK / BI / BSSN / PPATK | Bank umum BUKU 3-4, bank digital, fintech menengah | BPR, fintech P2P/LPBBTI kecil berizin |
| **Harga (estimasi)** | Negosiasi per lembaga; ~Rp 300-500 juta/tahun | Rp 30-75 juta/bulan (~Rp 360-900 juta/tahun) | Rp 5-15 juta/bulan (titik acuan **Rp 8 juta/bulan**; ~Rp 60-180 juta/tahun) |
| **Cakupan** | Feed lintas-lembaga + dashboard pengawasan nasional (visi multi-tenant Tahun-2) | Feed penuh + dashboard analis + webhook SOC + draft SEOJK 29/2022 + audit-log | Feed + dashboard + webhook + draft kepatuhan (skala lembaga tunggal) |
| **Diferensiasi nilai** | Suptech makro, early-warning sistemik | Otomasi kepatuhan + integrasi SOC, hindari *dwell-time* | Proteksi terjangkau yang tak ditawarkan kompetitor enterprise |
| **Add-on** | Integrasi kustom, dukungan prioritas | Ekspor laporan kepatuhan, feed premium, integrasi SOC kustom | Ekspor laporan kepatuhan |

**Catatan harga Tier-3 (justifikasi keterjangkauan).** Untuk BPR, satu insiden kebocoran data nasabah berisiko sanksi UU PDP (hingga 2% pendapatan tahunan) ditambah biaya notifikasi/remediasi — sehingga langganan ~Rp 8 juta/bulan proporsional terhadap eksposur. Harga rendah dimungkinkan karena pipeline terotomasi penuh dan deteksi deterministik tanpa biaya ML.

---

## 4. Unit Economics & Analisis Break-Even

> Semua angka di bagian ini adalah **estimasi** dengan asumsi yang dinyatakan eksplisit (lihat Bagian 5). Tujuannya menunjukkan *struktur* ekonomi, bukan proyeksi pasti.

### 4.1 Asumsi biaya operasional (estimasi)

| Komponen biaya | Estimasi bulanan | Catatan |
|----------------|------------------|---------|
| Infrastruktur (hosting backend + PostgreSQL + Redis + Vercel) | Rp 3-8 juta | Ringan; serverless-friendly; biaya marginal per pelanggan tambahan rendah |
| API sumber data berbayar | ~Rp 0 (MVP) | Google CSE gratis ~100 query/hari; Telegram/GitHub publik; HIBP opsional di luar MVP |
| Biaya operasional non-gaji (domain, legal ringan, tooling) | Rp 2-5 juta | Estimasi prototype |
| **Subtotal biaya tetap non-gaji (estimasi)** | **~Rp 5-13 juta/bulan** | Sebelum rekrutmen tim |
| Gaji tim (pasca-rekrutmen, di luar fase solo) | (belum berlaku di fase MVP) | Komponen biaya terbesar saat scaling |

Karena deteksi bersifat deterministik (tanpa GPU/ML), **biaya layanan per lembaga tambahan jauh di bawah harga tier** — terutama untuk Tier-2. Inilah pilar marjin SaaS yang tinggi.

### 4.2 Analisis break-even

Titik impas dihitung terhadap **biaya tetap non-gaji fase awal** (estimasi Rp 5-13 juta/bulan), konsisten dengan klaim Tahap-1 "break-even pada 8 klien Tier-3 ATAU 2 klien Tier-2".

**Skenario A — 8 klien Tier-3:**

| Item | Nilai (estimasi) |
|------|------------------|
| Harga Tier-3 (titik acuan) | Rp 8 juta/bulan/klien |
| 8 klien Tier-3 → pendapatan bulanan | 8 × Rp 8 juta = **Rp 64 juta/bulan** |
| Pendapatan tahunan (ARR) | ~**Rp 768 juta/tahun** |
| Biaya tetap non-gaji (estimasi) | Rp 5-13 juta/bulan |
| **Marjin kotor sebelum gaji (estimasi)** | **~Rp 51-59 juta/bulan** |

**Skenario B — 2 klien Tier-2:**

| Item | Nilai (estimasi) |
|------|------------------|
| Harga Tier-2 (titik tengah ~Rp 50 juta/bulan) | Rp 50 juta/bulan/klien |
| 2 klien Tier-2 → pendapatan bulanan | 2 × Rp 50 juta = **Rp 100 juta/bulan** |
| Pendapatan tahunan (ARR) | ~**Rp 1,2 miliar/tahun** |
| Biaya tetap non-gaji (estimasi) | Rp 5-13 juta/bulan |
| **Marjin kotor sebelum gaji (estimasi)** | **~Rp 87-95 juta/bulan** |

**Kesimpulan break-even.** Pada skema biaya tetap non-gaji yang ringan, **8 klien Tier-3 atau 2 klien Tier-2** sudah menutup biaya operasional fase awal dengan marjin signifikan. Setelah rekrutmen tim, ambang break-even naik seiring beban gaji; pertumbuhan ARR diharapkan menutupinya (lihat proyeksi).

### 4.3 Proyeksi ARR (estimasi, terbatas kapasitas tim solo)

> Proyeksi mengasumsikan penambahan tim pada Tahun-2/3 untuk menumbuhkan kapasitas delivery seiring permintaan.

| Periode | Komposisi klien (estimasi) | ARR (estimasi) |
|---------|----------------------------|----------------|
| **Tahun-1** | 1 anchor pilot + 2-3 Tier-3 berbayar | ~Rp 0,3-0,6 miliar |
| **Tahun-2** | 2 Tier-2 + 8 Tier-3 | ~Rp 2-2,5 miliar |
| **Tahun-3** | Berkembang seiring penambahan tim | > Rp 2,5 miliar (bergantung kapasitas & konversi) |

Asumsi konversi: siklus pilot→kontrak berbayar 6-9 bulan (mengakui pengadaan LJK lambat); dari 3 pilot diasumsikan 1-2 konversi berbayar.

### 4.4 Konteks pasar (TAM/SAM/SOM, estimasi)

Metode *bottom-up* (jumlah lembaga × harga tier), denominator dari data resmi OJK/BI 2024-2025:

| Tingkat | Nilai (estimasi/tahun) | Basis |
|---------|------------------------|-------|
| **TAM** | ~Rp 350-550 miliar | Seluruh LJK terawasi OJK + regulator: ~105 bank umum, ~1.360 BPR, 97 fintech P2P berizin, ~50 penerbit e-wallet, plus asuransi/multifinance/sekuritas & 3-4 regulator |
| **SAM** | ~Rp 70-100 miliar | Segmen realistis & wajib-patuh siber: (45 bank Tier-2 × Rp 50 jt/bln × 12) + (350 BPR/fintech Tier-3 × Rp 10 jt/bln × 12) + (1 regulator ~Rp 0,4 M) ≈ Rp 70 M/tahun |
| **SOM** | ~Rp 0,3-2,5 miliar (12-24 bulan pasca-pilot) | Konservatif: 1 anchor + 2-3 Tier-3; optimis: 2 Tier-2 + 8 Tier-3 |

---

## 5. Asumsi yang Perlu Divalidasi

Daftar asumsi yang menopang model ini beserta cara validasinya. Memisahkan **estimasi** dari **fakta terverifikasi** secara eksplisit adalah bagian dari integritas proposal Tahap-2.

| # | Asumsi (estimasi) | Mengapa belum pasti | Rencana validasi |
|---|-------------------|---------------------|------------------|
| 1 | **Kesediaan-bayar Tier-3 Rp 5-15 juta/bulan** oleh BPR/fintech kecil | Belum ada wawancara/survei berkualitas yang menetapkan WTP; anggaran TI BPR bervariasi | 5-8 wawancara CISO/Head of IT Security bank BUKU 3-4 & bank digital + 3-5 IT manager BPR/fintech; survei via AFPI/PERBARINDO/ASPI (target 30-50 respons) |
| 2 | **Kesediaan-bayar Tier-2 Rp 30-75 juta/bulan** oleh bank menengah | Pembanding harga kompetitor enterprise tidak transparan | Wawancara + benchmarking penawaran kompetitor saat sales |
| 3 | **Adopsi & target SOM** (8 Tier-3 / 2 Tier-2 dalam 12-24 bulan) | Bergantung siklus pengadaan LJK yang panjang & kapasitas tim solo | 2-3 Letter of Intent (LoI) pilot; jalur hibah OJK/PIDI sebagai sinyal anchor |
| 4 | **Siklus pilot→kontrak 6-9 bulan, konversi 1-2 dari 3 pilot** | Asumsi pengadaan; belum teruji | Jalankan pilot Jun-Sep 2026; ukur durasi & konversi aktual |
| 5 | **Biaya infrastruktur ringan tetap rendah saat scaling** | Saat ini deployment single-worker `--reload` (mode dev); scaling multi-worker via Redis belum diuji | Uji beban + migrasi multi-worker (roadmap); migrasi Alembic dari `create_all` |
| 6 | **Dampak deteksi: window MTTD turun ke <24 jam** pada lembaga terpasang | Efektivitas deteksi *real-world* belum terukur; data demo masih dari seed (20 threat) | Pilot terinstrumentasi (logging MTTD); ukur presisi/recall pada test-set berlabel; baseline IBM (global 2023 ~204 hari / sektor keuangan 2024 ~168 hari identify) |
| 7 | **Penghindaran kerugian (rujukan IBM USD 5,9 juta/breach)** sebagai argumen ROI | IBM 2023 = rata-rata biaya breach sektor keuangan global; **acuan, bukan jaminan** untuk konteks satu lembaga Indonesia | Gunakan sebagai pembanding, bukan klaim hasil; perkuat dengan studi kasus pilot |
| 8 | **Kanal asosiasi (PERBARINDO/AFPI/ASPI) efektif menekan CAC** | Belum ada komitmen kemitraan tertulis | Pendekatan resmi ke asosiasi; ukur jangkauan & respons survei |
| 9 | **Hibah OJK/PIDI/BI tersedia sebagai bootstrap** | Mempercepat, bukan prasyarat; belum diraih | Eksplorasi program hibah inovasi; siapkan proposal |
| 10 | **Demand struktural mengonversi ke pembelian** (regulasi-driven) | Mandat kepatuhan terverifikasi, tetapi niat-beli aktual belum | Pasangkan mandat (SEOJK 29/2022, POJK 11/2022, POJK 12/2024, Reg BSSN 1&2/2024) dengan kuotasi wawancara nyata |

### Catatan koreksi statistik (integritas data)

Beberapa angka yang dikutip pada Tahap-1 dikoreksi pada Tahap-2 dan **tidak boleh** dipakai dalam materi bisnis tanpa penyesuaian:

- "361,8 juta anomali trafik **sektor keuangan** 2023" → **salah atribusi**; 361 juta adalah angka **nasional** (BSSN, Jan-Okt 2023); sektor keuangan hanya **47.729 anomali** sepanjang 2023 (ANTARA).
- "334 fintech berizin OJK" → untuk **P2P lending hanya 97** berizin (Des 2024/Jan 2025); "334" kemungkinan mencakup kategori ITSK/sistem pembayaran lain.
- Statistik agregat "107 juta nasabah perbankan digital" & "e-wallet 180 juta pengguna" → **estimasi tanpa sumber tunggal**; gunakan pembanding spesifik (mobile banking BCA ~31 juta, Mandiri ~27 juta, BNI ~17 juta per 2024) bila perlu.

**Statistik terverifikasi yang aman dipakai sebagai dasar demand:** OJK 2.688 pengaduan external fraud 2024; BSSN 56,1 juta data dari 461 instansi 2024 (3,58% sektor keuangan) atau 7 juta data dari 450+ instansi (Sept 2024); Indonesia peringkat ke-8 dunia jumlah akun bocor (Surfshark, 2020-2024); IBM USD 5,9 juta rata-rata biaya breach sektor keuangan (2023).

---

## 6. Lampiran Pendukung (rujukan silang)

- **Proposal Tahap-2 lengkap:** `docs/PROPOSAL-TAHAP-2.md` (Bagian G — Business Model & Scalability).
- **Log perbaikan teknis:** `FIXES.md` (6 isu kritis Tahap-1 yang diperbaiki).
- **Bukti teknis:** 102 tes otomatis lulus (63 patterns, 16 scorer, 14 API, 5 webhook, 4 audit); CI `.github/workflows/backend-tests.yml`.
- **Demo live:** `https://shark-fin-zeta.vercel.app/` — **catatan:** data demo berasal dari seed (`scripts/seed_demo.py`), bukan deteksi produksi.
- **Repositori:** `https://github.com/0xNoramiya/shark-fin`.
