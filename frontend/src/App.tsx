import { useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Toaster } from 'react-hot-toast';
import { DocumentUpload } from '@/components/DocumentUpload';
import { AnalysisResults } from '@/components/AnalysisResults';
import { useHealthCheck } from '@/hooks/useDocumentAnalysis';
import { Brain, AlertCircle, CheckCircle2 } from 'lucide-react';
import type { DocumentAnalysisResponse } from '@/types';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function AppContent() {
  const [analysisData, setAnalysisData] = useState<DocumentAnalysisResponse | null>(null);
  const { data: healthData, isLoading: healthLoading, isError: healthError } = useHealthCheck();

  const handleReset = () => {
    setAnalysisData(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: '#363636',
            color: '#fff',
          },
          success: {
            duration: 3000,
            iconTheme: {
              primary: '#10b981',
              secondary: '#fff',
            },
          },
          error: {
            duration: 5000,
            iconTheme: {
              primary: '#ef4444',
              secondary: '#fff',
            },
          },
        }}
      />

      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-purple-600 rounded-lg">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900">
                  Multi-Agent Document Intelligence
                </h1>
                <p className="text-sm text-gray-600">
                  Powered by LangGraph & AI Agents
                </p>
              </div>
            </div>

            {/* Health Status */}
            <div className="flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-50 border border-gray-200">
              {healthLoading ? (
                <>
                  <div className="w-2 h-2 bg-amber-400 rounded-full animate-pulse" />
                  <span className="text-sm text-gray-700">Checking...</span>
                </>
              ) : healthError ? (
                <>
                  <AlertCircle className="w-4 h-4 text-red-500" />
                  <span className="text-sm text-red-700">API Offline</span>
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4 text-green-500" />
                  <span className="text-sm text-green-700">API Ready</span>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Info Banner */}
        {!analysisData && (
          <div className="mb-8 bg-primary-50 border border-primary-200 rounded-xl p-6">
            <div className="flex items-start gap-4">
              <Brain className="w-6 h-6 text-primary-600 flex-shrink-0 mt-1" />
              <div>
                <h3 className="text-lg font-semibold text-primary-900 mb-2">
                  How It Works
                </h3>
                <p className="text-sm text-primary-800 mb-3">
                  Our system uses three specialized AI agents working in sequence to deeply analyze your documents:
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div className="bg-white rounded-lg p-3 border border-primary-200">
                    <p className="font-semibold text-primary-900 mb-1">1. Summary Agent</p>
                    <p className="text-gray-700">Generates context-aware summaries</p>
                  </div>
                  <div className="bg-white rounded-lg p-3 border border-primary-200">
                    <p className="font-semibold text-primary-900 mb-1">2. Action Agent</p>
                    <p className="text-gray-700">Extracts tasks & dependencies</p>
                  </div>
                  <div className="bg-white rounded-lg p-3 border border-primary-200">
                    <p className="font-semibold text-primary-900 mb-1">3. Risk Agent</p>
                    <p className="text-gray-700">Identifies risks & open issues</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Content */}
        {analysisData ? (
          <AnalysisResults data={analysisData} onReset={handleReset} />
        ) : (
          <DocumentUpload onAnalysisComplete={setAnalysisData} />
        )}
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center text-sm text-gray-600">
            <p>Built with React 18, TypeScript, Tailwind CSS & LangGraph</p>
            <p className="mt-1">
              Backend: FastAPI + Groq AI + ChromaDB
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;
