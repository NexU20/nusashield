// Demo data layer — lets the dashboard render fully on a static deploy with NO
// backend. Mirrors backend/scripts/seed_demo.py (same 20 threats) and the
// /api/v1 response shapes. Only MASKED values are shipped here — no raw PII.
// Activated when VITE_DEMO_MODE === 'true' (see client.js).

const E = (type, value, confidence) => ({ type, value, confidence })

// hoursAgo lets timestamps stay recent on every visit (looks live).
const SEED = [
  // ── 3 CRITICAL ──
  { src: 'TELEGRAM', url: 'https://t.me/cc_dump_indo/1547', score: 98, sev: 'CRITICAL', status: 'VERIFIED', tags: ['BRI'], h: 6,
    preview: 'MEGA DUMP — 240.000 kartu kredit nasabah BRI | Format: CC|EXP|CVV|NAMA|ALAMAT | 4052 •••• •••• 0000|12/27|••• | Tested 95% live. #carding #freshcc',
    ents: [E('CREDIT_CARD','405290******0000',0.95),E('CREDIT_CARD','405290******0001',0.95),E('CREDIT_CARD','405290******0002',0.95),E('CVV','***',0.75),E('CVV','***',0.75),E('NIK','320101**********',0.60),E('BANK_NAME','BRI',1.0),E('BANKING_KEYWORD','kartu kredit',1.0),E('BANKING_KEYWORD','carding',1.0),E('BANKING_KEYWORD','fresh cc',1.0)] },
  { src: 'TELEGRAM', url: 'https://t.me/findata_id/3201', score: 96, sev: 'CRITICAL', status: 'NEW', tags: ['DANA','OVO','GoPay','ShopeePay'], h: 3,
    preview: 'KYC DUMP E-WALLET INDONESIA | 89.000 record: NIK + Selfie + No HP + Alamat | Platform: DANA, OVO, GoPay, ShopeePay | NIK: 320101••••••••01 | Full package $3000.',
    ents: [E('NIK','320101**********',0.90),E('NIK','357301**********',0.90),E('NIK','317502**********',0.90),E('BANK_NAME','DANA',1.0),E('BANK_NAME','OVO',1.0),E('BANK_NAME','GoPay',1.0),E('BANK_NAME','ShopeePay',1.0),E('BANKING_KEYWORD','data nasabah',1.0),E('BANKING_KEYWORD','bocor',1.0)] },
  { src: 'PASTE', url: 'https://pastebin.com/Xk9mNp4R', score: 95, sev: 'CRITICAL', status: 'NEW', tags: ['BCA','Mandiri','BNI'], h: 12,
    preview: '=== COMBOLIST BANKING INDONESIA 2026 === | 12.450 akun internet banking verified | Bank: BCA, Mandiri, BNI | email|password|bank | 90% tested valid. Premium list.',
    ents: [E('CREDENTIAL','user=user1@gmail.com pass=***',0.90),E('CREDENTIAL','user=admin@company.co.id pass=***',0.90),E('CREDENTIAL','user=finance@corp.id pass=***',0.90),E('BANK_NAME','BCA',1.0),E('BANK_NAME','Mandiri',1.0),E('BANK_NAME','BNI',1.0),E('BANKING_KEYWORD','internet banking',1.0),E('BANKING_KEYWORD','combolist',1.0)] },
  // ── 5 HIGH ──
  { src: 'PASTE', url: 'https://pastebin.com/Yz7bWq2K', score: 72, sev: 'HIGH', status: 'VERIFIED', tags: [], h: 18,
    preview: 'NPWP Dump — 3.200 Wajib Pajak Indonesia | NPWP: 01.234.567.8-901.234 | PT Sejahtera Abadi | Cocok untuk penipuan pajak. Dijual murah.',
    ents: [E('NPWP','01.234.567.8-901.234',0.85),E('NPWP','02.345.678.9-012.345',0.85),E('NPWP','03.456.789.0-123.456',0.85),E('BANKING_KEYWORD','dump',1.0)] },
  { src: 'TELEGRAM', url: 'https://t.me/bank_leak_idn/892', score: 78, sev: 'HIGH', status: 'NEW', tags: ['BSI','BTN'], h: 8,
    preview: 'Nomor rekening BSI & BTN — 5.400 account | Rek BSI: 700••••••890 | Saldo: Rp 45.000.000 | Include mutasi 6 bulan terakhir. Bulk discount available.',
    ents: [E('ACCOUNT_NUMBER','700****890',0.85),E('ACCOUNT_NUMBER','001****901',0.85),E('BANK_NAME','BSI',1.0),E('BANK_NAME','BTN',1.0),E('BANKING_KEYWORD','rekening',1.0),E('BANKING_KEYWORD','saldo',1.0),E('BANKING_KEYWORD','mutasi',1.0)] },
  { src: 'GITHUB', url: 'https://github.com/threat-actor/phish-bca/blob/main/index.html', score: 82, sev: 'HIGH', status: 'VERIFIED', tags: ['BCA'], h: 24,
    preview: '<!-- Phishing Kit BCA KlikBCA --> <title>KlikBCA - Internet Banking</title> <form action="https://evil-collect.xyz/grab.php"> input: User ID, PIN, Kode OTP/KeyBCA',
    ents: [E('BANK_NAME','BCA',1.0),E('BANKING_KEYWORD','internet banking',1.0),E('BANKING_KEYWORD','PIN',1.0),E('BANKING_KEYWORD','kode OTP',1.0)] },
  { src: 'PASTE', url: 'https://pastebin.com/Mn0pQr34', score: 80, sev: 'HIGH', status: 'NEW', tags: ['Permata','CIMB'], h: 15,
    preview: 'OTP Intercept Log — Permata & CIMB Niaga | Nasabah: +62812••••7890 | OTP: ••••91 | Bank: Permata | SS7 intercept aktif. Realtime feed tersedia.',
    ents: [E('BANK_NAME','Permata',1.0),E('BANK_NAME','CIMB',1.0),E('BANKING_KEYWORD','kode OTP',1.0),E('BANKING_KEYWORD','mobile banking',1.0)] },
  { src: 'HIBP', url: 'https://haveibeenpwned.com/breach/LinkAjaBreachMar2026', score: 75, sev: 'HIGH', status: 'VERIFIED', tags: ['LinkAja'], h: 36,
    preview: 'Breach: LinkAjaBreachMar2026 | Records: 67.000 accounts | Data: email, phone, hashed_password, KTP_number, balance | Source: API vulnerability. Verified by HIBP.',
    ents: [E('BANK_NAME','LinkAja',1.0),E('BANKING_KEYWORD','leak',1.0),E('BANKING_KEYWORD','data nasabah',1.0)] },
  // ── 8 MEDIUM ──
  { src: 'PASTE', url: 'https://pastebin.com/Ab3cDe45', score: 55, sev: 'MEDIUM', status: 'NEW', tags: ['BRI'], h: 40,
    preview: 'Small leak — 120 akun m-banking BRI | 0812••••7890|pin•••••• | Batch kecil, mungkin dari phishing lokal.',
    ents: [E('CREDENTIAL','user=081234567890 pass=***',0.80),E('CREDENTIAL','user=081298765432 pass=***',0.80),E('BANK_NAME','BRI',1.0),E('BANKING_KEYWORD','m-banking',1.0)] },
  { src: 'GITHUB', url: 'https://github.com/intern2026/tugas-akhir/blob/main/.env.production', score: 52, sev: 'MEDIUM', status: 'MITIGATED', tags: ['Mandiri'], h: 72,
    preview: '# Accidentally committed production credentials | MANDIRI_API_KEY=sk_live_••••••• | DB_URL=postgres://mandiri_admin:••••@db.mandiri-api.co.id/production',
    ents: [E('CREDENTIAL','user=mandiri_admin pass=***',0.85),E('BANK_NAME','Mandiri',1.0)] },
  { src: 'TELEGRAM', url: 'https://t.me/indo_leak_alert/1305', score: 45, sev: 'MEDIUM', status: 'NEW', tags: ['Danamon'], h: 10,
    preview: 'Jual data mutasi rekening Danamon 2025-2026 | 800 record, include nama, no rek, saldo terakhir | DM for sample. Harga nego.',
    ents: [E('BANK_NAME','Danamon',1.0),E('BANKING_KEYWORD','mutasi',1.0),E('BANKING_KEYWORD','rekening',1.0),E('BANKING_KEYWORD','saldo',1.0)] },
  { src: 'GITHUB', url: 'https://github.com/dev-test/project/blob/main/test_data.csv', score: 48, sev: 'MEDIUM', status: 'MITIGATED', tags: ['BNI'], h: 96,
    preview: 'nama,nik,no_rekening_bni,saldo | Ahmad W.,320101••••••••01,009••••••890,15000000 | Committed by intern, contains real customer data.',
    ents: [E('NIK','320101**********',0.70),E('NIK','357301**********',0.70),E('ACCOUNT_NUMBER','009****890',0.80),E('BANK_NAME','BNI',1.0)] },
  { src: 'PASTE', url: 'https://pastebin.com/Fg6hIj78', score: 42, sev: 'MEDIUM', status: 'NEW', tags: [], h: 55,
    preview: 'Data NPWP perusahaan Jakarta 2026 | NPWP: 04.567.890.1-234.567 | PT Makmur Jaya | 300 record total.',
    ents: [E('NPWP','04.567.890.1-234.567',0.80),E('NPWP','05.678.901.2-345.678',0.80),E('BANKING_KEYWORD','dump',1.0)] },
  { src: 'GOOGLE_DORK', url: 'https://www.google.com/search?q=shopeepay+breach+2026', score: 38, sev: 'MEDIUM', status: 'VERIFIED', tags: ['ShopeePay'], h: 168,
    preview: 'Breach: ShopeePay2026 | Records: 8.200 Indonesian users | Data: email, hashed_password, phone | No financial data exposed directly.',
    ents: [E('BANK_NAME','ShopeePay',1.0),E('BANKING_KEYWORD','leak',1.0)] },
  { src: 'GITHUB', url: 'https://github.com/random/backup/blob/main/db_dump.sql', score: 50, sev: 'MEDIUM', status: 'NEW', tags: ['BCA'], h: 120,
    preview: '-- Database dump from staging server | INSERT INTO nasabah VALUES (\'BCA\', \'012••••••890\', \'Andi W.\', \'320101••••••••01\', 25000000); -- 450 rows customer data',
    ents: [E('NIK','320101**********',0.70),E('ACCOUNT_NUMBER','012****890',0.80),E('BANK_NAME','BCA',1.0),E('BANKING_KEYWORD','data nasabah',1.0)] },
  { src: 'TELEGRAM', url: 'https://t.me/cc_dump_indo/1120', score: 58, sev: 'MEDIUM', status: 'NEW', tags: ['Mega'], h: 28,
    preview: 'CC Mega Bank - small batch | 4265 •••• •••• 0001|01/28|••• |RUDI H.|JAKARTA | 50 kartu, tested 70% live.',
    ents: [E('CREDIT_CARD','426504******0001',0.95),E('CREDIT_CARD','426505******0002',0.95),E('CVV','***',0.75),E('BANK_NAME','Mega',1.0),E('BANKING_KEYWORD','carding',1.0)] },
  // ── 4 LOW ──
  { src: 'TELEGRAM', url: 'https://t.me/findata_id/2890', score: 15, sev: 'LOW', status: 'FALSE_POSITIVE', tags: ['Bank Jago'], h: 480,
    preview: 'Re-share dari 2024: data lama nasabah Bank Jago | Sudah expired, kebanyakan akun sudah ditutup. Posting ulang dari channel lain.',
    ents: [E('BANK_NAME','Bank Jago',1.0),E('BANKING_KEYWORD','data nasabah',1.0)] },
  { src: 'PASTE', url: 'https://pastebin.com/Qr5sTu67', score: 12, sev: 'LOW', status: 'FALSE_POSITIVE', tags: [], h: 360,
    preview: 'Test data - looks like financial records but possibly fake | CC: 1234567890123456 (fails Luhn) | NIK: 9999990000000000 (invalid province) | Likely honeypot.',
    ents: [E('BANKING_KEYWORD','credit card',1.0)] },
  { src: 'TELEGRAM', url: 'https://t.me/indo_leak_alert/980', score: 18, sev: 'LOW', status: 'NEW', tags: ['Jenius'], h: 200,
    preview: 'Ada yang punya data Jenius? Saya cari buat riset kampus. Bukan untuk tujuan jahat, hanya research.',
    ents: [E('BANK_NAME','Jenius',1.0),E('BANKING_KEYWORD','data nasabah',0.40)] },
  { src: 'GOOGLE_DORK', url: 'https://www.google.com/search?q=bukopin+data+leak+2023', score: 22, sev: 'LOW', status: 'MITIGATED', tags: ['Bukopin'], h: 600,
    preview: 'Breach: OldBukopinLeak (originally from 2023) | Re-indexed by HIBP. 1.200 email+password combos. Most passwords already rotated.',
    ents: [E('BANK_NAME','Bukopin',1.0),E('BANKING_KEYWORD','leak',1.0)] },
]

