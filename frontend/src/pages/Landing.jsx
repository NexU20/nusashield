import { useNavigate } from 'react-router-dom'
import ThemeToggle from '../components/ThemeToggle'

function SentinelLogo({ size = 36 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 36 36" fill="none">
      <rect x="5" y="5" width="26" height="26" rx="8" fill="var(--accent-bg)" stroke="var(--accent-border)" />
      <path d="M18 9 L26 13 V19 C26 24 22.5 27 18 28 C13.5 27 10 24 10 19 V13 L18 9Z" fill="var(--accent)" opacity="0.9" />
      <path d="M14 18.5 L17 21.5 L23 15.5" stroke="var(--bg-page)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  )
}

function SentinelHero() {
  return (
    <svg width="520" height="230" viewBox="0 0 520 230" fill="none" className="mx-auto mt-12 max-w-full">
      <defs>
        <linearGradient id="heroPanel" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="var(--accent)" stopOpacity="0.18" />
          <stop offset="100%" stopColor="var(--landing-card)" stopOpacity="0.2" />
        </linearGradient>
      </defs>
      <rect x="64" y="24" width="392" height="182" rx="22" fill="url(#heroPanel)" stroke="var(--landing-border)" />
      <rect x="92" y="56" width="126" height="20" rx="10" fill="var(--accent)" opacity="0.18" />
      <rect x="92" y="96" width="336" height="16" rx="8" fill="var(--text-muted)" opacity="0.16" />
      <rect x="92" y="126" width="270" height="16" rx="8" fill="var(--text-muted)" opacity="0.12" />
      <rect x="92" y="156" width="304" height="16" rx="8" fill="var(--text-muted)" opacity="0.12" />
      <circle cx="396" cy="66" r="22" fill="var(--accent)" opacity="0.14" />
      <path d="M386 66 L394 74 L409 58" stroke="var(--accent)" strokeWidth="4" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M60 204 C150 176 222 230 326 194 C384 174 428 182 462 202" stroke="var(--accent)" strokeOpacity="0.24" strokeWidth="2" fill="none" />
    </svg>
  )
}

function SvgIcon({ children }) {
  return <svg width="40" height="40" viewBox="0 0 32 32" fill="none" style={{ color: 'var(--accent)', width: 40, height: 40 }}>{children}</svg>
}
function DetectionIcon() { return <SvgIcon><circle cx="14" cy="14" r="10" stroke="currentColor" strokeWidth="1.5" /><line x1="21" y1="21" x2="28" y2="28" stroke="currentColor" strokeWidth="1.5" /><circle cx="14" cy="14" r="4" stroke="currentColor" strokeWidth="1" opacity="0.5" /></SvgIcon> }
function ClassifierIcon() { return <SvgIcon><rect x="4" y="4" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.5" /><rect x="18" y="4" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.5" /><rect x="4" y="18" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.5" /><rect x="18" y="18" width="10" height="10" rx="2" stroke="currentColor" strokeWidth="1.5" opacity="0.5" /></SvgIcon> }
function ReportIcon() { return <SvgIcon><rect x="6" y="3" width="20" height="26" rx="2" stroke="currentColor" strokeWidth="1.5" /><line x1="10" y1="10" x2="22" y2="10" stroke="currentColor" strokeWidth="1" opacity="0.5" /><line x1="10" y1="14" x2="22" y2="14" stroke="currentColor" strokeWidth="1" opacity="0.5" /><line x1="10" y1="18" x2="18" y2="18" stroke="currentColor" strokeWidth="1" opacity="0.5" /><circle cx="22" cy="23" r="5" stroke="currentColor" strokeWidth="1.5" /><path d="M22 21 L22 23 L24 24" stroke="currentColor" strokeWidth="1" /></SvgIcon> }
function WebhookIcon() { return <SvgIcon><circle cx="16" cy="8" r="4" stroke="currentColor" strokeWidth="1.5" /><circle cx="8" cy="24" r="4" stroke="currentColor" strokeWidth="1.5" /><circle cx="24" cy="24" r="4" stroke="currentColor" strokeWidth="1.5" /><line x1="16" y1="12" x2="10" y2="20" stroke="currentColor" strokeWidth="1" opacity="0.5" /><line x1="16" y1="12" x2="22" y2="20" stroke="currentColor" strokeWidth="1" opacity="0.5" /></SvgIcon> }

const SEV = {
  KRITIS: { bg: 'var(--sev-kritis-bg)', text: 'var(--sev-kritis-text)' },
  TINGGI: { bg: 'var(--sev-tinggi-bg)', text: 'var(--sev-tinggi-text)' },
  SEDANG: { bg: 'var(--sev-sedang-bg)', text: 'var(--sev-sedang-text)' },
}

const MOCK_THREATS = [
  { sev: 'KRITIS', title: 'Dump kartu kredit BRI — 240rb record', meta: 'Telegram · NIK + CVV', time: '6j lalu' },
  { sev: 'KRITIS', title: 'KYC dump e-wallet — 89rb NIK + selfie', meta: 'Paste site · DANA/OVO/GoPay', time: '3j lalu' },
  { sev: 'TINGGI', title: 'Credential combo BCA/Mandiri/BNI — 12,4rb', meta: 'Forum underground', time: '12j lalu' },
  { sev: 'SEDANG', title: 'NPWP dump — 3,2rb record', meta: 'GitHub repo · .env commit', time: '1h lalu' },
]

export default function Landing({ theme, toggleTheme }) {
  const navigate = useNavigate()
  const goDemo = () => navigate('/dashboard')

  return (
    <div style={{ backgroundColor: 'var(--bg-page)', color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }} className="min-h-screen">
      {/* Nav */}
      <nav className="sticky top-0 z-50 backdrop-blur" style={{ backgroundColor: 'var(--bg-header)', borderBottom: '1px solid var(--landing-border)' }}>
        <div className="mx-auto max-w-6xl px-6 py-3 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <SentinelLogo size={32} />
            <div>
              <span className="font-semibold text-sm tracking-tight" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }}>NusaShield FI</span>
              <span className="hidden md:inline text-xs ml-2" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>Financial Exposure Monitoring</span>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="hidden sm:flex items-center gap-5">
              {['Fitur', 'Cara Kerja', 'Tentang'].map(l => (
                <a key={l} href={`#${l.toLowerCase().replace(' ','-')}`} className="text-xs transition-colors hover:opacity-80" style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-sans)' }}>{l}</a>
              ))}
            </div>
            <ThemeToggle theme={theme} onToggle={toggleTheme} />
            <button onClick={goDemo} className="text-sm font-medium px-5 py-2 rounded-md transition-all hover:opacity-80 hover:scale-105"
              style={{ backgroundColor: 'var(--accent)', color: 'var(--bg-page)', fontFamily: 'var(--font-sans)' }}>Lihat Demo</button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="mx-auto max-w-6xl px-6 pt-24 pb-16 text-center relative">
        <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full text-xs mb-10"
          style={{ backgroundColor: 'var(--landing-card)', border: '1px solid var(--landing-border)', color: 'var(--text-secondary)', fontFamily: 'var(--font-sans)' }}>
          <span className="relative flex h-2 w-2">
            <span className="pulse-dot absolute inline-flex h-full w-full rounded-full opacity-75" style={{ backgroundColor: 'var(--accent)' }} />
            <span className="relative inline-flex rounded-full h-2 w-2" style={{ backgroundColor: 'var(--accent)' }} />
          </span>
          Exposure Intelligence · Sektor Keuangan Indonesia
        </div>
        <h1 className="text-5xl md:text-6xl font-bold leading-tight max-w-4xl mx-auto"
          style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)', fontSize: undefined }}>
          <span className="block text-[48px] md:text-[64px] leading-[1.1]">
            Monitor eksposur data finansial dari satu ruang kendali
          </span>
        </h1>
        <p className="mt-6 leading-relaxed max-w-2xl mx-auto" style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-sans)', fontSize: 18 }}>
          Platform ini mengonsolidasikan sinyal OSINT, mengklasifikasi data sensitif Indonesia, lalu memprioritaskan respons berdasarkan risiko dan sumber temuan.
        </p>
        <div className="flex items-center justify-center gap-4 mt-10">
          <button onClick={goDemo} className="text-sm font-semibold px-8 py-3 rounded-md transition-all hover:opacity-90 hover:scale-105"
            style={{ backgroundColor: 'var(--accent)', color: 'var(--bg-page)', fontFamily: 'var(--font-sans)' }}>Lihat Demo Live</button>
          <a href="#cara-kerja" className="text-sm font-semibold px-8 py-3 rounded-md transition-all hover:opacity-80 hover:scale-105"
            style={{ border: '1px solid var(--landing-border)', color: 'var(--text-secondary)', fontFamily: 'var(--font-sans)' }}>Baca Dokumentasi</a>
        </div>
        <SentinelHero />
      </section>

      {/* Stats Bar */}
      <section className="mx-auto max-w-6xl px-6 py-12" style={{ borderTop: '1px solid var(--landing-border)', borderBottom: '1px solid var(--landing-border)' }}>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-8 sm:gap-0 sm:divide-x" style={{ borderColor: 'var(--landing-border)' }}>
          {[{ val: '4', desc: 'Sumber OSINT aktif' }, { val: '8', desc: 'Tipe entitas finansial' }, { val: '24/7', desc: 'Monitoring otomatis' }].map(s => (
            <div key={s.val} className="text-center px-4" style={{ borderColor: 'var(--landing-border)' }}>
              <div style={{ color: 'var(--accent)', fontFamily: 'var(--font-mono)', fontSize: 40, fontWeight: 600, lineHeight: 1.2 }}>{s.val}</div>
              <div className="text-sm mt-2" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>{s.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* Mock Threat Feed */}
      <section className="mx-auto max-w-6xl px-6 py-20">
        <div className="text-center mb-10">
          <div className="text-[11px] tracking-widest uppercase mb-3" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>Threat Feed · Preview</div>
          <h2 className="text-2xl sm:text-3xl font-semibold" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }}>Ancaman yang sedang dipantau</h2>
        </div>
        <div className="rounded-xl overflow-hidden" style={{ border: '1px solid var(--landing-border)', backgroundColor: 'var(--landing-card)' }}>
          {MOCK_THREATS.map((t, i) => (
            <div key={i} className="px-6 py-4.5 flex items-center justify-between gap-4"
              style={{ borderBottom: i < MOCK_THREATS.length - 1 ? '1px solid var(--landing-border)' : 'none', padding: '18px 24px' }}>
              <div className="flex items-center gap-4 min-w-0">
                <span className="text-[11px] font-semibold px-3 py-1 rounded shrink-0" style={{ backgroundColor: SEV[t.sev].bg, color: SEV[t.sev].text, fontFamily: 'var(--font-sans)' }}>{t.sev}</span>
                <div className="min-w-0">
                  <div className="text-[15px] truncate font-medium" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }}>{t.title}</div>
                  <div className="text-xs truncate mt-0.5" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>{t.meta}</div>
                </div>
              </div>
              <span className="text-xs shrink-0" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{t.time}</span>
            </div>
          ))}
        </div>
        <div className="text-center mt-8">
          <button onClick={goDemo} className="text-sm font-medium transition-all hover:opacity-80 hover:scale-105" style={{ color: 'var(--accent)', fontFamily: 'var(--font-sans)' }}>Buka Dashboard Lengkap &rarr;</button>
        </div>
      </section>

      {/* Fitur */}
      <section id="fitur" className="mx-auto max-w-6xl px-6 py-20">
        <div className="text-center mb-12">
          <div className="text-[11px] tracking-widest uppercase mb-3" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>Fitur</div>
          <h2 className="text-2xl sm:text-3xl font-semibold" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }}>Dibangun khusus untuk sektor keuangan Indonesia</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {[
            { icon: <DetectionIcon />, title: 'Deteksi < 1 jam', desc: 'Crawler 24/7 pada Telegram, paste site, GitHub, dan Google Dork. Alert dikirim ke dashboard dan webhook sebelum data dieksploitasi.' },
            { icon: <ClassifierIcon />, title: 'Classifier NIK, NPWP, BIN bank', desc: 'Validasi NIK dengan tanggal lahir dan kode provinsi, checksum NPWP, serta deteksi BIN bank untuk mengurangi false positive.' },
            { icon: <ReportIcon />, title: 'Draft notifikasi mengacu SEOJK 29/2022', desc: 'Draft notifikasi awal mengacu elemen wajib Bab IX SEOJK 29/SEOJK.03/2022. Membantu bank memenuhi kewajiban notifikasi 24 jam ke OJK setelah insiden dikonfirmasi.' },
            { icon: <WebhookIcon />, title: 'Webhook API real-time', desc: 'Integrasi langsung ke SIEM atau SOC lembaga. 92 automated tests. One-command deployment via Docker.' },
          ].map(f => (
            <div key={f.title} className="rounded-xl p-8 transition-all duration-200 hover:scale-[1.02]"
              style={{ background: 'var(--card-gradient)', border: '1px solid var(--landing-border)' }}>
              <div className="mb-4">{f.icon}</div>
              <h3 className="font-semibold mb-2" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)', fontSize: 18 }}>{f.title}</h3>
              <p className="leading-relaxed" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)', fontSize: 15 }}>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Cara Kerja */}
      <section id="cara-kerja" className="mx-auto max-w-6xl px-6 py-20">
        <div className="text-center mb-12">
          <div className="text-[11px] tracking-widest uppercase mb-3" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>Cara Kerja</div>
          <h2 className="text-2xl sm:text-3xl font-semibold" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }}>Tiga langkah. Otomatis.</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[
            { step: '01', title: 'Pantau', desc: 'Crawler otomatis memantau Telegram public channel, paste site, dan GitHub 24/7.' },
            { step: '02', title: 'Deteksi', desc: 'Classifier mengidentifikasi NIK, NPWP, nomor kartu, dan kredensial dengan validasi algoritmik.' },
            { step: '03', title: 'Respons', desc: 'Alert real-time ke dashboard analis + webhook ke sistem SOC lembaga.' },
          ].map(s => (
            <div key={s.step} className="rounded-xl p-8 transition-all duration-200 hover:scale-[1.02]"
              style={{ background: 'var(--card-gradient)', border: '1px solid var(--landing-border)' }}>
              <div className="mb-4 inline-block px-3 py-1.5 rounded-md"
                style={{ backgroundColor: 'var(--bg-page)', color: 'var(--accent)', border: '1px solid var(--landing-border)', fontFamily: 'var(--font-mono)', fontSize: 32, fontWeight: 600, lineHeight: 1.2 }}>{s.step}</div>
              <h3 className="font-semibold mb-2" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)', fontSize: 18 }}>{s.title}</h3>
              <p className="leading-relaxed" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)', fontSize: 15 }}>{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* CTA / Tentang */}
      <section id="tentang" className="mx-auto max-w-6xl px-6 py-20 text-center" style={{ borderTop: '1px solid var(--landing-border)' }}>
        <h2 className="text-2xl sm:text-3xl font-semibold mb-5" style={{ color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }}>Lindungi ekosistem keuangan digital Indonesia</h2>
        <p className="max-w-xl mx-auto mb-10" style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-sans)', fontSize: 16 }}>
          Sistem hanya memantau sumber yang dapat diakses secara publik. Tidak ada akses ilegal. Semua data sensitif di-mask dan digunakan untuk tujuan defensif.
        </p>
        <button onClick={goDemo} className="text-sm font-semibold px-8 py-3 rounded-md transition-all hover:opacity-90 hover:scale-105"
          style={{ backgroundColor: 'var(--accent)', color: 'var(--bg-page)', fontFamily: 'var(--font-sans)' }}>Lihat Demo Live</button>
      </section>

      {/* Footer */}
      <footer style={{ borderTop: '1px solid var(--landing-border)' }}>
        <div className="mx-auto max-w-6xl px-6 py-6 flex flex-col sm:flex-row items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <SentinelLogo size={20} />
            <div>
              <span className="text-xs font-semibold" style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-sans)' }}>NusaShield FI</span>
              <span className="text-[10px] ml-1.5" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>v0.1.0</span>
              <span className="text-[10px] ml-2 hidden sm:inline" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>Financial exposure monitoring dashboard</span>
            </div>
          </div>
          <div className="text-[10px]" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>Defensive OSINT · Data minimization · Analyst workflow</div>
        </div>
      </footer>
    </div>
  )
}
