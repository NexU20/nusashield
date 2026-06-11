export default function ThemeToggle({ theme, onToggle }) {
  const isDark = theme === 'dark'
  return (
    <button
      onClick={onToggle}
      title="Ganti tema"
      className="relative flex items-center justify-between rounded-full transition-colors"
      style={{
        width: '52px',
        height: '28px',
        padding: '4px',
        backgroundColor: 'var(--toggle-bg)',
        border: '0.5px solid var(--toggle-border)',
      }}
    >
      {/* Moon */}
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{ position: 'relative', zIndex: 1 }}>
        <path
          d="M12 3a6 6 0 0 0 0 10 7 7 0 1 1 0-10z"
          fill="currentColor"
          style={{ color: isDark ? 'var(--accent)' : 'var(--text-faint)' }}
        />
      </svg>
      {/* Sun */}
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" style={{ position: 'relative', zIndex: 1 }}>
        <circle cx="8" cy="8" r="3" fill="currentColor" style={{ color: isDark ? 'var(--text-faint)' : 'var(--accent)' }} />
        {[0, 45, 90, 135, 180, 225, 270, 315].map(deg => {
          const rad = (deg * Math.PI) / 180
          return (
            <line
              key={deg}
              x1={8 + Math.cos(rad) * 5}
              y1={8 + Math.sin(rad) * 5}
              x2={8 + Math.cos(rad) * 6.5}
              y2={8 + Math.sin(rad) * 6.5}
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              style={{ color: isDark ? 'var(--text-faint)' : 'var(--accent)' }}
            />
          )
        })}
      </svg>
      {/* Sliding indicator */}
      <span
        className="absolute rounded-full transition-all"
        style={{
          width: '20px',
          height: '20px',
          top: '3.5px',
          left: isDark ? '4px' : '27px',
          backgroundColor: 'var(--accent)',
          opacity: 0.2,
          transitionDuration: '200ms',
          transitionTimingFunction: 'ease',
        }}
      />
    </button>
  )
}
