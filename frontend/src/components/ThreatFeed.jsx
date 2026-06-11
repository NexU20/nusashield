import { useState, useContext } from 'react'
import { useThreats } from '../hooks/useThreats'
import { DemoContext } from '../pages/Dashboard'

const SEV_LABEL = { CRITICAL: 'KRITIS', HIGH: 'TINGGI', MEDIUM: 'SEDANG', LOW: 'RENDAH' }
const SEV_VAR = {
  CRITICAL: { bg: '--sev-kritis-bg', color: '--sev-kritis-text', border: '--sev-kritis-bdr', left: '--sev-kritis-bar', score: '--sev-kritis-text' },
  HIGH: { bg: '--sev-tinggi-bg', color: '--sev-tinggi-text', border: '--sev-tinggi-bdr', left: '--sev-tinggi-bar', score: '--sev-tinggi-text' },
  MEDIUM: { bg: '--sev-sedang-bg', color: '--sev-sedang-text', border: '--sev-sedang-bdr', left: '--sev-sedang-bar', score: '--sev-sedang-text' },
  LOW: { bg: '--sev-rendah-bg', color: '--sev-rendah-text', border: '--sev-rendah-bdr', left: '--sev-rendah-bar', score: '--sev-rendah-text' },
}
const SRC_LABEL = { TELEGRAM: 'Telegram', PASTE: 'Paste', GITHUB: 'GitHub', HIBP: 'HIBP', GOOGLE_DORK: 'Google Dork' }

function timeAgo(iso) {
  const diff = Date.now() - new Date(iso).getTime(), m = Math.floor(diff / 60000)
  if (m < 1) return 'baru saja'; if (m < 60) return `${m} menit lalu`
  const h = Math.floor(m / 60); if (h < 24) return `${h} jam lalu`; return `${Math.floor(h / 24)} hari lalu`
}
function buildTitle(t) {
  const types = [...new Set((t.detected_entities?.entities || []).map(e => e.type))]
  const labels = { CREDIT_CARD: 'Kartu Kredit', NIK: 'NIK', NPWP: 'NPWP', CREDENTIAL: 'Kredensial', ACCOUNT_NUMBER: 'No. Rekening', CVV: 'CVV', BANK_NAME: 'Bank', BANKING_KEYWORD: 'Keyword' }
  return `${labels[types[0]] || types[0] || 'DATA'} via ${SRC_LABEL[t.source_type] || t.source_type}${t.institution_tags?.length ? ` \u2014 ${t.institution_tags.join(', ')}` : ''}`
}
function truncateUrl(url, max = 40) { return !url ? '-' : url.length > max ? url.slice(0, max) + '...' : url }

function sev(severity) { return SEV_VAR[severity] || SEV_VAR.LOW }

