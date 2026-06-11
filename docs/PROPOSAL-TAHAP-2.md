# PROPOSAL TAHAP 2 — SHARK-Fin
**Digdaya x Hackathon 2026 / PIDI**

---

## A. TEAM IDENTITY

### A. Identitas Tim — Team ID, Nama Tim, Judul Proposal
*(tanpa batas kata — bidang identitas; ± 95 kata)*

**Team ID:** (diisi sesuai dashboard PIDI).
**Nama Tim:** 418.
**Ketua Tim:** Muhammad Rifqi Haikal (rhaikal91@gmail.com). **Portofolio:** https://github.com/0xNoramiya.

**Judul Proposal:** SHARK-Fin (Source Hunting Alert and Risk Knowledge for Financial Intelligence) — Platform Intelijen Ancaman OSINT untuk Deteksi Dini Kebocoran Data Keuangan dan Otomasi Pelaporan SEOJK No. 29/SEOJK.03/2022.

**Problem Statement (makro):** Penguatan Ketahanan dan Inovasi Keuangan: Manajemen Risiko. **Sub-Problem primer:** Cyber Security & Data Protection. **Sekunder:** Regtech & Suptech.

**Demo live:** https://shark-fin-zeta.vercel.app/ — **Repositori:** https://github.com/0xNoramiya/shark-fin.

Akronim, sub-problem, dan positioning dipertahankan konsisten dengan Tahap-1; bukan rebrand, melainkan pematangan.

### A. Komposisi Tim
*(batas 120 kata; ± 116 kata)*

Tim 418 adalah satu pengembang independen, Muhammad Rifqi Haikal, dengan 1-3 tahun pengalaman keamanan siber dan blockchain serta aktivitas CTF (analisis pola ancaman, reverse engineering) — relevan langsung dengan threat-intelligence dan OSINT yang menjadi inti SHARK-Fin.

Mitigasi risiko solo (bus-factor) mencakup dua sisi. (a) Teknis: kodebase modular (collectors, classifier, API terpisah) dengan 102 tes otomatis dan CI GitHub Actions yang mempercepat onboarding kontributor. (b) Go-to-market: rencana rekrut 1 backend/data engineer dan 1 advisor compliance (eks-OJK/PPATK) yang sekaligus membuka pintu business development; jalur asosiasi yang menggantikan penjualan satuan; serta keterlibatan mentor PIDI. Modularitas dan cakupan tes menurunkan ketergantungan teknis pada satu orang, sementara advisor dan kanal asosiasi menutup risiko komersial solo-dev.

### A. Executive Summary (WAJIB sebut penajaman)
*(batas 150 kata; ± 149 kata)*

Indonesia berperingkat ke-8 dunia jumlah akun bocor 2020-2024 (Surfshark); BSSN (Sep 2024, diungkap OJK Nov 2024) mencatat 7 juta akun terverifikasi di dark web dari 450+ instansi. Kebocoran besar (BRI Life ~2 juta, BPJS 279 juta) lazim ditemukan peneliti eksternal lebih dulu, sementara SEOJK No. 29/SEOJK.03/2022 mewajibkan notifikasi awal insiden 24 jam. SHARK-Fin menutup celah ini lewat pipeline OSINT tiga-lapis: Collection (4 sumber publik), Intelligence (klasifikasi + risk scoring), Action (draft SEOJK siap-tinjau, webhook ke SOC).

Pemenuhan saat ini: deteksi+klasifikasi+masking dan draft SEOJK adalah LIVE dan teruji; feed pengawasan lintas-lembaga (Suptech) adalah roadmap. Penajaman sejak Tahap-1: (1) klaim "NLP classifier" dikoreksi jujur menjadi deteksi deterministik tervalidasi (Luhn, checksum NPWP, validasi NIK, 10 tabel BIN) yang explainable dan auditable; (2) Redis dedup-cache, audit-log, dan webhook dispatch kini terbukti berjalan (102 tes lulus); (3) masking UU PDP di seluruh API. Sasaran: pilot 2-3 lembaga 2026.

---

## B. PROBLEM ALIGNMENT & REFINEMENT

### B. Problem Statement (Cyber Security & Data Protection + Regtech/Suptech)
*(batas 120 kata; ± 119 kata)*

Problem Statement makro: "Penguatan Ketahanan dan Inovasi Keuangan: Manajemen Risiko". SHARK-Fin memilih sub-problem **Cyber Security & Data Protection** sebagai primer dan **Regtech & Suptech** sebagai sekunder. Lapisan Collection dan Intelligence menjawab Cyber Security & Data Protection: deteksi dini kebocoran data nasabah di sumber publik sebelum dieksploitasi. Lapisan Action menjawab Regtech (draft notifikasi SEOJK No. 29/SEOJK.03/2022 Bab IX siap-tinjau) dan Suptech (dashboard pengawasan lintas-lembaga). Sub-problem primer tetap fokus utama: Collection+Intelligence adalah mayoritas kode terimplementasi (8 tipe entitas, 4 collector, 79 dari 102 tes), sedangkan Regtech/Suptech adalah lapisan Action tipis di atasnya — sehingga irisan kedua sub-problem tidak mengorbankan kedalaman pemenuhan sub-problem primer. Satu pipeline mengubah temuan ancaman siber menjadi keluaran kepatuhan terstruktur, bukan dua produk terpisah.

### B. Primary Sub-Problem Statement
*(batas 120 kata; ± 112 kata)*

Sub-Problem Statement primer yang dipilih adalah **Cyber Security & Data Protection**. Penajaman spesifik SHARK-Fin: lembaga jasa keuangan Indonesia belum memiliki kanal deteksi dini terstruktur dan berbahasa Indonesia atas kebocoran data nasabah di sumber publik (Telegram publik, Pastebin/Rentry, GitHub, hasil Google Dork). Akibatnya kebocoran umumnya baru disadari setelah berbulan-bulan dan kerap pertama kali diungkap peneliti eksternal, bukan lembaga sendiri. Rujukan: rata-rata waktu identifikasi breach sektor keuangan 168 hari (IBM 2024). Jarak waktu ini berbenturan langsung dengan kewajiban notifikasi awal 24 jam (SEOJK No. 29/SEOJK.03/2022) dan 3x24 jam (UU PDP 27/2022). Inti yang SHARK-Fin perpendek: jendela deteksi dari ratusan hari menuju mendekati real-time, sehingga kewajiban pelaporan dapat dipenuhi.

### B. Problem Validation (siapa, situasi, akar, mengapa penting)
*(batas 180 kata; ± 179 kata)*

SIAPA: bank BUKU 3-4 dan bank digital, BPR (~1.360, OJK 2024), fintech P2P/LPBBTI berizin (97, OJK Des 2024/Jan 2025), serta regulator (OJK, BSSN, PPATK). SITUASI: Indonesia peringkat ke-8 dunia jumlah akun bocor 2020-2024 (Surfshark). Catatan: dua angka BSSN beredar dengan basis hitung berbeda — 7 juta akun terverifikasi di dark web dari 450+ instansi per Sep 2024 (OJK mengutip BSSN, Nov 2024) versus 56,1 juta indikator paparan dari 461 instansi sepanjang 2024 (laporan BSSN via Prosperita, Okt 2025; 3,58% sektor keuangan). Kasus historis menegaskan pola: BRI Life ~2 juta nasabah + 463.000 dokumen (2021), BPJS Kesehatan 279 juta (2021), 34,9 juta data paspor dan 337 juta data Dukcapil (2023) semuanya diungkap peneliti eksternal lebih dulu. AKAR MASALAH: tidak ada pemantauan OSINT proaktif berbahasa Indonesia, dan tidak ada otomasi yang menjembatani temuan ke kewajiban regulasi. MENGAPA PENTING: OJK menerima 2.688 pengaduan external fraud sepanjang 2024; rata-rata kerugian breach sektor keuangan USD 5,9 juta (IBM 2023); ditambah risiko sanksi UU PDP dan erosi kepercayaan publik. Setiap angka dirujuk dengan sumber dan tahun (Lampiran: Tabel Verifikasi Statistik).

