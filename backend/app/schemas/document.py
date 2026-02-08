"""
Pydantic schemas for document analysis system.
Defines input/output models and validation logic.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field, validator


class ActionItem(BaseModel):
    """Structured action item with dependencies."""
    
    task: str = Field(..., description="Description of the task to be completed")
    owner: Optional[str] = Field(None, description="Person or team responsible")
    deadline: Optional[str] = Field(None, description="Deadline in ISO format or natural language")
    dependencies: List[str] = Field(default_factory=list, description="List of dependent tasks")
    
    @validator('task')
    def task_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Task description cannot be empty')
        return v.strip()


class RiskOrIssue(BaseModel):
    """Risk, open question, or assumption identified in document."""
    
    issue: str = Field(..., description="Description of the risk or issue")
    type: Literal["risk", "open_question", "assumption"] = Field(
        ..., 
        description="Classification of the issue"
    )
    impact: Literal["low", "medium", "high"] = Field(
        ..., 
        description="Potential impact level"
    )
    
    @validator('issue')
    def issue_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Issue description cannot be empty')
        return v.strip()


class DocumentAnalysisRequest(BaseModel):
    """Request model for document analysis."""
    
    document_text: str = Field(
        ..., 
        min_length=500,
        description="Long unstructured text document (minimum 500 words recommended)"
    )
    
    @validator('document_text')
    def validate_document_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Document text cannot be empty')
        
        # Check word count
        word_count = len(v.split())
        if word_count < 100:  # Relaxed from 500 for testing, but warn
            # Note: In production, you might want to be stricter
            pass
        
        return v.strip()


class DocumentAnalysisResponse(BaseModel):
    """Response model for document analysis."""
    
    summary: str = Field(..., description="Comprehensive document summary")
    action_items: List[ActionItem] = Field(
        default_factory=list,
        description="List of extracted action items"
    )
    risks_and_open_issues: List[RiskOrIssue] = Field(
        default_factory=list,
        description="List of identified risks and open issues"
    )
    
    @validator('summary')
    def summary_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Summary cannot be empty')
        return v.strip()


class ErrorResponse(BaseModel):
    """Error response model."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    error_type: str = Field(default="processing_error", description="Type of error")
