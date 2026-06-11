import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import client from '../api/client'

export function useThreats(filters = {}) {
  const params = new URLSearchParams()
  if (filters.severity) params.set('severity', filters.severity)
  if (filters.source_type) params.set('source_type', filters.source_type)
  if (filters.status) params.set('status', filters.status)
  params.set('limit', '50')

  return useQuery({
    queryKey: ['threats', filters],
    queryFn: () => client.get(`/threats?${params}`).then(r => r.data),
    staleTime: 30_000,
    refetchInterval: 30_000,
  })
}

export function useUpdateStatus() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, status }) =>
      client.patch(`/threats/${id}/status`, { status }).then(r => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['threats'] })
      qc.invalidateQueries({ queryKey: ['stats'] })
    },
  })
}