### B. Problem-Solution Mapping (masalah → fitur → outcome)
*(batas 180 kata; ± 176 kata)*

Pemetaan masalah → fitur → outcome (semua fitur sudah terimplementasi, 102 tes lulus):

(1) Deteksi terlambat (168 hari, IBM 2024) → Collection: 4 collector ber-poll (Telegram 5 mnt, Pastebin/Rentry 15 mnt, GitHub default 30 mnt terkonfigurasi, Google Dork default 1 jam terkonfigurasi) → jendela deteksi turun ke skala menit-jam (estimasi; target divalidasi pada pilot).

(2) Analis kebanjiran false positive → Intelligence: classifier deterministik tervalidasi algoritmik (Luhn untuk kartu kredit, validasi tanggal+kode provinsi NIK, checksum NPWP mod-10 berbobot, plus pencocokan terhadap tabel 10 BIN bank nasional) plus risk scorer 0-100 → temuan terprioritaskan, setiap skor dapat dijelaskan dan diaudit.

(3) Gagal lapor 24 jam (SEOJK 29/2022) → Action: draft notifikasi SEOJK 29/2022 Bab IX siap-tinjau + webhook ke SOC/CSIRT + audit-log → kepatuhan dapat dibuktikan dan tertelusur.

(4) Data sensitif berisiko bocor saat ditangani → mask_sensitive dua-lapis + dedup SHA-256 + mode hash-only → raw_content tidak pernah dikeluarkan via API (data-minimisation UU PDP Pasal 16).

Keunggulan classifier: deterministik, transparan, auditable, dengan false-positive rendah pada entitas ber-checksum — bukan kotak hitam ML.

---

## C. ECOSYSTEM ALIGNMENT

### C. Ecosystem Alignment (stakeholder, regulasi, infrastruktur, batasan)
*(batas 150 kata; ± 146 kata)*

STAKEHOLDER: OJK (pengawas sekaligus penerima laporan/Suptech), BSSN (CIRT Peraturan 1/2024 dan manajemen krisis 2/2024), PPATK, LJK (bank, BPR, fintech), serta CISO/Head of IT Security. REGULASI: UU PDP 27/2022 (berlaku penuh Okt 2024; Lembaga PDP belum operasional hingga awal 2026, draft Perpres masih harmonisasi — peluang positioning pengisi celah), POJK 11/2022 (mitigasi risiko TI), SEOJK No. 29/SEOJK.03/2022 Bab IX (notifikasi 24 jam), POJK 12/2024 (anti-fraud seluruh LJK), serta Peraturan BSSN 1&2/2024. INFRASTRUKTUR: integrasi webhook ke SOC/SIEM eksisting; model intelijen-bersama lintas-lembaga (analog FS-ISAC AS) — saat ini single-tenant, kapabilitas lintas-lembaga adalah roadmap Tahun-2. BATASAN IMPLEMENTASI (jujur): hanya memantau sumber PUBLIK dan legal, bukan akses ilegal dark web; bergantung pada API pihak ketiga dengan rate-limit (Telegram, GitHub, Google CSE); dan wajib data-minimisation (hash + preview tersamar, tanpa plaintext) agar SHARK-Fin sendiri tidak menjadi penampung data bocor. Posisi: pelengkap hulu (pra-insiden) dari kerangka CIRT/krisis BSSN.

---

## D. SOLUTION & IMPACT DEEP DIVE

### D. Solution Approach & Mechanism (input/proses/output/interaksi + penajaman)
*(batas 250 kata; ± 236 kata)*

INPUT. Empat collector OSINT memantau sumber publik secara berkala (APScheduler): kanal Telegram publik (5 menit), Pastebin/Rentry (15 menit), pencarian kode GitHub (default 30 menit, terkonfigurasi), dan Google Dork (default 1 jam, terkonfigurasi). Seluruhnya legal — tanpa akses ilegal dark web.

PROSES (sesuai kode scheduler._process_intel). Setiap konten: (1) dihitung content_hash SHA-256; (2) deduplikasi via fast-path Redis (set sharkfin:seen_hashes, TTL 7 hari) lalu fallback Postgres sebagai sumber kebenaran — graceful degrade bila Redis mati; (3) PatternScanner mendeteksi 8 tipe entitas (kartu kredit, NIK, NPWP, nomor rekening, kredensial, CVV, nama bank, kata kunci perbankan) secara deterministik dengan validasi algoritmik: Luhn, validasi tanggal+kode provinsi NIK, checksum NPWP mod-10 berbobot, dan pencocokan tabel 10 BIN bank nasional; (4) RiskScorer menghitung skor 0-100 = (Σ bobot-dasar × confidence) × volume × kesegaran × kredibilitas sumber, dipetakan ke LOW/MEDIUM/HIGH/CRITICAL; (5) mask_sensitive menyamarkan data sensitif sebelum persist ke Postgres.

OUTPUT. Feed dashboard analis, dispatch webhook ke SOC (terfilter min_severity, payload tersamar), draft notifikasi SEOJK 29/2022 siap-tinjau (bukan submission otomatis ke portal OJK), dan audit-log dengan actor berupa fingerprint SHA-256 kunci API.

INTERAKSI. Analis memverifikasi alur status (NEW→VERIFIED→MITIGATED, ber-audit) dan mengekspor laporan OJK/intel.

PENAJAMAN sejak Tahap-1. Dispatch webhook yang dahulu belum terhubung kini dipanggil langsung di pipeline (terverifikasi 5 tes); Redis dedup-cache dan audit-log yang dahulu sekadar klaim kini terbukti berjalan; classifier dijujurkan sebagai deteksi deterministik tervalidasi, bukan NLP. Seluruh 102 tes lulus.

### D. Impact Scale & Targets (dengan estimasi angka)
*(batas 230 kata; ± 224 kata)*

POPULASI TERDAMPAK. Sektor keuangan Indonesia mencakup ~105 bank umum, ~1.360 BPR, 97 fintech P2P berizin, dan ~50 penerbit e-wallet, melayani puluhan juta pengguna mobile banking (BCA ~31 juta, Mandiri ~27 juta, BNI ~17 juta per 2024) dan e-wallet (QRIS ~48 juta pengguna, BI Q1-2024). Sepanjang 2024, BSSN mencatat 56,1 juta indikator paparan dari 461 instansi (3,58% sektor keuangan) dan OJK menerima 2.688 pengaduan external fraud.

TARGET ADOPSI BERTAHAP (estimasi). Pilot 2-3 lembaga (Jun-Sep 2026) → 15-20 LJK Tier-2/3 pada Tahun-1 → feed pengawasan regulator nasional pada Tahun-2.

DAMPAK TERUKUR (estimasi). Catatan: window <24 jam adalah target rancangan; pada demo live data berasal dari seed karena collector memerlukan kredensial produksi (lihat E5). Validasi MTTD nyata dijadwalkan pada pilot Jun-Sep 2026 dengan instrumentasi waktu-posting vs waktu-deteksi. Komponen biaya breach yang dipengaruhi langsung adalah selisih dwell-time: IBM menunjukkan breach >200 hari jauh lebih mahal daripada <200 hari — selisih itulah yang ditargetkan SHARK-Fin, bukan keseluruhan USD 5,9 juta/breach (acuan IBM 2023, bukan jaminan).

