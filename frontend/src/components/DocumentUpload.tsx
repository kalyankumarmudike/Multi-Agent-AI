import { useState } from 'react';
import { FileText, Upload, Loader2 } from 'lucide-react';
import { useDocumentAnalysis } from '@/hooks/useDocumentAnalysis';
import toast from 'react-hot-toast';

interface DocumentUploadProps {
  onAnalysisComplete: (data: any) => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({ onAnalysisComplete }) => {
  const [documentText, setDocumentText] = useState('');
  const [fileName, setFileName] = useState('');
  const mutation = useDocumentAnalysis();

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setFileName(file.name);
    const reader = new FileReader();

    reader.onload = (e) => {
      const text = e.target?.result as string;
      setDocumentText(text);
      toast.success('File loaded successfully!');
    };

    reader.onerror = () => {
      toast.error('Error reading file');
    };

    reader.readAsText(file);
  };

  const handleAnalyze = async () => {
    if (!documentText.trim()) {
      toast.error('Please enter or upload document text');
      return;
    }

    if (documentText.trim().split(/\s+/).length < 50) {
      toast.error('Document should be at least 50 words for meaningful analysis');
      return;
    }

    const analysisPromise = mutation.mutateAsync({ document_text: documentText });

    toast.promise(analysisPromise, {
      loading: 'Analyzing document with AI agents...',
      success: (data) => {
        onAnalysisComplete(data);
        return 'Analysis complete!';
      },
      error: (err) => {
        console.error('Analysis error:', err);
        return err.response?.data?.detail || 'Failed to analyze document';
      },
    });
  };

  const handleClear = () => {
    setDocumentText('');
    setFileName('');
    toast.success('Cleared');
  };

  const wordCount = documentText.trim().split(/\s+/).filter(Boolean).length;

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-3 bg-primary-100 rounded-lg">
            <FileText className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Document Analysis</h2>
            <p className="text-sm text-gray-600">Upload or paste your document for AI-powered analysis</p>
          </div>
        </div>

        {/* File Upload */}
        <div className="mb-6">
          <label
            htmlFor="file-upload"
            className="flex items-center justify-center w-full px-4 py-8 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:border-primary-500 hover:bg-primary-50 transition-all duration-200"
          >
            <div className="flex flex-col items-center space-y-2">
              <Upload className="w-8 h-8 text-gray-400" />
              <span className="text-sm font-medium text-gray-700">
                {fileName || 'Click to upload or drag & drop'}
              </span>
              <span className="text-xs text-gray-500">.txt, .md files supported</span>
            </div>
            <input
              id="file-upload"
              type="file"
              className="hidden"
              accept=".txt,.md"
              onChange={handleFileUpload}
              disabled={mutation.isPending}
            />
          </label>
        </div>

        {/* Text Area */}
        <div className="mb-4">
          <label htmlFor="document-text" className="block text-sm font-medium text-gray-700 mb-2">
            Document Text
          </label>
          <textarea
            id="document-text"
            value={documentText}
            onChange={(e) => setDocumentText(e.target.value)}
            placeholder="Paste your document text here... (minimum 50 words)"
            className="w-full h-64 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none font-mono text-sm"
            disabled={mutation.isPending}
          />
          <div className="flex justify-between items-center mt-2">
            <span className="text-xs text-gray-500">
              Word count: <span className="font-semibold">{wordCount}</span>
            </span>
            {wordCount > 0 && wordCount < 50 && (
              <span className="text-xs text-amber-600">⚠ Minimum 50 words recommended</span>
            )}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-3">
          <button
            onClick={handleAnalyze}
            disabled={mutation.isPending || !documentText.trim()}
            className="flex-1 flex items-center justify-center gap-2 px-6 py-3 bg-primary-600 text-white font-semibold rounded-lg hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors duration-200"
          >
            {mutation.isPending ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                Analyze Document
              </>
            )}
          </button>

          <button
            onClick={handleClear}
            disabled={mutation.isPending || !documentText.trim()}
            className="px-6 py-3 border border-gray-300 text-gray-700 font-semibold rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            Clear
          </button>
        </div>

        {/* Processing Info */}
        {mutation.isPending && (
          <div className="mt-6 p-4 bg-primary-50 border border-primary-200 rounded-lg">
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 text-primary-600 animate-spin" />
              <div>
                <p className="text-sm font-medium text-primary-900">AI Agents Working...</p>
                <p className="text-xs text-primary-700 mt-1">
                  Summary Agent → Action Agent → Risk Agent
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
