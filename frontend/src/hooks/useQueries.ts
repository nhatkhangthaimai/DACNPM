import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiService } from '../services/api';
import { Job, CV, Application, UserRole, MatchScoreBreakdown } from '../types';

export const QUERY_KEYS = {
  jobs: (filters?: any) => ['jobs', filters ?? 'all'] as const,
  jobDetail: (id: string) => ['job', id] as const,
  cvs: (candidateId: string) => ['cvs', candidateId] as const,
  applications: (role: string, userId?: string) => ['applications', role, userId ?? 'default'] as const,
  matchResult: (cvId: string, jobId: string) => ['match', cvId, jobId] as const,
  notifications: (userId?: string) => ['notifications', userId ?? 'default'] as const,
};

/**
 * Hook to fetch jobs with automatic deduplication, caching (3 mins staleTime) & AbortSignal support.
 */
export function useJobs(filters?: Parameters<typeof apiService.getJobs>[0]) {
  return useQuery<Job[], Error>({
    queryKey: QUERY_KEYS.jobs(filters),
    queryFn: ({ signal }) => apiService.getJobs(filters, signal),
    staleTime: 3 * 60 * 1000, // 3 minutes fresh cache
    gcTime: 10 * 60 * 1000,    // 10 minutes memory garbage collection
    refetchOnWindowFocus: false,
    retry: 1,
  });
}

/**
 * Hook to fetch a single job by ID.
 */
export function useJob(id: string | undefined) {
  return useQuery<Job | null, Error>({
    queryKey: QUERY_KEYS.jobDetail(id || ''),
    queryFn: () => (id ? apiService.getJobById(id) : Promise.resolve(null)),
    enabled: Boolean(id),
    staleTime: 5 * 60 * 1000,
    gcTime: 15 * 60 * 1000,
    refetchOnWindowFocus: false,
  });
}

/**
 * Hook to fetch candidate's CV list with 30s cache, isolated to candidateId.
 */
export function useCandidateCVs(candidateId: string | undefined) {
  const validId = candidateId || 'user-cand-1';
  return useQuery<CV[], Error>({
    queryKey: QUERY_KEYS.cvs(validId),
    queryFn: ({ signal }) => apiService.getCandidateCVs(validId, signal),
    enabled: Boolean(validId),
    staleTime: 30 * 1000,     // 30 seconds
    gcTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
    retry: 1,
  });
}

/**
 * Hook to fetch candidate/recruiter applications with 60s cache.
 */
export function useApplications(role: 'candidate' | 'recruiter' = 'candidate', userId?: string) {
  return useQuery<Application[], Error>({
    queryKey: QUERY_KEYS.applications(role, userId),
    queryFn: () => apiService.getApplications(role),
    staleTime: 60 * 1000,      // 1 minute
    gcTime: 5 * 60 * 1000,
    refetchOnWindowFocus: false,
  });
}

/**
 * Invalidation hooks for mutations.
 */
export function useInvalidateQueries() {
  const queryClient = useQueryClient();

  return {
    invalidateJobs: () => queryClient.invalidateQueries({ queryKey: ['jobs'] }),
    invalidateCVs: (candidateId?: string) =>
      queryClient.invalidateQueries({
        queryKey: candidateId ? QUERY_KEYS.cvs(candidateId) : ['cvs'],
      }),
    invalidateApplications: () => queryClient.invalidateQueries({ queryKey: ['applications'] }),
  };
}