KONTRIBUSI SISTEMIK (estimasi, visi Tahun-2 setelah multi-tenant). Asumsi konservatif: 5 pilot LJK Tier-3 dengan masing-masing ~2 insiden relevan/tahun terdeteksi <24 jam (~10 insiden/tahun, window dipangkas dari ~168 hari). Bila ~30 LJK terhubung, terbentuk early-warning lintas-lembaga ala FS-ISAC — belum ada padanannya di Indonesia. Seluruh angka adopsi/dampak adalah estimasi dengan asumsi yang dinyatakan eksplisit di Bagian G.

### D. Impact Measurement (KPI terukur)
*(batas 270 kata; ± 268 kata)*

KPI disusun berlapis dan dapat diuji, bukan klaim.

(a) DETEKSI. Mean-Time-To-Detect (MTTD): target <24 jam sejak konten dipublikasikan, dibandingkan baseline ~204 hari (IBM 2023 global) / ~168 hari (sektor keuangan IBM 2024). Jumlah temuan tervalidasi per bulan. Presisi classifier: target >90% (estimasi) pada entitas ber-checksum (NIK, NPWP, kartu kredit) yang sifatnya deterministik; diukur memakai test-set berlabel. Recall: target ≥70% pada test-set 200 sampel kebocoran NIK/NPWP/kartu kredit nyata-tersanitasi (bukan hanya sintetis); diakui jujur bahwa data ter-obfuscate berat (mis. NIK dipisah karakter) berada di luar jangkauan deteksi deterministik saat ini dan masuk roadmap enrichment. Angka terukur pertama yang dapat diverifikasi: 63 kasus berlabel positif/negatif di test_patterns.py seluruhnya lulus (presisi 100% pada set berlabel itu), terpisah dari estimasi tahap-pilot.

(b) OPERASIONAL & RESPONS. Persentase temuan yang ditindaklanjuti analis; Mean-Time-To-Acknowledge (NEW→VERIFIED) target <2 jam; Mean-Time-To-Notify (draft SEOJK terkirim) target <12 jam — keduanya dilacak via timestamp audit-log; jumlah draft SEOJK 29/2022 yang dihasilkan <24 jam.

(c) KEPATUHAN & PRIVASI. Traceability 100% — setiap status_update dan report.export tercatat di audit-log (actor = fingerprint SHA-256, terverifikasi non-reversible oleh test_audit). Nol kebocoran raw_content via API, diverifikasi bahwa skema ThreatResponse tidak menyertakan raw_content dan diuji penetrasi berkala.

(d) DAMPAK BISNIS. Jumlah lembaga pilot, tingkat retensi, dan NPS analis.

INSTRUMENTASI. Endpoint /api/v1/stats/summary mengagregasi by_severity, by_source, by_status, institutions_mentioned, dan total_records_exposed_estimate (catatan jujur: estimasi paparan saat ini heuristik sederhana = total×5; pada Tahap-2 akan diperbaiki agar diturunkan dari hitungan entitas terdeteksi). Logging MTTD ditambahkan dengan membandingkan waktu posting sumber dan waktu deteksi.

### D. System & Public Value Proposition (nilai sistemik)
*(batas 200 kata; ± 184 kata)*

Nilai SHARK-Fin melampaui satu lembaga; ia bersifat infrastruktur publik-privat, bukan sekadar produk SaaS.

(1) KETAHANAN SIBER SEKTORAL (roadmap Tahun-2). Model intelijen-bersama lintas-lembaga (analog FS-ISAC AS, belum ada padanannya di Indonesia) akan menciptakan network-effect: satu temuan di sebuah BPR dapat memperingatkan seluruh ekosistem. Saat ini sistem single-tenant; kapabilitas berbagi-intel lintas-lembaga adalah roadmap setelah multi-tenant.

(2) VISIBILITAS PENGAWASAN MAKRO (SUPTECH, roadmap). Feed dan dashboard akan memberi OJK/BSSN gambaran agregat kebocoran data sektor keuangan secara dini — melengkapi kerangka respons pasca-insiden BSSN (Peraturan 1 & 2/2024) di sisi hulu (pra-eksploitasi). Kapabilitas agregasi lintas-lembaga ini menyusul multi-tenant; saat ini single-tenant.

(3) PERLINDUNGAN NASABAH & KEPERCAYAAN PUBLIK. Dengan memperpendek window deteksi dan mendukung notifikasi tepat waktu, SHARK-Fin membantu menjaga kepercayaan publik pada digitalisasi keuangan yang menyentuh puluhan juta nasabah.

(4) PENUTUP CELAH KELEMBAGAAN. Selagi Lembaga PDP UU PDP 27/2022 belum operasional (hingga awal 2026 masih tahap harmonisasi Perpres), SHARK-Fin membantu pengendali data memenuhi kewajiban deteksi dini dan notifikasi (3×24 jam UU PDP; 24 jam SEOJK 29/2022) dengan desain minimisasi data (hanya hash SHA-256 + preview tersamar). Penajaman Tahap-2 mempertegas posisi ini lewat audit-log dan masking yang kini terbukti.

---

## E. TECHNICAL VALIDATION

### E. System Architecture (+ sebut diagram)
*(batas 250 kata; ± 222 kata)*

SHARK-Fin berarsitektur tiga lapis (Collection → Intelligence → Action) dalam satu monorepo yang dijalankan via Docker Compose berisi empat layanan: PostgreSQL 16, Redis 7, backend Python 3.11/FastAPI, dan frontend React 18/Vite 6. PostgreSQL adalah sumber kebenaran (UUID PK, JSONB detected_entities, ARRAY institution_tags) sekaligus otoritas deduplikasi via unique content_hash; Redis 7 berperan sebagai cache jalur-cepat (dedup set, TTL 7 hari) yang OPSIONAL dan terdegradasi anggun (no-op) bila mati. APScheduler (AsyncIOScheduler) menjalankan empat job interval (Telegram 5m, Pastebin/Rentry 15m, GitHub default 30m, Google Dork default 1j).

Alur data (scheduler._process_intel): collector menghasilkan RawIntel → hitung SHA-256 content_hash → cek dedup Redis lalu PostgreSQL → PatternScanner.scan (regex + validasi algoritmik) → RiskScorer.score (0-100) → mask_sensitive → persist baris Threat → dispatch_webhooks ke pelanggan (terfilter min_severity, header X-SHARK-Fin-Key, payload tersamar). Aksi analis (PATCH status, ekspor laporan) tercatat pada audit-log.

API tunggal di /api/v1 mengekspos 9 operasi terverifikasi (threats:3, alerts:3, reports:1, stats:1, audit:1) dengan autentikasi X-API-Key pada seluruh endpoint tulis/ekspor/audit dan baca terbatas; endpoint /health terpisah melaporkan status database dan Redis (total 10 rute OpenAPI). Frontend (Tailwind, Recharts, react-query, axios) ter-deploy di Vercel; backend dikemas Docker (uvicorn). Komunikasi backend berbasis async penuh (SQLAlchemy 2.0 + asyncpg).

Detail visual data flow tiga lapis dan topologi layanan disajikan pada Lampiran — Diagram Arsitektur Sistem (lihat juga blok diagram di bawah).

