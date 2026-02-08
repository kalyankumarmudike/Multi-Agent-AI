import { useMutation, useQuery } from '@tanstack/react-query';
import { documentApi } from '@/api/client';
import type { DocumentAnalysisRequest } from '@/types';

export const useDocumentAnalysis = () => {
  return useMutation({
    mutationFn: (data: DocumentAnalysisRequest) => documentApi.analyzeDocument(data),
    retry: 1,
  });
};

export const useHealthCheck = () => {
  return useQuery({
    queryKey: ['health'],
    queryFn: documentApi.healthCheck,
    retry: 3,
    refetchInterval: 30000, // Check every 30 seconds
  });
};
