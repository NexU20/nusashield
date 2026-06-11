import { useMemo } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, CartesianGrid } from 'recharts'
import { useStats } from '../hooks/useStats'

const SOURCE_LABELS = { TELEGRAM: 'Telegram', PASTE: 'Paste Site', GITHUB: 'GitHub', GOOGLE_DORK: 'Google Dork' }
const SRC_KEYS = ['TELEGRAM', 'PASTE', 'GITHUB', 'GOOGLE_DORK']
const SRC_VARS = ['--src-telegram', '--src-paste', '--src-github', '--src-google-dork']

function getVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim()
}

function CustomTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div className="rounded-lg px-4 py-2.5"
      style={{ fontSize: '13px', backgroundColor: 'var(--bg-card)', border: '0.5px solid var(--border-card)' }}>
      <p className="font-medium" style={{ color: 'var(--text-primary)' }}>{d.label}</p>
      <p className="font-mono" style={{ color: 'var(--text-secondary)' }}>{d.count} ancaman</p>
    </div>
  )
}

export default function SourceChart({ theme }) {
  const { data: stats, isLoading } = useStats()

  const colors = useMemo(() => {
    const c = {}
    SRC_KEYS.forEach((k, i) => { c[k] = getVar(SRC_VARS[i]) || '#4a7d9a' })
    return c
  }, [theme])

  if (isLoading || !stats) {
    return (
      <div className="rounded-xl p-5 h-72 animate-pulse"
        style={{ backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-card)' }} />
    )
  }

  const data = Object.entries(stats.by_source || {}).map(([key, count]) => ({
    name: key, label: SOURCE_LABELS[key] || key, count, fill: colors[key] || '#4a7d9a',
  }))

  const axisColor = getVar('--text-muted') || '#4a7d9a'

  return (
    <div className="rounded-xl p-5" style={{ background: 'var(--card-gradient)', backgroundColor: 'var(--bg-card)', border: '1px solid var(--border-card)' }}>
      <h2 className="font-medium uppercase tracking-widest mb-4"
        style={{ fontSize: '13px', color: 'var(--text-muted)', letterSpacing: '0.08em' }}>Ancaman per Sumber</h2>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} layout="vertical" margin={{ left: 5, right: 15 }}>
          <CartesianGrid horizontal={false} stroke="var(--border-divider)" />
          <XAxis type="number" tick={{ fill: axisColor, fontSize: 11 }} axisLine={false} tickLine={false} />
          <YAxis type="category" dataKey="label" tick={{ fill: axisColor, fontSize: 13 }} axisLine={false} tickLine={false} width={80} />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'var(--bg-row-hover)' }} />
          <Bar dataKey="count" radius={[0, 6, 6, 0]} barSize={28}>
            {data.map((entry, i) => <Cell key={i} fill={entry.fill} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
      <div className="flex flex-wrap gap-3 mt-3 justify-center">
        {data.map(d => (
          <div key={d.name} className="flex items-center gap-1.5" style={{ color: 'var(--text-muted)' }}>
            <span className="rounded-sm" style={{ width: '12px', height: '12px', backgroundColor: d.fill }} />
            <span style={{ fontSize: '13px' }}>{d.label}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