```
                         SHARK-Fin — Arsitektur Tiga Lapis
 ┌──────────────────────── COLLECTION (sumber PUBLIK/legal) ────────────────────────┐
 │  Telegram(5m)   Pastebin/Rentry(15m)   GitHub(30m*)   Google Dork(1j*)            │
 │      └──────────────┴──────────┬────────────┴──────────────┘   (*terkonfigurasi) │
 └─────────────────────────────────┼─────────────────────────────────────────────────┘
                                    │  RawIntel
                                    ▼
 ┌──────────────────────────── INTELLIGENCE ────────────────────────────────────────┐
 │  SHA-256 content_hash ─► dedup: Redis fast-path ──► Postgres (authoritative)       │
 │  PatternScanner  (Luhn+BIN, NIK, NPWP mod-10, rekening, CVV, kredensial, keyword)  │
 │  RiskScorer 0-100  ─►  mask_sensitive (dua-lapis)                                   │
 └─────────┬───────────────────────────────────────────────────┬─────────────────────┘
           │ persist Threat                                     │
           ▼                                                    ▼
 ┌─── Postgres 16 ───┐   ┌─── Redis 7 (opsional) ───┐   ┌──────────── ACTION ────────────┐
 │ Threat / Audit /  │   │ sharkfin:seen_hashes     │   │ Dashboard analis (X-API-Key)    │
 │ WebhookSub        │◄──┤ TTL 7h, graceful no-op   │   │ Webhook → SOC (min_severity)    │
 └───────────────────┘   └──────────────────────────┘   │ Draft SEOJK siap-tinjau         │
                                                         │ Audit-log (actor=fingerprint)   │
                                                         └─────────────────────────────────┘
        API /api/v1 (9 operasi) + /health   │   Frontend React/Vite @ Vercel
```

### E. Solution Originality
*(batas 300 kata; ± 268 kata)*

SHARK-Fin berdiri di celah yang tidak diisi pemain eksisting. Pembanding lokal terdekat, CSIRTradar (PT Prosperita, diluncurkan Okt 2025), berfokus pada dark web/forum tertutup (Tor) dengan deteksi kredensial generik, tanpa classifier tervalidasi spesifik Indonesia dan tanpa output kepatuhan OJK. Telkomsigma Digital Risk Protection dan ITSEC Asia menyasar segmen enterprise/BUMN berbiaya tinggi dengan integrasi berat — tak terjangkau ~1.360 BPR dan fintech kecil. Pemain global (Recorded Future, Group-IB, Cyble, KELA, CloudSEK, Flashpoint) berharga enterprise dan tidak memahami format identitas/keuangan Indonesia maupun kewajiban SEOJK.

Tiga sumber orisinalitas SHARK-Fin, seluruhnya terkodekan dan teruji:

(1) Classifier Indonesia-native yang deterministik. Tantangan teknis orisinal: membedakan NIK 16-digit dari nomor kartu 16-digit tanpa ML — diselesaikan dengan urutan validasi (Luhn untuk kartu lalu decode tanggal+kode provinsi untuk NIK), menghindari false-cross-classification yang menjadi sumber utama false positive pada tools generik. Ditambah checksum NPWP weighted mod-10, pencocokan tabel 10 BIN bank nasional (INDONESIAN_BINS), deteksi nomor rekening (prefix-to-bank), CVV, kredensial, nama bank, dan kata-kunci perbankan Bahasa Indonesia — total delapan tipe entitas dengan confidence per-entitas. Karena deterministik, setiap temuan dapat dijelaskan dan diaudit (63 tes lulus).

(2) Penjembatan deteksi ke kewajiban regulasi. SHARK-Fin mengisi otomatis draft notifikasi SEOJK 29/2022 Bab IX siap-tinjau dari temuan: dari {NIK, kartu kredit, sumber Telegram} sistem mengisi jenis insiden, kategori data terekspos, estimasi terdampak, waktu deteksi, sumber paparan, dan status — analis melengkapi identitas bank dan elemen naratif lalu menandatangani. Bukan submission otomatis ke portal OJK; pengiriman tetap proses manusia.

(3) Model intelijen-bersama lintas-lembaga (visi Tahun-2) dengan tier terjangkau (Tier-3 estimasi Rp 5-15 juta/bulan) bagi segmen yang diabaikan pasar. Indonesia belum punya padanan FS-ISAC sektor keuangan.

SHARK-Fin memantau hanya sumber PUBLIK/legal — diferensiasi etis sekaligus teknis.

### E. Technological / Method Innovation
*(batas 240 kata; ± 214 kata)*

Inovasi metode SHARK-Fin sengaja dirancang jujur dan dapat diverifikasi, bukan klaim ML black-box.

(1) Deteksi DETERMINISTIK tervalidasi. Inti classifier adalah regex yang dipadukan validasi algoritmik: Luhn untuk kartu kredit plus pencocokan tabel BIN 10 bank nasional, checksum NPWP weighted mod-10, validasi struktur NIK (tanggal lahir + kode provinsi), serta deteksi nomor rekening, CVV, kredensial, dan kata-kunci perbankan Bahasa Indonesia. Pendekatan ini menekan false positive dan, yang lebih penting untuk konteks regulasi, membuat SETIAP temuan dapat dijelaskan dan diaudit langkah demi langkah — keunggulan explainability yang tidak dimiliki model probabilistik.

(2) Risk scoring komposit multi-faktor. Skor 0-100 dihitung sebagai sum(base_weight × confidence) lalu dikalikan pengali volume, freshness, dan kredibilitas sumber, di-clamp ke [0,100], dan dipetakan ke tier LOW/MEDIUM/HIGH/CRITICAL untuk triase terprioritaskan (16 tes lulus).

(3) Privacy-by-design. Masking dua-lapis (mask_sensitive) plus deduplikasi SHA-256 memastikan platform tidak menyimpan maupun mengekspos data mentah; selaras prinsip minimisasi data UU PDP.

(4) Ketahanan operasional. Redis sebagai cache jalur-cepat dedup dengan degradasi anggun bila tidak tersedia, sehingga ketersediaan layanan tidak bergantung pada satu komponen.

Inovasi baru Tahap-2: reposisi determinisme dari keterbatasan menjadi keunggulan ganda — explainability audit-grade untuk regulator DAN nol biaya inferensi ML (tanpa GPU/training). Klaim "NLP classifier" Tahap-1 dikoreksi menjadi deteksi deterministik tervalidasi; koreksi ini bukan penurunan, melainkan reposisi yang tepat — determinisme adalah prasyarat auditabilitas regulasi sekaligus penekan biaya.

### E. Creativity in Implementation (distribusi/monetisasi/onboarding)
*(batas 250 kata; ± 228 kata)*

DISTRIBUSI. SHARK-Fin bersifat webhook-native: dispatch_webhooks (live, terfilter min_severity, header X-SHARK-Fin-Key, timeout 10 detik) memungkinkan integrasi ke SOC/SIEM eksisting tanpa perombakan alur kerja. Demo publik live (shark-fin-zeta.vercel.app) berfungsi sebagai funnel akuisisi. Jalur strategis utama adalah anchor-regulator: feed lintas-lembaga ke OJK/BSSN yang kemudian mendorong adopsi turunan oleh LJK terawasi — distribusi top-down, bukan penjualan satuan. Asosiasi industri (Perbarindo untuk BPR, AFTECH/AFPI untuk fintech) menjadi kanal massal ke segmen kecil.

MONETISASI. SaaS B2B tiga tier + kontrak anchor-regulator: Tier-1 Regulator (negosiasi per lembaga), Tier-2 Profesional (bank BUKU 3-4/fintech menengah), Tier-3 Reguler untuk BPR/fintech kecil (estimasi Rp 8 juta/bulan, rentang Rp 5-15 juta). Strategi land-and-expand menyasar segmen yang diabaikan kompetitor enterprise, lalu naik ke regulator. Hibah inovasi OJK/PIDI/BI dieksplorasi sebagai bootstrap, bukan prasyarat keberlanjutan.

