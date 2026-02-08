export interface ActionItem {
  task: string;
  owner?: string;
  deadline?: string;
  dependencies?: string[];
}

export interface RiskIssue {
  issue: string;
  type: 'risk' | 'open_issue' | 'assumption';
  impact?: 'high' | 'medium' | 'low';
  details?: string;
}

export interface DocumentAnalysisResponse {
  summary: string;
  action_items: ActionItem[];
  risks_and_open_issues: RiskIssue[];
  processing_time?: number;
  document_length?: number;
}

export interface DocumentAnalysisRequest {
  document_text: string;
}

export interface AnalysisError {
  message: string;
  details?: string;
}
