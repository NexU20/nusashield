import { useQuery } from '@tanstack/react-query'
import client from '../api/client'

export function useStats() {
  return useQuery({
    queryKey: ['stats'],
    queryFn: () => client.get('/stats/summary').then(r => r.data),
    staleTime: 30_000,
    refetchInterval: 30_000,
  })
}