ONBOARDING. Keputusan produk kreatif kunci: pilot zero-friction dalam <1 hari. Friksi adopsi ditekan secara teknis: deploy Docker Compose satu-perintah, API key self-serve, API terdokumentasi (/docs OpenAPI, 9 rute), dan seed demo (scripts/seed_demo.py: 20 threat berbagai severity + 2 pelanggan webhook + entri audit) sehingga pilot dapat langsung melihat data berisi. Mode degradasi tanpa Redis membuat lingkungan pilot ringan tanpa kehilangan fungsi inti.

Unsur kreatif lain: SHA-256-fingerprint-as-audit-actor — akuntabilitas yang menjaga privasi (mencatat siapa bertindak tanpa menyimpan kunci asli). Dua keputusan ini — onboarding instan dan akuntabilitas privasi-pertama — mengubah detail rekayasa menjadi proposisi nilai yang langsung relevan bagi pembeli kepatuhan-sensitif.

### E. Data & Feasibility
*(batas 200 kata; ± 192 kata)*

SUMBER DATA legal dan layak. SHARK-Fin memantau empat sumber PUBLIK: channel Telegram publik, Pastebin/Rentry, GitHub Code Search API, dan Google Custom Search (gratis 100 query/hari). Tidak ada akses ilegal ke dark web; seluruh data berasal dari paparan publik yang dapat diakses sah.

