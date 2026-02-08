import { CheckCircle, AlertTriangle, ListTodo, FileText, Clock, TrendingUp } from 'lucide-react';
import type { DocumentAnalysisResponse } from '@/types';

interface AnalysisResultsProps {
  data: DocumentAnalysisResponse;
  onReset: () => void;
}

export const AnalysisResults: React.FC<AnalysisResultsProps> = ({ data, onReset }) => {
  const getImpactColor = (impact?: string) => {
    switch (impact) {
      case 'high':
        return 'text-red-700 bg-red-100 border-red-200';
      case 'medium':
        return 'text-amber-700 bg-amber-100 border-amber-200';
      case 'low':
        return 'text-blue-700 bg-blue-100 border-blue-200';
      default:
        return 'text-gray-700 bg-gray-100 border-gray-200';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'risk':
        return <AlertTriangle className="w-4 h-4" />;
      case 'open_issue':
        return <FileText className="w-4 h-4" />;
      case 'assumption':
        return <TrendingUp className="w-4 h-4" />;
      default:
        return <AlertTriangle className="w-4 h-4" />;
    }
  };

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-green-100 rounded-lg">
            <CheckCircle className="w-6 h-6 text-green-600" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Analysis Complete</h2>
            <p className="text-sm text-gray-600">Multi-agent analysis results</p>
          </div>
        </div>
        <button
          onClick={onReset}
          className="px-4 py-2 text-sm font-medium text-primary-600 border border-primary-600 rounded-lg hover:bg-primary-50 transition-colors"
        >
          New Analysis
        </button>
      </div>

      {/* Stats */}
      {(data.processing_time || data.document_length) && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {data.processing_time && (
            <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
              <div className="flex items-center gap-2">
                <Clock className="w-5 h-5 text-primary-600" />
                <div>
                  <p className="text-sm text-gray-600">Processing Time</p>
                  <p className="text-xl font-bold text-gray-900">{data.processing_time.toFixed(2)}s</p>
                </div>
              </div>
            </div>
          )}
          {data.document_length && (
            <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
              <div className="flex items-center gap-2">
                <FileText className="w-5 h-5 text-primary-600" />
                <div>
                  <p className="text-sm text-gray-600">Document Length</p>
                  <p className="text-xl font-bold text-gray-900">{data.document_length} words</p>
                </div>
              </div>
            </div>
          )}
          <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
            <div className="flex items-center gap-2">
              <ListTodo className="w-5 h-5 text-primary-600" />
              <div>
                <p className="text-sm text-gray-600">Items Found</p>
                <p className="text-xl font-bold text-gray-900">
                  {data.action_items.length + data.risks_and_open_issues.length}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Summary */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-bold text-gray-900">Executive Summary</h3>
        </div>
        <div className="prose max-w-none">
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{data.summary}</p>
        </div>
      </div>

      {/* Action Items */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <ListTodo className="w-5 h-5 text-primary-600" />
          <h3 className="text-lg font-bold text-gray-900">Action Items & Dependencies</h3>
          <span className="ml-auto text-sm font-semibold text-gray-600">
            {data.action_items.length} items
          </span>
        </div>

        {data.action_items.length === 0 ? (
          <p className="text-gray-500 italic">No action items identified</p>
        ) : (
          <div className="space-y-4">
            {data.action_items.map((item, index) => (
              <div
                key={index}
                className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
              >
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 w-8 h-8 flex items-center justify-center bg-primary-100 text-primary-700 rounded-full font-semibold text-sm">
                    {index + 1}
                  </div>
                  <div className="flex-1 space-y-2">
                    <p className="font-semibold text-gray-900">{item.task}</p>

                    <div className="flex flex-wrap gap-3 text-sm">
                      {item.owner && (
                        <div className="flex items-center gap-1 text-gray-600">
                          <span className="font-medium">Owner:</span>
                          <span>{item.owner}</span>
                        </div>
                      )}
                      {item.deadline && (
                        <div className="flex items-center gap-1 text-gray-600">
                          <Clock className="w-4 h-4" />
                          <span className="font-medium">Deadline:</span>
                          <span>{item.deadline}</span>
                        </div>
                      )}
                    </div>

                    {item.dependencies && item.dependencies.length > 0 && (
                      <div className="mt-2">
                        <p className="text-sm font-medium text-gray-700 mb-1">Dependencies:</p>
                        <div className="flex flex-wrap gap-2">
                          {item.dependencies.map((dep, depIndex) => (
                            <span
                              key={depIndex}
                              className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-700 rounded-full border border-gray-200"
                            >
                              {dep}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Risks and Issues */}
      <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
        <div className="flex items-center gap-2 mb-4">
          <AlertTriangle className="w-5 h-5 text-amber-600" />
          <h3 className="text-lg font-bold text-gray-900">Risks & Open Issues</h3>
          <span className="ml-auto text-sm font-semibold text-gray-600">
            {data.risks_and_open_issues.length} items
          </span>
        </div>

        {data.risks_and_open_issues.length === 0 ? (
          <p className="text-gray-500 italic">No risks or open issues identified</p>
        ) : (
          <div className="space-y-4">
            {data.risks_and_open_issues.map((item, index) => (
              <div
                key={index}
                className={`p-4 border rounded-lg ${getImpactColor(item.impact)}`}
              >
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0 pt-1">{getTypeIcon(item.type)}</div>
                  <div className="flex-1 space-y-2">
                    <div className="flex items-start justify-between gap-2">
                      <p className="font-semibold">{item.issue}</p>
                      <div className="flex gap-2">
                        <span className="px-2 py-1 text-xs font-semibold uppercase rounded">
                          {item.type.replace('_', ' ')}
                        </span>
                        {item.impact && (
                          <span className="px-2 py-1 text-xs font-semibold uppercase rounded">
                            {item.impact} impact
                          </span>
                        )}
                      </div>
                    </div>
                    {item.details && (
                      <p className="text-sm opacity-90">{item.details}</p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
