import { useState, useEffect, useCallback, createContext, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { useQueryClient } from '@tanstack/react-query'
import StatCards from '../components/StatCards'
import ThreatFeed from '../components/ThreatFeed'
import SourceChart from '../components/SourceChart'
import ThreatDetail from '../components/ThreatDetail'
import ThemeToggle from '../components/ThemeToggle'
import { IS_DEMO } from '../api/client'

export const DemoContext = createContext({ demoThreat: null, statBoost: null })

const DEMO_THREAT = {
  id: 'demo-' + Date.now(), source_type: 'TELEGRAM',
  source_url: 'https://t.me/indo_cc_dumps/8821',
  content_preview: 'Fresh Mandiri fullz 5.2k | CC + NIK + CVV | exp 2026 | harga nego | format: 4539XXXXXXXX|XX/XX|XXX|nama|NIK16digit',
  detected_entities: { entities: [
    { type: 'CREDIT_CARD', value: '4539 •••• •••• 1234', confidence: 0.95 },
    { type: 'CREDIT_CARD', value: '4539 •••• •••• 5678', confidence: 0.93 },
    { type: 'NIK', value: '321201 •••••••• 07', confidence: 0.90 },
    { type: 'CVV', value: '***', confidence: 0.75 },
    { type: 'BANK_NAME', value: 'Mandiri', confidence: 1.0 },
  ], count: 5 },
  content_hash: 'demo', risk_score: 94, severity: 'CRITICAL', status: 'NEW',
  institution_tags: ['Bank Mandiri'],
  created_at: new Date().toISOString(), updated_at: new Date().toISOString(), _isDemo: true,
}

function WibClock() {
  const [time, setTime] = useState('')
  useEffect(() => {
    function tick() {
      const now = new Date()
      const wib = new Date(now.getTime() + (7 * 60 + now.getTimezoneOffset()) * 60000)
      setTime(wib.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' }))
    }
    tick(); const id = setInterval(tick, 1000); return () => clearInterval(id)
  }, [])
  return <span className="font-mono" style={{ color: 'var(--accent)', fontFamily: 'var(--font-sans)', fontSize: '12px' }}>{time}</span>
}

function ScanIndicator() {
  const [open, setOpen] = useState(false)
  return (
    <div className="relative">
      <button onClick={() => setOpen(o => !o)} className="flex items-center gap-2 text-xs" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>
        <span className="relative flex h-2 w-2">
          <span className="pulse-green absolute inline-flex h-full w-full rounded-full" style={{ backgroundColor: 'var(--scan-dot)' }} />
          <span className="relative inline-flex rounded-full h-2 w-2" style={{ backgroundColor: 'var(--scan-dot)' }} />
        </span>
        <span className="hidden sm:inline">Memindai 4 sumber</span>
      </button>
      {open && (
        <>
          <div className="fixed inset-0 z-40" onClick={() => setOpen(false)} />
          <div className="absolute right-0 top-8 z-50 w-72 rounded-xl p-4 space-y-3"
            style={{ backgroundColor: 'var(--bg-header)', border: '1px solid var(--border-input)', fontFamily: 'var(--font-sans)' }}>
            {[{ name: 'Telegram', time: '2 menit lalu' }, { name: 'Paste Site', time: '8 menit lalu' },
              { name: 'GitHub', time: '12 menit lalu' }, { name: 'Google Dork', time: '52 menit lalu' }].map(s => (
              <div key={s.name} className="flex items-center justify-between" style={{ fontSize: '14px' }}>
                <span style={{ color: 'var(--text-secondary)' }}><span style={{ color: 'var(--scan-dot)' }}>&#10003;</span> {s.name}</span>
                <span style={{ color: 'var(--text-faint)' }}>{s.time}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

function ScanBar({ phase }) {
  if (!phase) return null
  const configs = {
    scanning: { bg: 'var(--scan-scanning)', text: 'var(--accent)', msg: 'NusaShield FI sedang memindai sumber aktif...' },
    detected: { bg: 'var(--scan-detected)', text: '#fff', msg: '\u26A0 Konten mencurigakan terdeteksi di Telegram' },
    analyzing: { bg: 'var(--scan-analyzing)', text: '#fff', msg: '\uD83D\uDD0D Menganalisis entitas finansial...' },
    critical: { bg: 'var(--scan-critical)', text: '#fff', msg: 'KRITIS \u2014 Kebocoran data dikonfirmasi' },
    out: { bg: 'var(--scan-critical)', text: '#fff', msg: 'KRITIS \u2014 Kebocoran data dikonfirmasi' },
  }
  const c = configs[phase] || configs.scanning
  return (
    <div className={`fixed top-0 left-0 right-0 z-[60] ${phase === 'out' ? 'scan-slide-out' : 'scan-slide-in'}`}
      style={{ backgroundColor: c.bg, borderBottom: '1px solid var(--border-input)', fontFamily: 'var(--font-sans)' }}>
      <div className="mx-auto max-w-[1440px] px-6 py-2.5 flex items-center gap-3">
        {phase === 'scanning' && <span className="scan-pulse" style={{ color: c.text, fontSize: '14px' }}>●</span>}
        <span className="font-medium" style={{ color: c.text, fontSize: '14px' }}>{c.msg}</span>
      </div>
    </div>
  )
}

function Toast({ show, fading, onDetail }) {
  if (!show) return null
  return (
    <div className={`fixed top-16 right-6 z-[60] max-w-md w-full ${fading ? 'toast-out' : 'toast-in'}`}
      style={{ backgroundColor: 'var(--toast-bg)', border: '1px solid var(--toast-bdr)', borderLeft: '4px solid #ef4444', borderRadius: '10px', boxShadow: 'var(--toast-shadow)', fontFamily: 'var(--font-sans)' }}>
      <div className="p-5 space-y-2">
        <div className="flex items-center gap-2">
          <span style={{ color: '#ef4444' }}>&#x1F534;</span>
          <span className="text-xs font-medium" style={{ color: 'var(--sev-kritis-text)' }}>ANCAMAN BARU TERDETEKSI</span>
        </div>
        <p className="text-sm font-medium" style={{ color: 'var(--text-primary)' }}>Kartu kredit Mandiri — 5.200 record</p>
        <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Telegram · t.me/indo_cc_dumps · KRITIS</p>
        <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Entitas: CREDIT_CARD, NIK, CVV</p>
        <p className="text-xs" style={{ color: 'var(--accent)' }}>Risk score: 94/100</p>
        <button onClick={onDetail} className="text-xs font-medium mt-1" style={{ color: 'var(--accent)' }}>Lihat Detail &rarr;</button>
      </div>
    </div>
  )
}

export default function Dashboard({ theme, toggleTheme }) {
  const [selected, setSelected] = useState(null)
  const [demoThreat, setDemoThreat] = useState(null)
  const [statBoost, setStatBoost] = useState(null)
  const [scanPhase, setScanPhase] = useState(null)
  const [showToast, setShowToast] = useState(false)
  const [toastFading, setToastFading] = useState(false)
  const [demoRunning, setDemoRunning] = useState(false)
  const navigate = useNavigate()
  const qc = useQueryClient()

  const runDemo = useCallback(() => {
    if (demoRunning) return; setDemoRunning(true); setDemoThreat(null); setStatBoost(null); setShowToast(false); setToastFading(false)
    const newThreat = { ...DEMO_THREAT, id: 'demo-' + Date.now(), created_at: new Date().toISOString(), updated_at: new Date().toISOString() }
    setScanPhase('scanning')
    setTimeout(() => setScanPhase('detected'), 2000)
    setTimeout(() => setScanPhase('analyzing'), 3500)
    setTimeout(() => { setScanPhase('critical'); setShowToast(true) }, 5000)
    setTimeout(() => { setDemoThreat(newThreat); setStatBoost({ active: 1, exposed: 5200 }); qc.invalidateQueries({ queryKey: ['stats'] }) }, 6000)
    setTimeout(() => { setScanPhase('out'); setTimeout(() => setScanPhase(null), 400) }, 8000)
    setTimeout(() => setToastFading(true), 12000)
    setTimeout(() => { setShowToast(false); setToastFading(false) }, 12500)
    setTimeout(() => setDemoRunning(false), 9000)
  }, [demoRunning, qc])

  return (
    <DemoContext.Provider value={{ demoThreat, statBoost }}>
      <div className="min-h-screen" style={{ backgroundColor: 'var(--bg-page)', color: 'var(--text-primary)', fontFamily: 'var(--font-sans)' }}>
        <ScanBar phase={scanPhase} />
        <Toast show={showToast} fading={toastFading} onDetail={() => { setShowToast(false); setSelected(demoThreat || DEMO_THREAT) }} />

        <nav className="sticky top-0 z-40 backdrop-blur" style={{ backgroundColor: 'var(--bg-header)', borderBottom: '1px solid var(--border-card)' }}>
          <div className="mx-auto max-w-[1440px] px-6 py-4 flex items-center gap-3">
            <button onClick={() => navigate('/')} className="h-9 w-9 rounded-lg flex items-center justify-center shrink-0"
              style={{ backgroundColor: 'var(--accent-bg)' }}>
              <svg width="24" height="24" viewBox="0 0 36 36" fill="none">
                <path d="M18 7 L27 12 V19 C27 24.5 23.2 28 18 29 C12.8 28 9 24.5 9 19 V12 L18 7Z" fill="var(--accent)" opacity="0.9" />
                <path d="M14 18.5 L17 21.5 L23 15.5" stroke="var(--bg-page)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </button>
            <span className="font-semibold" style={{ color: 'var(--text-primary)', fontSize: '16px', fontFamily: 'var(--font-sans)' }}>NusaShield FI</span>
            <span className="hidden md:inline text-xs" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>Financial Exposure Monitoring</span>
            {IS_DEMO && (
              <span title="Data contoh untuk peragaan — bukan data produksi"
                className="px-2 py-0.5 rounded-md font-medium"
                style={{ fontSize: '10px', letterSpacing: '0.04em', backgroundColor: 'var(--accent-bg)', color: 'var(--text-muted)', border: '1px solid var(--border-subtle)', fontFamily: 'var(--font-sans)' }}>
                DEMO · data contoh
              </span>
            )}
            <div className="ml-auto flex items-center gap-4">
              <ScanIndicator />
              <ThemeToggle theme={theme} onToggle={toggleTheme} />
              <button onClick={() => navigate('/')} className="text-xs hidden sm:inline" style={{ color: 'var(--text-secondary)', fontFamily: 'var(--font-sans)' }}>&larr; Beranda</button>
              <div className="text-xs flex items-center gap-2" style={{ color: 'var(--text-muted)', fontFamily: 'var(--font-sans)' }}>
                <span className="hidden sm:inline">WIB</span><WibClock />
              </div>
            </div>
          </div>
        </nav>

        <main className="mx-auto max-w-[1440px] px-6 py-6">
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
            <div className="lg:col-span-3"><ThreatFeed onSelect={setSelected} /></div>
            <div className="lg:col-span-2 space-y-6"><StatCards /><SourceChart theme={theme} /></div>
          </div>
        </main>

        <div className="mt-8" style={{ paddingBottom: '24px' }}>
          {[1, 2, 3].map(i => <div key={i} style={{ height: '0.5px', backgroundColor: i === 1 ? 'var(--ocean-line-1)' : 'var(--ocean-line-2)', marginBottom: '6px', marginLeft: '10%', marginRight: '10%' }} />)}
        </div>

        <button onClick={runDemo} disabled={demoRunning} className="fixed bottom-6 right-6 z-50 px-6 py-3 rounded-2xl font-medium text-sm flex items-center gap-2"
          style={{ backgroundColor: demoRunning ? 'var(--logo-fin)' : 'var(--accent)', color: 'var(--bg-page)', opacity: demoRunning ? 0.6 : 1, fontFamily: 'var(--font-sans)', boxShadow: '0 2px 8px rgba(0,0,0,0.15)' }}>
          {demoRunning ? (
            <><svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><circle cx="8" cy="8" r="4" /></svg> Memindai...</>
          ) : (
            <><svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor"><path d="M5 3 L13 8 L5 13 Z" /></svg> Simulasi Deteksi</>
          )}
        </button>

        {selected && <ThreatDetail threat={selected} onClose={() => setSelected(null)} />}
      </div>
    </DemoContext.Provider>
  )
}
