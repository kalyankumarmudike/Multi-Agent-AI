import axios from 'axios';
import type { DocumentAnalysisRequest, DocumentAnalysisResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 120000, // 2 minutes for long documents
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.message);
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const documentApi = {
  analyzeDocument: async (data: DocumentAnalysisRequest): Promise<DocumentAnalysisResponse> => {
    const response = await apiClient.post<DocumentAnalysisResponse>('/analyze-document', data);
    return response.data;
  },

  healthCheck: async (): Promise<{ status: string }> => {
    const response = await apiClient.get('/');
    return response.data;
  },
};
