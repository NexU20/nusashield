import axios from 'axios'
import { demoAdapter } from './demo'

const API_KEY = import.meta.env.VITE_API_KEY || 'sharkfin-demo-key-2026'

// Demo mode: serve bundled seed data with no backend (static deploy on Vercel).
// Enabled by the build (VITE_DEMO_MODE=true) so the public demo always renders.
export const IS_DEMO = import.meta.env.VITE_DEMO_MODE === 'true'

const client = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api/v1',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY,
  },
})

if (IS_DEMO) {
  client.defaults.adapter = demoAdapter
}

export default client
