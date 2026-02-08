"""
LangGraph state definitions.
Defines the central state that flows through the orchestration graph.
"""

from typing import List, Dict, Optional, TypedDict, Any


class DocumentState(TypedDict):
    """
    Central state for document processing workflow.
    This state is shared across all nodes in the LangGraph.
    """
    
    # Input
    document_text: str
    
    # Chunking
    chunks: List[str]
    chunk_summaries: List[str]
    
    # Consolidated context for agents
    consolidated_context: str
    
    # Agent outputs
    summary: Optional[str]
    action_items: Optional[List[Dict[str, Any]]]
    risks_and_open_issues: Optional[List[Dict[str, Any]]]
    
    # Intermediate processing
    intermediate_notes: Dict[str, Any]
    
    # Metadata
    processing_metadata: Dict[str, Any]
    
    # Error handling
    error: Optional[str]
    retry_count: int


class AgentOutput(TypedDict):
    """Standard output format for agents."""
    
    success: bool
    data: Optional[Dict[str, Any]]
    error: Optional[str]
    agent_name: str
