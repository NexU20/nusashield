import { useContext } from 'react'
import { useStats } from '../hooks/useStats'
import { DemoContext } from '../pages/Dashboard'

function Icon({ children }) {
  return <svg width="24" height="24" viewBox="0 0 24 24" fill="none" style={{ color: 'var(--text-muted)' }}>{children}</svg>
}
function ShieldIcon() { return <Icon><path d="M12 2 L20 6 V12 C20 17.3 16.6 21 12 22.2 C7.4 21 4 17.3 4 12 V6 Z" stroke="currentColor" strokeWidth="1.2" fill="none" /><path d="M12 8 V13 M12 15.5 V16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" /></Icon> }
function DatabaseIcon() { return <Icon><ellipse cx="12" cy="6" rx="8" ry="3" stroke="currentColor" strokeWidth="1.2" fill="none" /><path d="M4 6 V18 C4 19.7 7.6 21 12 21 C16.4 21 20 19.7 20 18 V6" stroke="currentColor" strokeWidth="1.2" fill="none" /><path d="M4 12 C4 13.7 7.6 15 12 15 C16.4 15 20 13.7 20 12" stroke="currentColor" strokeWidth="1.2" fill="none" /></Icon> }
function BuildingIcon() { return <Icon><rect x="4" y="3" width="16" height="19" rx="1" stroke="currentColor" strokeWidth="1.2" fill="none" /><rect x="8" y="7" width="2.5" height="2.5" rx="0.5" fill="currentColor" opacity="0.5" /><rect x="13.5" y="7" width="2.5" height="2.5" rx="0.5" fill="currentColor" opacity="0.5" /><rect x="8" y="12" width="2.5" height="2.5" rx="0.5" fill="currentColor" opacity="0.5" /><rect x="13.5" y="12" width="2.5" height="2.5" rx="0.5" fill="currentColor" opacity="0.5" /><rect x="10" y="17" width="4" height="5" rx="0.5" fill="currentColor" opacity="0.5" /></Icon> }
function CheckIcon() { return <Icon><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="1.2" fill="none" /><path d="M8 12 L11 15 L16 9" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" strokeLinejoin="round" fill="none" /></Icon> }

function formatExposed(n) {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}jt`
  if (n >= 1000) return `${Math.round(n / 1000)}rb`
  return String(n)
}

export default function StatCards() {
  const { data: stats, isLoading } = useStats()
  const { statBoost } = useContext(DemoContext)

  if (isLoading || !stats) {
    return (
      <div className="grid grid-cols-2 gap-4">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="rounded-xl p-6 h-[128px] animate-pulse"
            style={{ backgroundColor: 'var(--accent-bg)', border: '1px solid var(--border-card)' }} />
        ))}
      </div>
    )
  }

  const active = (stats.by_status?.NEW || 0) + (stats.by_status?.VERIFIED || 0) + (statBoost?.active || 0)
  const exposed = (stats.total_records_exposed_estimate || 0) + (statBoost?.exposed || 0)
  const mitigated = stats.by_status?.MITIGATED || 0
  const institutions = stats.institutions_mentioned?.length || 0

  const cards = [
    { label: 'Ancaman Aktif', value: active, trend: '\u2191 +3 dalam 24 jam terakhir', icon: <ShieldIcon />,
      leftBorder: active > 10 ? '3px solid var(--sev-kritis-bar)' : undefined, flash: statBoost?.active },
    { label: 'Estimasi Record Bocor', value: formatExposed(exposed), trend: 'dari 18 sumber aktif', icon: <DatabaseIcon />, flash: statBoost?.exposed },
    { label: 'Lembaga Terekspos', value: institutions, trend: 'bank, fintech, e-wallet', icon: <BuildingIcon /> },
    { label: 'Sudah Dimitigasi', value: mitigated, trend: '\u2193 3 insiden diselesaikan', icon: <CheckIcon />,
      leftBorder: '3px solid var(--sev-rendah-bar)' },
  ]

  return (
    <div className="grid grid-cols-2 gap-4">
      {cards.map(c => (
        <div key={c.label} className="rounded-xl p-6"
          style={{ background: 'var(--card-gradient)', backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-card)', borderLeft: c.leftBorder || '1px solid var(--border-card)' }}>
          <div className="flex items-start justify-between">
            <p className="uppercase" style={{ color: 'var(--text-muted)', fontSize: '11px', letterSpacing: '0.1em', fontFamily: 'var(--font-sans)' }}>{c.label}</p>
            {c.icon}
          </div>
          <p className={`font-bold font-mono mt-2 ${c.flash ? 'flash-value' : ''}`} style={{ color: 'var(--accent)', fontSize: '32px', lineHeight: 1.1, fontFamily: 'var(--font-sans)' }}>{c.value}</p>
          <p className="mt-1.5" style={{ color: 'var(--text-faint)', fontSize: '11px', fontFamily: 'var(--font-sans)' }}>{c.trend}</p>
        </div>
      ))}
    </div>
  )
}