KELAYAKAN TEKNIS TERBUKTI. Prototype berjalan dengan 102 tes otomatis LULUS penuh di CI: 63 patterns, 16 scorer, 14 API, 5 webhook, 4 audit. Dari 102 tes, 79 (patterns+scorer) berjalan tanpa database dan dapat diverifikasi langsung dari kode; 23 (API/webhook/audit) memerlukan PostgreSQL 16 dan dijalankan di container serta di CI GitHub Actions (postgres:16-alpine) pada setiap push/PR ke backend/**. Endpoint /health live mengonfirmasi database dan Redis ok; OpenAPI live mengonfirmasi 9 rute /api/v1.

KETERBATASAN JUJUR. (1) Ketergantungan pada API pihak ketiga dengan rate-limit (mitigasi: exponential backoff sudah ada di collector GitHub; interval poll terkonfigurasi). (2) Dengan konfigurasi default, collector early-return tanpa kredensial (TELEGRAM/GITHUB/GOOGLE), sehingga data demo live berasal dari seed — konsisten dengan posisi "prototype + demo". (3) HIBP berbayar berada di luar MVP. (4) Kualitas data bergantung pada paparan publik.

ROADMAP DATA. Pasca-pilot: kurasi sumber dark-web legal terkurasi dan forum carding, plus pengayaan tipe entitas.

### E. Security & Compliance (UU PDP, akses, enkripsi, penyimpanan)
*(batas 200 kata; ± 195 kata)*

UU PDP 27/2022 (minimisasi data, Pasal 16). raw_content TIDAK PERNAH diekspos via API: skema ThreatResponse hanya mengembalikan content_preview, detected_entities (matched_value sudah tersamar, mis. 405290******0000, user=x pass=***), dan content_hash. mask_sensitive() menyamarkan kartu kredit (keep 4+4), NIK (keep 6+2), dan password/PIN/secret menjadi [TERSEMBUNYI]. Flag STORE_RAW_CONTENT default False (mode hash-only) sehingga kolom raw_content (nullable=False) hanya menerima teks tersamar; teks penuh hanya di-memori untuk klasifikasi/dedup.

KONTROL AKSES. Dependency require_api_key (X-API-Key) melindungi seluruh endpoint tulis/ekspor/audit; endpoint baca terbatas. Diverifikasi via tes 401 (update unauthorized, audit requires api key).

AUDIT & TRACEABILITY. Audit-log mencatat threat.status_update dan report.export; aktor disimpan sebagai prefiks 12-heksadesimal dari SHA-256 kunci API (non-reversibel; roadmap: HMAC ber-salt penuh untuk ketahanan brute-force pada ruang kunci terbatas). Selaras kebutuhan keterlacakan SEOJK 29/2022 dan POJK 11/2022.

PENYIMPANAN. PostgreSQL 16; dedup via SHA-256 content_hash.

ROADMAP (jujur — belum ada): enkripsi at-rest, kebijakan retensi/penghapusan terjadwal, RBAC per-scope dan rotasi kunci (saat ini API_KEYS statis tanpa rate-limit), enkripsi api_key pelanggan webhook (kini plaintext di DB, namun tidak dikembalikan oleh skema respons), serta migrasi Alembic (kini create_all). Item-item ini disiapkan untuk produksi, sejalan kerangka CIRT BSSN 1/2024.

### E. Implementation Readiness MVP (scope 6-12 bln, prioritas, di luar MVP, tim/tech, risiko)
*(batas 300 kata; ± 283 kata)*

SCOPE MVP (6-12 bulan) selaras roadmap: Fase 2 Penguatan (Apr-Jun 2026) lalu Fase 3 Pilot 2-3 lembaga (Jun-Sep 2026, estimasi).

FITUR PRIORITAS — sebagian besar SUDAH terimplementasi dan teruji: empat collector OSINT, classifier delapan tipe entitas tervalidasi (Luhn+BIN, checksum NPWP, validasi NIK), risk scorer 0-100, dashboard analis React, dispatch webhook ke SOC (live), draft SEOJK 29/2022 + laporan intel, audit-log, masking dua-lapis UU PDP, auth X-API-Key. Penguatan Fase-2: stabilisasi collector dengan kredensial produksi, instrumentasi MTTD, dan dataset berlabel untuk mengukur presisi/recall.

DI LUAR MVP: ML/anomaly-detection, sumber dark-web berbayar/HIBP, RBAC penuh, multi-tenant skala regulator, dan aplikasi mobile.

KEBUTUHAN TIM/TECH: rekrut 1 data/backend engineer dan 1 advisor compliance (idealnya berlatar OJK/PPATK) untuk memitigasi bus-factor solo-dev; secara teknis menambahkan enkripsi at-rest, migrasi Alembic (menggantikan Base.metadata.create_all), monitoring/observability, dan deployment multi-worker (kini uvicorn single-worker --reload, mode dev — manfaat penskalaan horizontal via Redis masih laten).

RISIKO TEKNIS & MITIGASI: (1) bus-factor solo-dev — mitigasi: codebase modular + 102 tes otomatis + advisor. (2) Rate-limit/perubahan API sumber — mitigasi: exponential backoff, interval terkonfigurasi, arsitektur collector pluggable. (3) False positive/false negative — mitigasi: validasi algoritmik + uji presisi/recall pada test-set berlabel; data ter-obfuscate berat diakui di luar jangkauan deteksi deterministik saat ini. (4) Beban penyimpanan — mitigasi: mode hash-only + kebijakan retensi (roadmap). (5) Keamanan produksi — API_KEYS statis tanpa rotasi/rate-limit dan tanpa enkripsi at-rest, memadai untuk prototype namun masuk backlog produksi. (6) Catatan integritas: seluruh aksi tulis (threat.status_update, report.export, webhook.register, webhook.delete) kini tercatat di audit-log runtime; keterbatasan tersisa — api_key pelanggan webhook masih plaintext di DB (roadmap: enkripsi).

Kesimpulan: inti MVP fungsional dan teruji; pekerjaan tersisa adalah pengerasan produksi dan validasi pilot, bukan pembangunan dari nol.

---

## F. MARKET VALIDATION

### F. Problem-Market Fit (urgensi + konsekuensi)
*(batas 120 kata; ± 117 kata)*

Pasar ini bersifat must-have, bukan nice-to-have, karena dipaksa regulasi. UU PDP 27/2022 berlaku penuh Oktober 2024 dengan sanksi, sementara Lembaga PDP belum operasional hingga awal 2026 — pengendali data harus melindungi diri sendiri. SEOJK No. 29/SEOJK.03/2022 mewajibkan notifikasi insiden 24 jam, POJK 11/2022 mewajibkan mitigasi risiko TI, dan POJK 12/2024 mewajibkan strategi anti-fraud bagi SELURUH LJK. Urgensi nyata: 7 juta akun terverifikasi dari 450+ lembaga di dark web (OJK mengutip BSSN, Sep/Nov 2024) dan peringkat ke-8 dunia jumlah akun bocor (Surfshark, 2020-2024). Konsekuensi jika tidak diselesaikan: gagal lapor 24 jam (pelanggaran SEOJK 29/2022), kerugian rujukan USD 5,9 juta per breach (IBM 2023, acuan bukan jaminan), erosi kepercayaan publik, dan risiko sistemik.

---

## G. BUSINESS MODEL & SCALABILITY

### G. Value Proposition
*(batas 220 kata; ± 200 kata)*

SHARK-Fin menawarkan nilai berbeda per segmen, dipetakan ke kewajiban regulasi dan angka kerugian.

REGULATOR (OJK/BI/BSSN/PPATK): visibilitas pengawasan makro (Suptech) atas kebocoran data sektor keuangan lintas-lembaga, plus early-warning sistemik yang melengkapi kerangka CIRT BSSN (Reg 1&2/2024) di sisi hulu (pra-insiden) — kapabilitas roadmap Tahun-2 setelah multi-tenant.

LJK BESAR (bank BUKU 3-4, bank digital, fintech menengah): pemangkasan window deteksi dari ratusan hari menuju target <24 jam, otomasi draft notifikasi SEOJK 29/2022 Bab IX siap-tinjau, integrasi webhook langsung ke SOC/SIEM, dan dukungan menghindari komponen kerugian dwell-time dari rujukan USD 5,9 juta per breach (IBM 2023, acuan bukan jaminan).

LJK KECIL (BPR, fintech P2P berizin): proteksi setara enterprise dengan harga terjangkau (Tier-3 estimasi Rp 8 juta/bulan) — segmen yang diabaikan kompetitor enterprise (Telkomsigma, ITSEC Asia) maupun pemain global mahal (Recorded Future, Group-IB, Cyble).

Nilai inti yang tak dimiliki kompetitor terdekat (CSIRTradar/Prosperita): kombinasi (1) classifier Indonesia-native — validasi NIK (tanggal lahir + kode provinsi), checksum NPWP mod-10, Luhn + pencocokan 10 tabel BIN bank lokal, keyword perbankan Bahasa Indonesia; (2) determinisme yang explainable dan auditable — setiap temuan dapat dijelaskan dan diaudit, kritis bagi konteks regulasi (bukan ML black-box); (3) jembatan langsung deteksi ke kewajiban kepatuhan OJK (draft SEOJK siap-tinjau + audit-log). Bukan crawler dark-web, murni OSINT sumber publik legal.

### G. Model Revenue / Funding
*(batas 200 kata; ± 173 kata)*

Model: SaaS B2B berjenjang ditambah anchor regulator. Tier-1 Regulator — kontrak negosiasi per lembaga (estimasi Rp 300-500 juta/tahun), mencakup feed lintas-lembaga + dashboard pengawasan nasional. Tier-2 Profesional — estimasi Rp 30-75 juta/bulan (~Rp 360-900 juta/tahun) untuk bank BUKU 3-4, bank digital, dan fintech menengah. Tier-3 Reguler — estimasi Rp 8 juta/bulan (rentang Rp 5-15 juta; ~Rp 60-180 juta/tahun) untuk BPR dan fintech P2P kecil; harga terjangkau karena pipeline terotomasi penuh dan deteksi deterministik tanpa biaya GPU/ML.

Add-on: ekspor laporan kepatuhan, integrasi SOC kustom, dan feed premium. Funding bootstrap: eksplorasi hibah inovasi OJK/PIDI/BI untuk menutup runway awal — mempercepat, bukan prasyarat.

Asumsi model eksplisit: siklus pilot→kontrak berbayar diasumsikan 6-9 bulan (mengakui pengadaan LJK lambat); dari 3 pilot diasumsikan 1-2 konversi berbayar. Break-even (estimasi) pada 8 klien Tier-3 ATAU 2 klien Tier-2. Proyeksi ARR (estimasi, terbatas kapasitas tim solo): Tahun-1 ~Rp 0,3-0,6 miliar (1 anchor pilot + 2-3 Tier-3 berbayar); Tahun-2 ~Rp 2-2,5 miliar (2 Tier-2 + 8 Tier-3); Tahun-3 berkembang seiring penambahan tim. Asumsi harga & kesediaan-bayar divalidasi via wawancara/survei praktisi (lihat Evidence of Demand).

### G. Cost Structure & Sustainability
*(batas 200 kata; ± 156 kata)*

Struktur biaya ringan. Komponen utama: (1) infrastruktur — hosting backend/PostgreSQL/Redis + Vercel; saat ini ringan dan serverless-friendly; (2) API sumber data — sebagian besar gratis (Google Custom Search ~100 query/hari, Telegram/GitHub publik), HIBP berbayar opsional di luar MVP; (3) gaji tim kecil pasca-rekrutmen (data/backend engineer + advisor compliance); (4) biaya legal/kepatuhan.

Keunggulan ekonomi kunci: deteksi DETERMINISTIK (regex + validasi algoritmik, bukan ML) berarti TIDAK ada biaya GPU/training/inferensi mahal — marjin SaaS tinggi dan biaya marginal per pelanggan tambahan rendah. Pipeline terotomasi penuh (collectors → dedup → classifier → scorer → dispatch) menekan biaya operasional manusia.

Keberlanjutan: arsitektur multi-tenant ringan (PostgreSQL authoritative + Redis cache opsional dengan graceful degradation), sehingga menambah pelanggan tidak menambah biaya infra signifikan. Unit economics (estimasi): biaya layanan per lembaga jauh di bawah harga tier, terutama Tier-2. Skenario dasar (tanpa hibah): break-even pada 8 Tier-3 dengan biaya infra rendah per bulan; hibah PIDI/OJK/BI mempercepat tetapi bukan prasyarat keberlanjutan. Determinisme yang tanpa biaya ML adalah pilar marjin sekaligus pembeda etis/regulasi.

### G. Evidence of Demand
*(batas 220 kata; ± 196 kata)*

Bukti permintaan disajikan sebagai funnel, diperkuat sejak Tahap-1.

(1) Demand struktural regulasi-driven (terverifikasi): SEOJK No. 29/SEOJK.03/2022 (lapor 24 jam), POJK 11/2022 (mitigasi risiko TI), POJK 12/2024 (anti-fraud seluruh LJK, efektif Okt 2024), Reg BSSN 1&2/2024 (CIRT) — menciptakan kewajiban kepatuhan yang membutuhkan kapabilitas early-warning yang belum tersedia terjangkau.

(2) Sinyal pasar makro (terverifikasi): OJK menerima 2.688 pengaduan external fraud sepanjang 2024 (account takeover, phishing, smishing); BSSN mencatat 56,1 juta indikator paparan dari 461 instansi 2024 (3,58% sektor keuangan); rujukan kerugian IBM USD 5,9 juta/breach (acuan bukan jaminan). Untuk BPR, satu insiden kebocoran nasabah berisiko sanksi UU PDP hingga 2% pendapatan tahunan + biaya notifikasi/remediasi — menjadikan Tier-3 Rp 8 juta/bulan proporsional terhadap eksposur.

(3) Validasi kompetitor: peluncuran CSIRTradar (Prosperita, Okt 2025) membuktikan pasar leak-monitoring lokal sedang tumbuh dan tervalidasi komersial; SHARK-Fin berdiferensiasi via OSINT publik + classifier Indonesia + output OJK. Belum ada padanan FS-ISAC sektor keuangan Indonesia — gap nyata.

(4) Validasi primer (rencana Tahap-2, sedang dijalankan; belum ada hasil yang ditandatangani): target 5-8 wawancara CISO/Head of IT Security bank BUKU 3-4 & bank digital + 3-5 IT manager BPR/fintech, survei via asosiasi (AFPI, PERBARINDO, ASPI) untuk mengukur kesediaan-bayar, serta 2-3 Letter of Intent pilot. Hasil kuantitatif (jumlah responden, kutipan, LoI) dilampirkan saat tersedia.

### G. Target Market (tersegmentasi, TAM/SAM/SOM)
*(batas 150 kata; ± 134 kata)*

Pasar tersegmentasi tiga lapis (semua angka estimasi, metode bottom-up: jumlah lembaga × harga tier, denominator dari data resmi OJK/BI 2024-2025).

TAM (estimasi ~Rp 350-550 miliar/tahun): seluruh LJK terawasi OJK + regulator — ~105 bank umum, ~1.360 BPR, 97 fintech P2P berizin, ~50 penerbit e-wallet, plus asuransi/multifinance/sekuritas dan 3-4 regulator.

SAM (estimasi ~Rp 70-100 miliar/tahun): segmen realistis & wajib-patuh siber. Perhitungan inline: (45 bank Tier-2 × Rp 50 jt/bln × 12) + (350 BPR/fintech Tier-3 × Rp 10 jt/bln × 12) + (1 regulator ~Rp 0,4 M) ≈ Rp 70 M/tahun. Filter SAM: dari ~1.360 BPR, ~300-400 disaring berdasarkan aset/kanal-digital aktif yang beranggaran TI memadai untuk Tier-3.

SOM (estimasi ~Rp 0,3-2,5 miliar/tahun, 12-24 bulan pasca-pilot): 1 anchor + 2-3 Tier-3 (konservatif) hingga 2 Tier-2 + 8 Tier-3 (optimis).

### G. Adoption Readiness
*(batas 180 kata; ± 134 kata)*

Kesiapan teknis tinggi, friksi adopsi rendah. Integrasi webhook ke SOC/SIEM eksisting cepat (payload masked-only, header X-SHARK-Fin-Key, filter min_severity per pelanggan — sudah live di pipeline). Deployment Docker-compose 4-service; mode degraded tanpa Redis (graceful no-op) memungkinkan pilot ringan. Tersedia demo publik live, seed demo (20 threat + 2 subscriber), API terdokumentasi (OpenAPI /docs, 9 rute), dan auth X-API-Key.

Hambatan adopsi & mitigasi: (1) prosedur pengadaan LJK lambat (asumsi siklus 6-12 bulan) → jalur hibah OJK/PIDI dan pilot gratis 2-3 lembaga (roadmap Jun-Sep 2026); (2) kekhawatiran data → data-minimization UU PDP (raw_content tidak pernah keluar via API), masking dua-lapis, audit-log; (3) kepercayaan ke vendor solo → transparansi (102 tes otomatis lulus, repo + CI publik), rencana advisor compliance eks-OJK/PPATK, dan modularitas codebase untuk onboarding tim cepat.

Adopsi turunan dipicu jalur anchor-regulator: feed OJK mendorong lembaga terawasi ikut mengadopsi; karena siklus regulator panjang, pendapatan Tahun-1 tidak bergantung pada anchor — jalur Tier-3 via asosiasi didahulukan.

### G. Scalability
*(batas 170 kata; ± 128 kata)*

Skalabilitas teknis: collectors modular (tambah sumber tanpa mengubah pipeline scheduler), pipeline async FastAPI + APScheduler (4 job interval), Redis sebagai cache hot-path dedup (opsional, shared set 7-hari TTL), PostgreSQL authoritative, dan biaya marginal rendah karena deteksi deterministik (tanpa GPU/ML). Arsitektur berbasis Redis memungkinkan scaling horizontal lintas-worker, tetapi BELUM diuji multi-worker — deployment saat ini single-worker --reload (mode dev); dicatat sebagai item roadmap konkret, bukan kapabilitas yang sudah teruji.

Skalabilitas bisnis: network-effect intelijen-bersama — setiap lembaga baru menambah cakupan dan nilai feed bagi seluruh ekosistem (analog FS-ISAC, visi Tahun-2), mendorong strategi land-and-expand dari BPR/fintech kecil menuju anchor regulator.

Roadmap skala (jujur soal batas saat ini): migrasi Base.metadata.create_all → Alembic, deployment multi-worker, multi-tenant penuh, sharding sumber, serta ekspansi entitas dan sumber data. Bukan klaim siap-skala penuh; batas infrastruktur diakui sebagai item roadmap konkret.

### G. Partnership & Distribution
*(batas 170 kata; ± 132 kata)*

Kemitraan adalah strategi go-to-market utama, bukan penjualan satuan.

Key partners: OJK (anchor + jalur regulasi yang memicu adopsi turunan LJK terawasi), BSSN (komplementer kerangka CIRT/krisis siber Reg 1&2/2024, di sisi hulu pra-insiden), PPATK (intelijen keuangan), dan asosiasi industri sebagai kanal distribusi massal — PERBARINDO (menaungi BPR), AFPI/AFTECH (fintech P2P berizin), serta ASPI (sistem pembayaran).

Jalur distribusi: (1) anchor-regulator — feed/dashboard OJK mendorong lembaga terawasi mengadopsi; (2) asosiasi — satu demo Perbarindo menjangkau ~50 BPR sekaligus, menekan biaya akuisisi (CAC) pada siklus pengadaan yang diakui lambat; (3) webhook-native — integrasi cepat ke SOC/SIEM eksisting sebagai daya tarik teknis dan onboarding <1 hari; (4) PIDI sebagai akselerator, jaringan mentor, dan kemungkinan sumber hibah inovasi.

Demo publik live berfungsi sebagai funnel awal yang mengonversi calon pelanggan ke pilot dan langganan berjenjang. Posisi sebagai infrastruktur publik-privat memperkuat daya tawar kemitraan regulator.

---

## H. PROGRESS UPDATE & ATTACHMENT

### H. Progress Since 1st Submission (konkret)
*(batas 150 kata; ± 146 kata)*

Penajaman terverifikasi di repositori (lihat FIXES.md dan riwayat commit):

(1) PROTOTYPE: webhook dispatch ke SOC kini LIVE (dipanggil di scheduler._process_intel, filter min_severity); Redis dedup-cache nyata (set sharkfin:seen_hashes, TTL 7 hari) + /health melaporkan status DB & Redis; audit-log (actor = fingerprint SHA-256 kunci, non-reversibel) terimplementasi dan teruji; bugfix config (env_ignore_empty) agar .env kosong tidak crash; masking dua-lapis UU PDP serta auth X-API-Key aktif; sumber OSINT naik dari 2 ke 4 collector; CI GitHub Actions ditambahkan; suite tes kini 102 tes otomatis lulus (63 patterns, 16 scorer, 14 API, plus penambahan test_webhook 5 dan test_audit 4 dari yang dilaporkan pada Tahap-1).

(2) KEJUJURAN/SOLUSI: "NLP classifier" dikoreksi menjadi deteksi deterministik tervalidasi — explainable dan auditable.

(3) DESAIN: bundle frontend dipecah (<400KB per chunk), UI dirombak, demo live.

(4) BISNIS: TAM/SAM/SOM eksplisit + perhitungan inline ditambahkan; rencana validasi pasar primer (wawancara/survei praktisi) disiapkan.

### H. Current Status (idea/mockup/prototype/pilot + bukti)
*(batas 50 kata; ± 47 kata)*

PROTOTYPE FUNGSIONAL menuju pilot (belum pilot). Bukti: demo live https://shark-fin-zeta.vercel.app/, repositori + CI https://github.com/0xNoramiya/shark-fin, 102 tes lulus, pipeline 4-collector + dashboard + webhook + draft SEOJK berjalan. Demo live memakai seed (20 threat); efektivitas deteksi real-world belum terukur di produksi — pilot Jun-Sep 2026 (estimasi) adalah uji efektivitas pertama.

### H. Attachment (daftar lampiran)
*(batas 150 kata; ± 118 kata)*

Lampiran berlabel dengan tautan yang dapat diakses panitia:

(1) Demo live: https://shark-fin-zeta.vercel.app/.
(2) Repositori + CI GitHub Actions: https://github.com/0xNoramiya/shark-fin.
(3) Diagram Arsitektur Sistem (tiga lapis + topologi layanan — lihat blok diagram pada Bagian E.System Architecture).
(4) Tabel Verifikasi Statistik (setiap angka + sumber + tahun: Surfshark, BSSN/OJK, IBM, OJK fraud).
(5) FIXES.md + riwayat commit penajaman Tahap-2.
(6) Bukti 102 tes lulus (output pytest; breakdown 63/16/14/5/4) dan workflow CI .github/workflows/backend-tests.yml.
(7) Tabel komparasi kompetitor (CSIRTradar/Telkomsigma/ITSEC/global vs SHARK-Fin).
(8) Worksheet TAM/SAM/SOM dengan asumsi (jumlah lembaga × harga tier).
(9) Contoh output draft SEOJK 29/2022 Bab IX siap-tinjau yang dihasilkan sistem.
(10) Screenshot dashboard & landing (docs/screenshots/dashboard.png, landing.png).
(11) Hasil wawancara/survei pasar (dilampirkan saat tersedia).

---

## REFERENCES

Sumber yang dirujuk (Tahap-1 yang dipertahankan + sumber baru terverifikasi Tahap-2). Statistik tanpa rujukan ditandai "estimasi".

1. Surfshark — Global data breach statistics 2020-2024 (Indonesia peringkat ke-8 jumlah akun bocor). https://databoks.katadata.co.id/en/technology-telecommunications/statistics/cc5473708a4f8dc
2. CNBC Indonesia (26 Nov 2024) — OJK (Sophia Wattimena) mengutip laporan BSSN Sep 2024: 7 juta data dari 450+ instansi terekspos di dark web (~3% sektor keuangan). https://www.cnbcindonesia.com/market/20241126154403-17-591286
3. Bisnis.com / Teknologi (9 Okt 2025) — Laporan BSSN via PT Prosperita: 56,1 juta indikator paparan dari 461 instansi sepanjang 2024 (3,58% sektor keuangan); peluncuran CSIRTradar. https://teknologi.bisnis.com/read/20251009/84/1918979
4. Infobank / Media Asuransi (5 Feb 2025) — OJK (Arwan Hasibuan): 2.688 pengaduan external fraud sepanjang 2024. https://infobanknews.com/ojk-beberkan-telah-terima-2-688-aduan-di-sektor-jasa-keuangan-begini-modusnya/
5. IBM — Cost of a Data Breach Report 2023 (sektor keuangan rata-rata USD 5,9 juta; global mean-time-to-identify ~204 hari). https://www.ibm.com/reports/data-breach
6. IBM — Cost of a Data Breach 2024, financial industry (mean-time-to-identify ~168 hari sektor keuangan). https://www.ibm.com/think/insights/cost-of-a-data-breach-2024-financial-industry
7. Detik / Liputan6 (Jul 2021) — Kebocoran BRI Life ~2 juta nasabah + 463.000 dokumen; diungkap @UnderTheBreach. https://inet.detik.com/security/d-5659935
8. Kompas / Tempo (Mei 2021) — Kebocoran BPJS Kesehatan 279 juta data di RaidForums. https://www.kompas.com/tren/read/2021/05/21/125000465
9. Liputan6 / Kompas (Jul 2023) — 34,9 juta data paspor dan 337 juta data Dukcapil bocor; diungkap peneliti eksternal Teguh Aprianto. https://www.liputan6.com/tekno/read/5337926 ; https://www.kompas.id/baca/polhuk/2023/07/17/337-juta-data-dukcapil-diduga-bocor
10. OJK — SEOJK No. 29/SEOJK.03/2022 (Ketahanan & Keamanan Siber bagi Bank Umum; notifikasi awal insiden 24 jam, Bab IX). https://ojk.go.id/id/regulasi/Documents/Pages/Ketahanan-dan-Keamanan-Siber-Bagi-Bank-Umum/RINGKASAN%20SEOJK%2029%20-%2003%20-%202022-1.pdf
11. BPK — UU No. 27/2022 tentang Pelindungan Data Pribadi (Pasal 16 minimisasi data; notifikasi 3×24 jam; Lembaga PDP belum operasional hingga awal 2026). https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022
12. OJK — POJK 11/POJK.03/2022 (Penyelenggaraan Teknologi Informasi oleh Bank Umum). https://ojk.go.id/id/regulasi/Documents/Pages/Penyelenggaraan-Teknologi-Informasi-Oleh-Bank-Umum/POJK%2011%20-%2003%20-%202022.pdf
13. peraturan.go.id — POJK No. 12/2024 (Penerapan Strategi Anti-Fraud bagi seluruh LJK, efektif 31 Okt 2024). https://peraturan.go.id/id/peraturan-ojk-no-12-tahun-2024
14. BPK — Peraturan BSSN No. 1/2024 (Pengelolaan Insiden Siber/CIRT) dan No. 2/2024 (Manajemen Krisis Siber). https://peraturan.bpk.go.id/Details/291240/peraturan-bssn-no-1-tahun-2024 ; https://peraturan.bpk.go.id/Details/291245/peraturan-bssn-no-2-tahun-2024
15. OJK — Direktori Penyelenggara Fintech Lending Berizin (97 fintech P2P/LPBBTI berizin per Jan 2025). https://ojk.go.id/id/kanal/iknb/data-dan-statistik/direktori/fintech/Pages/Penyelenggara-Fintech-Lending-Berizin-di-OJK-per-31-Januari-2025.aspx
16. Bisnis.com Finansial (7 Nov 2024) — Pengguna mobile banking BCA ~31 juta, Mandiri ~27 juta, BNI ~17 juta (estimasi per 2024). https://finansial.bisnis.com/read/20241107/90/1813852
17. Bank Indonesia — Statistik QRIS Q1-2024 (~48 juta pengguna; estimasi). https://www.bi.go.id
18. IndoSec Summit — Lanskap ancaman siber Indonesia (mengutip Surfshark; sumber sekunder). https://indosecsummit.com/the-escalating-cyber-threat-in-indonesia-a-wake-up-call-for-digital-security/