function buildThreats() {
  const now = Date.now()
  return SEED.map((s, i) => {
    const iso = new Date(now - s.h * 3600_000).toISOString()
    return {
      id: `demo-${String(i + 1).padStart(2, '0')}-${(s.src + s.score).toLowerCase()}`,
      source_type: s.src,
      source_url: s.url,
      content_preview: s.preview,
      detected_entities: { entities: s.ents, count: s.ents.length },
      content_hash: `demo${String(i).padStart(2, '0')}${'0'.repeat(58)}`.slice(0, 64),
      risk_score: s.score,
      severity: s.sev,
      status: s.status,
      institution_tags: s.tags.length ? s.tags : null,
      created_at: iso,
      updated_at: iso,
      _isDemo: true,
    }
  })
}

const THREATS = buildThreats()
const SOURCE_TYPES = ['TELEGRAM', 'PASTE', 'GITHUB', 'HIBP', 'GOOGLE_DORK']
const STATUSES = ['NEW', 'VERIFIED', 'MITIGATED', 'FALSE_POSITIVE']
const SEVERITIES = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']

function listThreats(qs) {
  let items = THREATS.filter(t =>
    (!qs.get('severity') || t.severity === qs.get('severity')) &&
    (!qs.get('source_type') || t.source_type === qs.get('source_type')) &&
    (!qs.get('status') || t.status === qs.get('status')))
  const total = items.length
  const offset = parseInt(qs.get('offset') || '0', 10)
  const limit = parseInt(qs.get('limit') || '50', 10)
  items = items
    .slice()
    .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    .slice(offset, offset + limit)
  return { items, total, limit, offset }
}

