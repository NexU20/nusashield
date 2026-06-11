# VALIDASI PASAR — SHARK-Fin

**Tim 418 · Digdaya x Hackathon 2026 / PIDI · Submission Tahap 2**
**SHARK-Fin** (Source Hunting Alert and Risk Knowledge for Financial Intelligence) — Platform Intelijen Ancaman OSINT untuk Deteksi Dini Kebocoran Data Keuangan dan Otomasi Pelaporan SEOJK No. 29/SEOJK.03/2022.

> **Catatan metodologi.** Dokumen ini melengkapi `docs/PROPOSAL-TAHAP-2.md` dengan pendalaman validasi pasar. Setiap angka pasar (ukuran pasar, harga, target adopsi) ditandai **(estimasi)** kecuali angka statistik publik yang diverifikasi terhadap sumber resmi/media yang tercantum di [Bagian 9 — Tabel Verifikasi Statistik](#9-tabel-verifikasi-statistik). Klaim teknis dibatasi pada apa yang benar-benar terimplementasi dan teruji (102 tes otomatis lulus); kapabilitas yang belum ada (mis. lintas-lembaga multi-tenant, deteksi efektivitas real-world) dinyatakan sebagai **roadmap**, bukan kapabilitas saat ini.

---

## 1. Ringkasan Eksekutif Validasi Pasar

SHARK-Fin menyasar celah pasar yang spesifik dan dapat diverifikasi: lembaga jasa keuangan (LJK) Indonesia belum memiliki kanal deteksi dini **terstruktur dan berbahasa Indonesia** atas kebocoran data nasabah di sumber publik (Telegram publik, Pastebin/Rentry, GitHub, hasil Google Dork), padahal kewajiban kepatuhan siber (notifikasi 24 jam SEOJK 29/2022) mengikat dan tren kebocoran nasional meningkat.

- **TAM (estimasi): ~Rp 350–550 miliar/tahun** — seluruh LJK terawasi OJK + e-wallet + regulator, bila semua berlangganan tier relevan.
- **SAM (estimasi): ~Rp 70–100 miliar/tahun** — segmen realistis terjangkau dan wajib-patuh siber (bank KBMI 3–4/digital, BPR menengah-besar, fintech P2P berizin, 1 regulator anchor).
- **SOM (estimasi): ~Rp 0,3–2,5 miliar/tahun** (12–24 bulan pertama pasca-pilot, target konservatif).
- **Problem-market fit:** pasar bersifat **must-have karena dorongan regulasi**, bukan nice-to-have. UU PDP 27/2022 berlaku penuh Okt 2024 sementara Lembaga PDP belum operasional hingga awal 2026 — pengendali data harus melindungi diri sendiri.
- **Bukti permintaan saat ini:** dorongan regulasi struktural + statistik otoritas terverifikasi + validasi komersial kompetitor (peluncuran CSIRTradar, Okt 2025). **Bukti primer (wawancara/survei/LoI) masih dalam tahap eksekusi** dan belum menghasilkan hasil yang ditandatangani — rencana eksperimen validasi dijabarkan di [Bagian 6](#6-rencana-eksperimen-validasi-wawancara-survei-pilot).

---

## 2. Validasi Ukuran Pasar (TAM / SAM / SOM)

### 2.1 Metode

**Pendekatan bottom-up berbasis jumlah lembaga (institution-count × harga tier).** Pendekatan ini lebih kredibel daripada top-down (persentase belanja TI nasional) karena denominator-nya adalah jumlah lembaga yang dapat diverifikasi dari data resmi OJK/BI, dan numerator-nya adalah harga langganan SHARK-Fin yang dinyatakan eksplisit sebagai estimasi.

**Harga tier (estimasi, basis perhitungan):**

| Tier | Segmen | Harga estimasi/bulan | Harga estimasi/tahun |
|---|---|---|---|
| Tier-1 Regulator | OJK / BI / BSSN (kontrak negosiasi per lembaga) | — | Rp 300–500 juta (kontrak) |
| Tier-2 Profesional | Bank KBMI 3–4, bank digital, fintech menengah | Rp 30–75 juta | Rp 360–900 juta |
| Tier-3 Reguler | BPR, fintech P2P kecil | Rp 5–15 juta (titik tengah Rp 8 juta) | Rp 60–180 juta |

**Denominator lembaga (terverifikasi, lihat Bagian 9):**

| Kategori lembaga | Jumlah | Sumber & tanggal |
|---|---|---|
| Bank umum | ~105–107 | OJK, Statistik Perbankan 2023–2024 |
| BPR/BPRS | ~1.369 (Okt 2024), turun dari 1.405 (Des 2023) | OJK; ~20 izin dicabut sepanjang 2024 |
| Fintech P2P lending (LPBBTI) berizin | 97 (per 31 Jan 2025); ~96 pertengahan 2025 | Direktori OJK |
| Penerbit uang elektronik/e-wallet berizin BI | ~50-an | BI (≈49 per 2020, tren naik) — **estimasi** |
| Regulator/quasi-anchor | 4 (OJK, BI, BSSN, PPATK) | — |

> **Catatan klasifikasi.** Istilah "BUKU 3–4" secara formal telah digantikan oleh **KBMI (Kelompok Bank Berdasarkan Modal Inti) 3–4** berdasarkan POJK 12/POJK.03/2021. Dokumen ini memakai "KBMI 3–4" sebagai padanan modern untuk bank bermodal-inti besar yang menjadi target Tier-2.

### 2.2 TAM — Total Addressable Market

**Estimasi ~Rp 350–550 miliar/tahun.** Skenario teoretis di mana seluruh LJK terawasi OJK + regulator berlangganan tier yang relevan.

| Komponen | Jumlah | Harga estimasi/tahun | Subtotal (estimasi) |
|---|---|---|---|
| Bank umum | 105 | Rp 600 juta | ~Rp 63 miliar |
| BPR | 1.360 | Rp 120 juta | ~Rp 163 miliar |
| Fintech P2P berizin | 97 | Rp 200 juta | ~Rp 19 miliar |
| Penerbit e-wallet | 50 | Rp 300 juta | ~Rp 15 miliar |
| Regulator (kontrak besar) | 4 | — | ~Rp 100 miliar |
| **Subtotal subset terverifikasi** | | | **~Rp 360 miliar** |

Bila ditambah seluruh sektor IKNB lain (asuransi, multifinance, sekuritas, dana pensiun) yang juga wajib-patuh POJK 12/2024 anti-fraud, TAM teoretis dapat melampaui **Rp 600 miliar/tahun (estimasi)**. Angka headline TAM dipertahankan konservatif pada rentang Rp 350–550 miliar/tahun.

### 2.3 SAM — Serviceable Addressable Market

**Estimasi ~Rp 70–100 miliar/tahun.** Segmen yang realistis terjangkau secara harga **dan** terikat kewajiban kepatuhan siber (POJK 11/2022, SEOJK 29/2022, POJK 12/2024).

| Komponen | Jumlah disaring | Harga estimasi | Subtotal (estimasi) |
|---|---|---|---|
| Bank KBMI 3–4 + bank digital (Tier-2) | ~45 | Rp 50 juta/bln × 12 | ~Rp 27 miliar |
| BPR menengah-besar + fintech P2P beranggaran TI (Tier-3) | ~350 (dari ~1.450 BPR+fintech) | Rp 10 juta/bln × 12 | ~Rp 42 miliar |
| Regulator anchor | 1 | ~Rp 0,4 miliar | ~Rp 0,4 miliar |
| **Total SAM (estimasi)** | | | **~Rp 70 miliar** (rentang 70–100) |

**Filter SAM yang dinyatakan eksplisit:** dari ~1.369 BPR, hanya ~300–400 yang diasumsikan punya kanal digital aktif dan anggaran TI memadai untuk Tier-3; sisanya (BPR kecil/non-digital, sebagian dalam proses konsolidasi/pencabutan izin) belum menjadi pasar terlayani realistis dalam horizon 1–2 tahun.

### 2.4 SOM — Serviceable Obtainable Market

**Estimasi ~Rp 0,3–2,5 miliar/tahun** dalam 12–24 bulan pertama pasca-pilot (selaras roadmap Fase 3, Jun–Sep 2026).

| Skenario | Komposisi klien | Pendapatan tahunan (estimasi) |
|---|---|---|
| Konservatif (Tahun-1) | 1 anchor/pilot regulator + 2–3 Tier-3 berbayar | ~Rp 0,3–0,6 miliar |
| Optimis (Tahun-2) | 2 Tier-2 + 8 Tier-3 | ~Rp 2–2,5 miliar |

**Break-even (estimasi): 8 klien Tier-3 ATAU 2 klien Tier-2.** SOM dipasang konservatif untuk 12–24 bulan pertama pasca-pilot; pertumbuhan menuju SAM didorong oleh penambahan tim, kanal distribusi asosiasi, dan jalur anchor-regulator.

```
TAM  ~Rp 350–550 M/th   seluruh LJK + e-wallet + regulator
   └─ SAM  ~Rp 70–100 M/th   LJK wajib-patuh & terjangkau tier
        └─ SOM  ~Rp 0,3–2,5 M/th   yang realistis ditangani tim solo (12–24 bln)
```

### 2.5 Sensitivitas & keterbatasan asumsi

- **Asumsi harga belum tervalidasi pasar.** Kesediaan-bayar Tier-3 (Rp 5–15 juta/bln) untuk BPR adalah hipotesis yang harus diuji lewat wawancara/survei (Bagian 6). Jika WTP riil di bawah Rp 5 juta, denominator SAM/SOM perlu dikoreksi turun.
- **Denominator BPR menyusut.** OJK menargetkan konsolidasi BPR ke ~1.000 lembaga sehat; tren ini mengecilkan jumlah lembaga tetapi memperbesar proporsi yang beranggaran TI memadai (kualitas naik).
- **Angka e-wallet & sebagian IKNB bersifat estimasi** tanpa sumber tunggal yang otoritatif; disajikan sebagai pelengkap, bukan basis SOM.

---

## 3. Segmentasi Target Market

Tiga segmen dengan kebutuhan, ukuran, dan jalur akuisisi yang berbeda.

| Segmen | Lembaga representatif | Kebutuhan utama | Tier | Pembatas adopsi |
|---|---|---|---|---|
| **Regulator / Anchor** | OJK, BI, BSSN, PPATK | Visibilitas pengawasan makro (Suptech) atas kebocoran sektor; early-warning sistemik lintas-lembaga | Tier-1 (kontrak negosiasi) | Siklus pengadaan publik panjang; butuh referensi/pilot dulu |
| **LJK Besar** | Bank KBMI 3–4, bank digital, fintech menengah | Pangkas waktu deteksi; otomasi kepatuhan SEOJK 29/2022; integrasi SOC/SIEM via webhook | Tier-2 (Rp 30–75 jt/bln, estimasi) | Sudah punya tim SOC; harus tunjukkan diferensiasi vs vendor enterprise |
| **LJK Kecil** | BPR, fintech P2P kecil berizin | Proteksi setara enterprise dengan harga terjangkau; kepatuhan minimal-friksi | Tier-3 (Rp 5–15 jt/bln, estimasi) | Anggaran TI terbatas; literasi siber rendah; sensitif harga |

**Prioritas go-to-market (estimasi strategi):** LJK Kecil (Tier-3) didahulukan melalui **kanal asosiasi** (PERBARINDO untuk BPR, AFPI/AFTECH untuk fintech) karena (a) segmen ini paling diabaikan kompetitor enterprise, (b) satu demo asosiasi menjangkau puluhan lembaga sekaligus sehingga menekan biaya akuisisi, dan (c) tidak bergantung pada siklus pengadaan regulator yang panjang. Jalur **anchor-regulator** (top-down: feed OJK mendorong adopsi turunan LJK terawasi) dikembangkan paralel sebagai pengganda jangka menengah, bukan sumber pendapatan Tahun-1.

---

## 4. Peta Kompetitor

### 4.1 Tabel komparasi

Legenda: ✔ ada · ✘ tidak ada · ◐ sebagian/terbatas.

| Pemain | Kategori | Sumber OSINT publik ID (Telegram/Paste/GitHub/Dork) | Classifier tervalidasi Indonesia (NIK/NPWP/Luhn-BIN) | Output kepatuhan SEOJK 29/2022 | Sasaran BPR/fintech kecil | Harga |
|---|---|---|---|---|---|---|
| **SHARK-Fin** | OSINT + Regtech (lokal) | ✔ (4 collector publik) | ✔ (NIK tgl+provinsi, NPWP mod-10, Luhn + 10 BIN) | ✔ (draft SEOJK siap-tinjau) | ✔ (Tier-3 terjangkau) | Berjenjang, terjangkau |
| **CSIRTradar** (PT Prosperita) | Dark-web/leak monitoring (lokal) | ◐ (fokus dark web/Tor, bukan OSINT publik) | ✘ (deteksi kredensial generik) | ✘ | ✘ | n/a publik |
| **Telkomsigma DRP** (grup Telkom/BUMN) | Digital Risk Protection + anti-fraud (lokal) | ◐ (brand/infrastruktur, bukan classifier kebocoran ID) | ✘ | ✘ | ✘ (enterprise/BUMN) | Tinggi |
| **ITSEC Asia** (Tbk) | MSSP/SOC/threat-intel (APAC) | ◐ (feed global + intel lokal) | ✘ | ✘ | ✘ (enterprise) | Tinggi (jasa) |
| **Recorded Future** | DRP/threat-intel (global) | ◐ (dark web + surface global) | ✘ (tanpa format NIK/NPWP/BIN) | ✘ | ✘ | Sangat tinggi |
| **Group-IB DRP** | DRP/anti-fraud (global) | ◐ | ✘ | ✘ | ✘ | Enterprise |
| **Cyble** | Cyber-intel/DRP (global) | ◐ | ✘ | ✘ | ✘ | Enterprise |
| **KELA / CloudSEK / Flashpoint** | DRP/threat-intel (global) | ◐ | ✘ | ✘ | ✘ | Enterprise |

### 4.2 Analisis posisi

- **Kompetitor terdekat & terbaru: CSIRTradar (PT Prosperita, diluncurkan 9 Okt 2025).** Keberadaannya **memvalidasi pasar leak-monitoring lokal** sekaligus mendefinisikan diferensiasi SHARK-Fin: CSIRTradar berfokus dark web/forum tertutup (Tor) dengan deteksi kredensial generik, sedangkan SHARK-Fin memantau **sumber publik OSINT** dengan **classifier tervalidasi spesifik Indonesia** dan **output kepatuhan OJK**. Keduanya komplementer, bukan substitusi penuh.
- **Pemain enterprise lokal (Telkomsigma, ITSEC Asia)** berorientasi integrasi berat & harga tinggi — tidak terjangkau ~1.369 BPR dan fintech kecil. Ini adalah **segmen kosong** (white space) yang dibidik Tier-3.
- **Pemain global (Recorded Future, Group-IB, Cyble, KELA, CloudSEK, Flashpoint)** kuat secara teknologi tetapi tidak memahami format identitas/keuangan Indonesia (NIK/NPWP/BIN bank nasional), tidak menghasilkan draft notifikasi SEOJK, dan tidak menyasar pasar domestik kecil.
- **Gap struktural pasar:** Indonesia **belum memiliki padanan FS-ISAC** (financial-sector ISAC AS) — wadah intelijen-bersama lintas-lembaga sektor keuangan. SHARK-Fin memposisikan model lintas-lembaga sebagai visi roadmap Tahun-2 (saat ini single-tenant), menutup celah kelembagaan ini.

### 4.3 Moat yang dapat diuji (bukan klaim AI)

Diferensiasi SHARK-Fin bertumpu pada apa yang **benar-benar dikodekan dan teruji**, bukan klaim ML:

1. **Classifier Indonesia-native deterministik** — urutan validasi (Luhn untuk kartu, lalu decode tanggal+kode provinsi untuk NIK) menghindari salah-klasifikasi NIK 16-digit vs kartu 16-digit; checksum NPWP weighted mod-10; pencocokan 10 tabel BIN bank nasional (`INDONESIAN_BINS`); 8 tipe entitas dengan confidence per-entitas. **Terverifikasi: 63 tes lulus** di `test_patterns.py`.
2. **Jembatan deteksi → kewajiban regulasi** — satu-satunya yang menghasilkan draft SEOJK 29/2022 siap-tinjau + audit-log immutable. Tidak dimiliki kompetitor mana pun.
3. **Determinisme yang explainable & auditable** — setiap temuan dapat dijelaskan dan diaudit (kritis untuk konteks regulator), tanpa biaya GPU/ML.

---

## 5. Problem-Market Fit

### 5.1 Masalah yang divalidasi (terverifikasi)

| Dimensi | Bukti terverifikasi |
|---|---|
| **Skala paparan nasional** | Indonesia peringkat ke-8 dunia jumlah akun bocor 2020–2024 (Surfshark). BSSN: 7 juta akun terverifikasi di dark web dari 450+ instansi (Sep 2024, diungkap OJK Nov 2024); 56,1 juta indikator paparan dari 461 instansi sepanjang 2024 (laporan BSSN via Prosperita, Okt 2025; 3,58% sektor keuangan). |
| **Pola "ditemukan eksternal lebih dulu"** | BRI Life ~2 juta nasabah + 463.000 dokumen (2021, diungkap @UnderTheBreach); BPJS Kesehatan 279 juta (2021, RaidForums); 34,9 juta data paspor & 337 juta data Dukcapil (2023, diungkap Teguh Aprianto). Lembaga/regulator kalah cepat dari peneliti eksternal — persis masalah yang dipecahkan SHARK-Fin. |
| **Window deteksi vs kewajiban lapor** | Rata-rata waktu identifikasi breach: ~204 hari global (IBM 2023) / ~168 hari sektor keuangan (IBM 2024). Berbenturan langsung dengan kewajiban notifikasi awal 24 jam (SEOJK 29/2022) dan 3×24 jam (UU PDP 27/2022). |
| **Volume fraud nyata** | OJK menerima 2.688 pengaduan external fraud sepanjang 2024 (account takeover, phishing, smishing). |
| **Biaya konsekuensi** | Rata-rata kerugian breach sektor keuangan USD 5,9 juta (IBM 2023; acuan rujukan, bukan jaminan). |

### 5.2 Urgensi: mengapa ini "must-have", bukan "nice-to-have"

Pasar ini bersifat **must-have karena dipaksa regulasi**:

- **UU PDP 27/2022** berlaku penuh Okt 2024 dengan sanksi, sementara **Lembaga PDP belum operasional hingga awal 2026** (draft Perpres masih harmonisasi) — pengendali data harus melindungi diri sendiri tanpa menunggu otoritas pengawas data terbentuk.
- **SEOJK 29/2022** mewajibkan notifikasi insiden 24 jam + laporan rinci 5 hari kerja.
- **POJK 11/2022** mewajibkan mitigasi risiko TI termasuk risiko kebocoran data.
- **POJK 12/2024** mewajibkan strategi anti-fraud bagi **SELURUH LJK** (bukan hanya bank) — efektif 31 Okt 2024, memperluas basis pelanggan wajib-patuh.
- **Peraturan BSSN 1 & 2/2024** mengatur respons/krisis (pasca-insiden); tidak ada mandat pemantauan **proaktif pra-eksploitasi** — celah yang diisi SHARK-Fin di sisi hulu.

**Konsekuensi bila masalah tidak diselesaikan:** gagal lapor 24 jam (pelanggaran SEOJK 29/2022 → sanksi & reputasi), kerugian rujukan USD 5,9 juta/breach, erosi kepercayaan publik, dan risiko sistemik di sektor yang melayani puluhan juta pengguna mobile/internet banking dan e-wallet.

### 5.3 Kecocokan solusi → masalah

| Masalah terukur | Fitur SHARK-Fin (terimplementasi) | Outcome (target/estimasi) |
|---|---|---|
| Deteksi terlambat ~168–204 hari | Collection poll 5–60 mnt (4 sumber publik) + Intelligence + dispatch | Window deteksi → mendekati real-time (target <24 jam) |
| False positive membanjiri analis | Classifier deterministik (Luhn, NPWP mod-10, validasi NIK, 10 BIN) + risk scorer 0–100 | Triase terprioritaskan; false-positive rendah pada entitas ber-checksum |
| Gagal lapor 24 jam | Draft SEOJK 29/2022 siap-tinjau + audit-log immutable | Kepatuhan terbukti & tertelusur |
| Data sensitif bocor saat ditangani | mask_sensitive() dua-lapis + STORE_RAW_CONTENT hash-only + dedup SHA-256 | Tidak ada raw data via API (selaras minimisasi data UU PDP) |

---

## 6. Evidence-of-Demand & Rencana Eksperimen Validasi

### 6.1 Bukti permintaan yang sudah ada

Disajikan sebagai **funnel bukti** dari yang terkuat-terverifikasi ke yang masih rencana:

1. **Demand struktural regulasi (terverifikasi, terkuat).** SEOJK 29/2022, POJK 11/2022, POJK 12/2024, UU PDP 27/2022 menciptakan kewajiban kepatuhan yang membutuhkan kapabilitas early-warning yang belum tersedia secara terjangkau. Ini adalah demand yang tidak bergantung pada sentimen pembeli individu.
2. **Sinyal pasar makro (terverifikasi).** 2.688 pengaduan external fraud OJK (2024); 56,1 juta indikator paparan dari 461 instansi (BSSN 2024); rujukan kerugian USD 5,9 juta/breach (IBM 2023). Untuk satu BPR, eksposur sanksi UU PDP (hingga 2% pendapatan tahunan) + biaya notifikasi/remediasi menjadikan langganan Tier-3 (estimasi Rp 8 juta/bln) proporsional terhadap risiko.
3. **Validasi komersial kompetitor (terverifikasi).** Peluncuran CSIRTradar (Prosperita, Okt 2025) membuktikan pasar leak-monitoring lokal sedang tumbuh dan tervalidasi komersial. SHARK-Fin berdiferensiasi via OSINT publik + classifier Indonesia + output OJK.
4. **Analog pasar (terverifikasi sebagai gap).** Belum ada padanan FS-ISAC sektor keuangan Indonesia — gap kelembagaan nyata yang dibidik visi lintas-lembaga.
5. **Bukti primer (RENCANA, sedang dijalankan, belum ada hasil ditandatangani).** Wawancara, survei, dan Letter of Intent pilot — dijabarkan di 6.2.

> **Pernyataan jujur.** Pada saat submission ini, **belum ada wawancara/survei selesai dengan hasil yang dapat dikutip, dan belum ada LoI yang ditandatangani.** Klaim demand saat ini bertumpu pada demand struktural + statistik otoritas + validasi kompetitor, bukan pada riset primer yang sudah terkumpul. Rencana di bawah adalah komitmen eksekusi, bukan hasil.

### 6.2 Rencana eksperimen validasi

Dirancang realistis untuk kapasitas tim solo, diprioritaskan menurut nilai pembuktian.

| # | Eksperimen | Target sampel | Hipotesis yang diuji | Metrik keberhasilan | Output |
|---|---|---|---|---|---|
| E1 | **Wawancara semi-terstruktur** CISO/Head of IT Security | 5–8 bank KBMI 3–4 & bank digital | Apakah mereka sudah punya monitoring sumber publik/Telegram? Berapa anggaran threat-intel? | ≥60% menyatakan tidak punya kanal OSINT proaktif | Kutipan & profil kebutuhan (Tier-2) |
| E2 | **Wawancara** IT manager BPR menengah & fintech P2P | 3–5 lembaga | Kesediaan bayar Rp 5–15 jt/bln (Tier-3)? Hambatan adopsi? | ≥40% menyatakan WTP dalam rentang Tier-3 | Validasi/koreksi asumsi harga SAM/SOM |
| E3 | **Survei kuantitatif** via asosiasi | 30–50 respons (AFPI ~96–97 fintech; PERBARINDO BPR; ASPI sistem pembayaran) | Kuantifikasi willingness-to-pay & kanal ancaman yang dirasakan | ≥30 respons valid; distribusi WTP terukur | Worksheet WTP + prioritisasi kanal ancaman |
| E4 | **Letter of Intent / komitmen pilot** | 2–3 lembaga (selaras Fase 3) | Apakah ada lembaga bersedia menjadi pilot? | ≥2 LoI atau percakapan pilot serius | LoI/komitmen (bukti demand terkuat) |
| E5 | **Eksplorasi hibah/anchor** | OJK/PIDI/BI | Minat anchor regulator/akselerator | 1 jalur hibah/anchor teridentifikasi | Bukti minat anchor + runway bootstrap |
| E6 | **Telemetri demo publik** | Trafik demo live | Apakah ada minat organik? | Sesi & uji fitur terukur | Sinyal funnel akuisisi |

**Urutan eksekusi:** E1–E3 (kuantifikasi kebutuhan & WTP) → E4 (konversi minat menjadi komitmen pilot) → E5–E6 (paralel). Hasil kuantitatif (jumlah responden, % WTP, kutipan anonim, LoI) akan dilampirkan ke proposal saat tersedia, menggantikan asumsi demand dengan bukti primer.

---

## 7. Adoption Readiness & Hambatan

### 7.1 Kesiapan adopsi (faktor pendukung — terverifikasi teknis)

| Faktor | Status | Dampak adopsi |
|---|---|---|
| **Integrasi webhook-native** | `dispatch_webhooks` live (filter min_severity, header X-SHARK-Fin-Key, timeout 10s) | Integrasi ke SOC/SIEM eksisting tanpa perombakan alur (onboarding <1 hari, estimasi) |
| **Deployment Docker-compose** | 4-service, satu perintah | Pilot ringan, mudah dijalankan |
| **Mode degraded tanpa Redis** | Redis opsional, graceful no-op; Postgres tetap authoritative | Pilot tidak butuh infra penuh |
| **Demo publik live + seed** | shark-fin-zeta.vercel.app, seed 20 threat | Funnel akuisisi & bukti fungsional |
| **API terdokumentasi** | OpenAPI `/docs`, 10 rute terverifikasi | Evaluasi teknis cepat oleh calon klien |
| **Bukti kelayakan** | 102 tes otomatis lulus + CI GitHub Actions | Mengurangi keraguan teknis & bus-factor |

### 7.2 Hambatan adopsi & mitigasi

| Hambatan | Tingkat | Mitigasi |
|---|---|---|
| **Siklus pengadaan LJK/regulator lambat** | Tinggi | Jalur asosiasi (akuisisi massal), pilot gratis, eksplorasi hibah OJK/PIDI; pendapatan Tahun-1 tidak digantungkan pada anchor regulator |
| **Kepercayaan ke vendor solo (bus-factor)** | Tinggi | Transparansi open (repo + CI publik), 102 tes, rencana advisor compliance (eks-OJK/PPATK) + rekrut engineer; modularitas codebase |
| **Kekhawatiran "platform jadi penampung data bocor"** | Tinggi | Data-minimisation by design: hash-only mode, masking dua-lapis, raw_content tidak pernah diekspos via API; audit-log; selaras UU PDP Pasal 16 |
| **Anggaran TI BPR/fintech kecil terbatas** | Sedang | Tier-3 terjangkau (estimasi Rp 5–15 jt/bln); marjin tinggi karena tanpa biaya GPU/ML memungkinkan harga rendah |
| **Sudah punya vendor enterprise (LJK besar)** | Sedang | Posisikan sebagai pelengkap (OSINT publik + output OJK) yang tidak ditawarkan DRP enterprise; integrasi webhook ke SOC eksisting |
| **Keamanan produksi belum matang** | Sedang | Diakui jujur: API_KEYS statis tanpa rotasi/rate-limit, tanpa enkripsi at-rest, tanpa Alembic (pakai create_all), api_key webhook pelanggan masih plaintext — semua masuk backlog produksi, bukan diklaim selesai |
| **Efektivitas real-world belum terukur** | Sedang | Demo memakai seed; pilot Jun–Sep 2026 (estimasi) adalah uji efektivitas pertama — dinyatakan eksplisit, tidak diklaim sebagai hasil produksi |

### 7.3 Batas kejujuran (anti-overclaim)

Agar validasi pasar tidak melebihi realitas teknis:

- **Bukan ML/NLP** — deteksi adalah regex + validasi algoritmik deterministik. Ini dibingkai sebagai keunggulan (explainable, auditable, murah), bukan disembunyikan.
- **Lintas-lembaga (ala FS-ISAC) adalah roadmap Tahun-2**, bukan kapabilitas saat ini (sistem single-tenant).
- **Collectors live butuh kredensial** yang kosong di `.env.example`; dengan konfigurasi default, scheduler berjalan namun collector early-return — data demo berasal dari seed. Konsisten dengan positioning "prototype fungsional + demo", bukan "produksi".
- **Klaim deteksi <1 jam/<24 jam adalah target**, bukan benchmark produksi terukur.

---

## 8. Kesimpulan Validasi Pasar

SHARK-Fin menyasar pasar yang **terdefinisi, terverifikasi, dan didorong regulasi** dengan white space yang nyata (BPR/fintech kecil yang diabaikan vendor enterprise, dan absennya padanan FS-ISAC Indonesia). Ukuran pasar TAM ~Rp 350–550 miliar/tahun dan SAM ~Rp 70–100 miliar/tahun (estimasi, metode bottom-up dengan denominator OJK/BI terverifikasi) cukup besar untuk menopang bisnis, sementara SOM ~Rp 0,3–2,5 miliar/tahun (estimasi) realistis untuk 12–24 bulan pertama pasca-pilot. Problem-market fit kuat karena kepatuhan siber bersifat wajib. Kesenjangan utama yang diakui jujur adalah **bukti primer (wawancara/survei/LoI) yang masih dalam tahap eksekusi**; rencana eksperimen di Bagian 6 adalah jalur konkret untuk menggantikan asumsi demand dengan bukti terkumpul.

---

## 9. Tabel Verifikasi Statistik

Setiap angka pasar yang dirujuk dokumen ini, dengan sumber, tahun, dan status verifikasi.

| Klaim | Status | Sumber |
|---|---|---|
| Indonesia peringkat ke-8 dunia jumlah akun bocor (2020–2024) | Verified (sumber primer **Surfshark**, bukan IndoSec) | Surfshark via Databoks/Katadata. https://databoks.katadata.co.id/en/technology-telecommunications/statistics/cc5473708a4f8dc |
| 7 juta data dari 450+ instansi di dark web (Sep 2024) | Verified | OJK (Sophia Wattimena) mengutip BSSN, CNBC Indonesia 26 Nov 2024. https://www.cnbcindonesia.com/market/20241126154403-17-591286 |
| 56,1 juta indikator paparan dari 461 instansi (2024; 3,58% keuangan); peluncuran CSIRTradar | Verified | Laporan BSSN via PT Prosperita, Bisnis.com 9 Okt 2025. https://teknologi.bisnis.com/read/20251009/84/1918979 |
| OJK 2.688 pengaduan external fraud (2024) | Verified | OJK (Arwan Hasibuan), Infobank 5 Feb 2025. https://infobanknews.com/ojk-beberkan-telah-terima-2-688-aduan-di-sektor-jasa-keuangan-begini-modusnya/ |
| BRI Life ~2 juta nasabah + 463.000 dokumen (2021) — diungkap eksternal | Verified (koreksi dari "1,3 juta" Tahap-1) | @UnderTheBreach, Jul 2021. https://inet.detik.com/security/d-5659935 |
| BPJS Kesehatan 279 juta (2021) — diungkap eksternal | Verified | RaidForums, Mei 2021. https://www.kompas.com/tren/read/2021/05/21/125000465 |
| 34,9 juta data paspor & 337 juta data Dukcapil (2023) — diungkap eksternal | Verified (reframe dari "KTP digital 35 juta" Tahap-1) | Teguh Aprianto, Jul 2023. https://www.liputan6.com/tekno/read/5337926 ; https://www.kompas.id/baca/polhuk/2023/07/17/337-juta-data-dukcapil-diduga-bocor |
| Kerugian breach sektor keuangan USD 5,9 juta (2023) | Verified | IBM Cost of a Data Breach Report 2023. https://www.ibm.com/think/insights/cost-of-a-data-breach-2024-financial-industry |
| Waktu identifikasi breach ~204 hari (global 2023) / ~168 hari (keuangan 2024) | Verified (koreksi dari "197 hari" Tahap-1) | IBM 2023/2024. https://www.ibm.com/reports/data-breach |
| 97 fintech P2P (LPBBTI) berizin (31 Jan 2025); ~96 pertengahan 2025 | Verified (koreksi dari "334 fintech" Tahap-1) | Direktori OJK. https://ojk.go.id/id/kanal/iknb/data-dan-statistik/direktori/fintech/Pages/Penyelenggara-Fintech-Lending-Berizin-di-OJK-per-31-Januari-2025.aspx |
| BPR ~1.369 (Okt 2024), turun dari 1.405 (Des 2023); ~20 izin dicabut 2024 | Verified | OJK via Kontan/Kompas/ANTARA. https://money.kompas.com/read/2024/10/12/233903926/daftar-15-bank-bpr-yang-ditutup-ojk-hingga-september-2024 |
| Bank umum ~105–107 | Verified | OJK Statistik Perbankan 2023–2024. https://ojk.go.id/id/kanal/perbankan/data-dan-statistik/ |
| Pengguna mobile banking BCA ~31 jt, Mandiri ~27 jt, BNI ~17 jt (2024) | Verified (estimasi per bank) | Bisnis.com 7 Nov 2024. https://finansial.bisnis.com/read/20241107/90/1813852 |
| SEOJK 29/2022: notifikasi insiden 24 jam + laporan rinci 5 hari kerja | Verified | OJK, efektif 27 Des 2022. https://ojk.go.id/id/regulasi/Documents/Pages/Ketahanan-dan-Keamanan-Siber-Bagi-Bank-Umum/RINGKASAN%20SEOJK%2029%20-%2003%20-%202022-1.pdf |
| POJK 12/2024 anti-fraud SELURUH LJK (efektif 31 Okt 2024) | Verified | https://peraturan.go.id/id/peraturan-ojk-no-12-tahun-2024 |
| UU PDP 27/2022 berlaku penuh Okt 2024; Lembaga PDP belum operasional hingga awal 2026 | Verified | https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022 |
| e-wallet ~50-an penerbit berizin BI | **Estimasi** (tanpa sumber tunggal otoritatif) | BI (≈49 per 2020, tren naik) |
| Harga tier, TAM/SAM/SOM, target adopsi, break-even, ARR | **Estimasi** (asumsi dinyatakan eksplisit di Bagian 2 & 6) | Perhitungan internal SHARK-Fin |

> **Koreksi atas Tahap-1.** Empat klaim Tahap-1 diperbaiki demi integritas: (1) "361,8 juta anomali sektor keuangan" → 361 juta adalah angka **nasional**; sektor keuangan hanya 47.729 anomali (BSSN 2023). (2) "1,3 juta record BRI Life" → ~2 juta nasabah. (3) "KTP digital 35 juta" → 34,9 juta paspor / 337 juta Dukcapil. (4) "197 hari" → ~204 hari (global 2023) / ~168 hari (keuangan 2024). "334 fintech berizin" dikoreksi menjadi 97 fintech P2P berizin.