export default function ThreatFeed({ onSelect }) {
  const [filters, setFilters] = useState({}), [search, setSearch] = useState(''), [hoveredId, setHoveredId] = useState(null)
  const { data, isLoading } = useThreats(filters)
  const { demoThreat } = useContext(DemoContext)

  let threats = (data?.items || []).filter(t => {
    if (!search) return true; const s = search.toLowerCase()
    return (t.raw_content || '').toLowerCase().includes(s) || (t.institution_tags || []).some(tag => tag.toLowerCase().includes(s)) || (t.source_url || '').toLowerCase().includes(s)
  })
  if (demoThreat) threats = [demoThreat, ...threats]

  return (
    <div className="rounded-xl overflow-hidden flex flex-col" style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-card)' }}>
      <div className="p-4 space-y-3" style={{ borderBottom: '1px solid var(--border-subtle)' }}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <h2 className="font-medium uppercase tracking-widest" style={{ fontSize: '13px', color: 'var(--text-muted)', letterSpacing: '0.08em' }}>Feed Ancaman</h2>
            <span className="flex items-center gap-1.5" style={{ fontSize: '11px', color: '#ef4444' }}>
              <span className="relative flex h-2 w-2"><span className="pulse-dot absolute inline-flex h-full w-full rounded-full" style={{ backgroundColor: '#ef4444' }} /><span className="relative inline-flex rounded-full h-2 w-2" style={{ backgroundColor: '#ef4444' }} /></span>LIVE
            </span>
          </div>
          <span className="text-[10px]" style={{ color: 'var(--text-faint)' }}>{data?.total || 0} total · Diperbarui setiap 30 detik</span>
        </div>
        <div className="flex flex-wrap gap-2">
          <input type="text" placeholder="Cari..." value={search} onChange={e => setSearch(e.target.value)}
            className="px-3 py-1.5 rounded-xl w-44"
            style={{ fontSize: '14px', backgroundColor: 'var(--bg-input)', border: '1px solid var(--border-input)', color: 'var(--text-secondary)', outline: 'none' }} />
          {[
            { key: 'severity', opts: [['', 'Semua Severity'], ['CRITICAL', 'Kritis'], ['HIGH', 'Tinggi'], ['MEDIUM', 'Sedang'], ['LOW', 'Rendah']] },
            { key: 'source_type', opts: [['', 'Semua Sumber'], ['TELEGRAM', 'Telegram'], ['PASTE', 'Paste'], ['GITHUB', 'GitHub'], ['GOOGLE_DORK', 'Google Dork']] },
            { key: 'status', opts: [['', 'Semua Status'], ['NEW', 'Baru'], ['VERIFIED', 'Terverifikasi'], ['MITIGATED', 'Dimitigasi'], ['FALSE_POSITIVE', 'Positif Palsu']] },
          ].map(f => (
            <select key={f.key} value={filters[f.key] || ''} onChange={e => setFilters(prev => ({ ...prev, [f.key]: e.target.value || undefined }))}
              className="px-2.5 py-1.5 rounded-xl text-sm"
              style={{ backgroundColor: 'var(--bg-input)', border: '1px solid var(--border-input)', color: 'var(--text-secondary)', outline: 'none' }}>
              {f.opts.map(([v, l]) => <option key={v} value={v} style={{ backgroundColor: 'var(--bg-input)' }}>{l}</option>)}
            </select>
          ))}
        </div>
      </div>

      <ul className="overflow-y-auto max-h-[720px]">
        {isLoading && <li className="p-6 text-center text-sm" style={{ color: 'var(--text-faint)' }}>Memuat...</li>}
        {!isLoading && !threats.length && <li className="p-6 text-center text-sm" style={{ color: 'var(--text-faint)' }}>Tidak ada ancaman ditemukan.</li>}
        {threats.map((t, idx) => {
          const entityList = t.detected_entities?.entities || [], entityTypes = [...new Set(entityList.map(e => e.type))]
          const s = sev(t.severity), isHovered = hoveredId === t.id
          return (
            <li key={t.id} onClick={() => onSelect(t)} onMouseEnter={() => setHoveredId(t.id)} onMouseLeave={() => setHoveredId(null)}
              className={`px-5 py-4 cursor-pointer transition-colors ${t._isDemo ? 'threat-enter threat-pulse-red' : ''}`}
              style={{ borderBottom: idx < threats.length - 1 ? '1px solid var(--border-divider)' : 'none', borderLeft: `3px solid var(${s.left})`,
                backgroundColor: isHovered ? 'var(--bg-row-hover)' : 'transparent' }}>
              <div className="flex items-start gap-3">
                <span className="mt-0.5 shrink-0 rounded-md uppercase font-medium"
                  style={{ fontSize: '10px', padding: '4px 10px', letterSpacing: '0.06em', backgroundColor: `var(${s.bg})`, color: `var(${s.color})`, border: `1px solid var(${s.border})` }}>
                  {SEV_LABEL[t.severity]}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="font-semibold truncate" style={{ fontSize: '15px', color: 'var(--text-primary)' }}>{buildTitle(t)}</p>
                  <p className="mt-0.5 truncate" style={{ fontSize: '13px', color: 'var(--text-faint)' }}>
                    {truncateUrl(t.source_url)} &middot; {entityList.length} entitas &middot; {timeAgo(t.created_at)}
                  </p>
                  <div className="flex flex-wrap items-center gap-1.5 mt-2">
                    {entityTypes.map(et => (
                      <span key={et} className="rounded px-2 py-0.5"
                        style={{ fontSize: '11px', backgroundColor: 'var(--tag-bg)', color: 'var(--tag-text)', border: '1px solid var(--tag-bdr)' }}>{et}</span>
                    ))}
                    {isHovered && <span className="ml-1" style={{ fontSize: '11px', color: 'var(--accent)' }}>&rarr; lihat</span>}
                  </div>
                </div>
                <div className="shrink-0 mt-0.5">
                  <div className="rounded-full flex items-center justify-center transition-shadow"
                    style={{ width: '42px', height: '42px', border: `2px solid var(${s.score})`, backgroundColor: isHovered ? `var(${s.bg})` : 'var(--score-bg)',
                      boxShadow: isHovered ? `0 0 10px var(${s.bg})` : 'none' }}>
                    <span className="font-bold font-mono" style={{ fontSize: '14px', color: `var(${s.score})` }}>{t.risk_score}</span>
                  </div>
                </div>
              </div>
            </li>
          )
        })}
      </ul>
    </div>
  )
}