function statsSummary() {
  const count = (arr, key, val) => arr.filter(t => t[key] === val).length
  const by_severity = Object.fromEntries(SEVERITIES.map(s => [s, count(THREATS, 'severity', s)]))
  const by_source = Object.fromEntries(SOURCE_TYPES.map(s => [s, count(THREATS, 'source_type', s)]))
  const by_status = Object.fromEntries(STATUSES.map(s => [s, count(THREATS, 'status', s)]))
  const institutions = [...new Set(THREATS.flatMap(t => t.institution_tags || []))].sort()
  return {
    total_threats: THREATS.length,
    by_severity, by_source, by_status,
    total_records_exposed_estimate: THREATS.length * 5,
    institutions_mentioned: institutions,
  }
}

// Axios adapter: resolve known /api/v1 routes from demo data with a small delay
// so loading states still flash (feels live). Everything else 404s.
export function demoAdapter(config) {
  const url = (config.url || '').split('?')[0]
  const qs = new URLSearchParams((config.url || '').split('?')[1] || '')
  const method = (config.method || 'get').toLowerCase()
  let data, status = 200

  const detailMatch = url.match(/\/threats\/([^/]+)$/)
  const statusMatch = url.match(/\/threats\/([^/]+)\/status$/)

  if (method === 'patch' && statusMatch) {
    let body = {}
    try { body = JSON.parse(config.data || '{}') } catch { /* ignore */ }
    data = { id: statusMatch[1], status: body.status, updated_at: new Date().toISOString() }
  } else if (url.endsWith('/stats/summary')) {
    data = statsSummary()
  } else if (url.endsWith('/alerts/webhook/subscriptions')) {
    data = [
      { id: 'demo-wh-1', url: 'https://soc.bri.co.id/hooks/shark-fin', institution: 'BRI', min_severity: 'HIGH', active: true },
      { id: 'demo-wh-2', url: 'https://csirt-fintech.id/ingest', institution: 'AFTECH', min_severity: 'CRITICAL', active: true },
    ]
  } else if (statusMatch) {
    data = THREATS.find(t => t.id === statusMatch[1]) || null
  } else if (url.match(/\/threats\/[^/]+\/report$/)) {
    data = 'Laporan dihasilkan di sisi klien pada mode demo.'
  } else if (detailMatch && detailMatch[1] !== 'threats') {
    data = THREATS.find(t => t.id === detailMatch[1]) || null
    if (!data) status = 404
  } else if (url.endsWith('/threats')) {
    data = listThreats(qs)
  } else {
    data = { detail: 'demo' }; status = 404
  }

  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const res = { data, status, statusText: status === 200 ? 'OK' : 'Error', headers: {}, config, request: {} }
      status >= 400 ? reject({ response: res, config, message: `Demo ${status}` }) : resolve(res)
    }, 180)
  })
}
