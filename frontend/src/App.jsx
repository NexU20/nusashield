import { lazy, Suspense } from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { useTheme } from './hooks/useTheme'

const Landing = lazy(() => import('./pages/Landing'))
const Dashboard = lazy(() => import('./pages/Dashboard'))

const base = import.meta.env.BASE_URL || '/'

function LoadingScreen() {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'var(--bg-body)',
      color: 'var(--accent)',
      fontFamily: 'var(--font-sans)',
      gap: '16px',
    }}>
      <svg width="32" height="32" viewBox="0 0 36 36" fill="none">
        <path d="M18 4 L30 28 Q24 26 18 28 Q12 26 6 28 Z" fill="currentColor" opacity="0.7" />
      </svg>
      <div style={{ fontSize: '14px', opacity: 0.7 }}>Memuat...</div>
    </div>
  )
}

export default function App() {
  const { theme, toggle } = useTheme()

  return (
    <BrowserRouter basename={base}>
      <Suspense fallback={<LoadingScreen />}>
        <Routes>
          <Route path="/" element={<Landing theme={theme} toggleTheme={toggle} />} />
          <Route path="/dashboard" element={<Dashboard theme={theme} toggleTheme={toggle} />} />
        </Routes>
      </Suspense>
    </BrowserRouter>
  )
}
