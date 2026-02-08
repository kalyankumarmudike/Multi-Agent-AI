"""
API endpoints for document analysis.
"""

import logging
import time
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from ..schemas.document import (
    DocumentAnalysisRequest,
    DocumentAnalysisResponse,
    ErrorResponse
)
from ..ai.orchestrator import get_orchestrator

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/analyze-document",
    response_model=DocumentAnalysisResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def analyze_document(request: DocumentAnalysisRequest) -> DocumentAnalysisResponse:
    """
    Analyze a document and extract structured insights.
    
    This endpoint orchestrates multiple AI agents to:
    - Generate a comprehensive summary
    - Extract action items with owners, deadlines, and dependencies
    - Identify risks, open questions, and assumptions
    
    Args:
        request: Document analysis request with document text
        
    Returns:
        Structured analysis results
        
    Raises:
        HTTPException: If processing fails
    """
    start_time = time.time()
    
    try:
        logger.info("Received document analysis request")
        
        # Get orchestrator
        orchestrator = get_orchestrator()
        
        # Process document
        result = await orchestrator.analyze_document_async(request.document_text)
        
        # Check for errors
        if "_error" in result:
            logger.warning(f"Analysis completed with warnings: {result['_error']}")
            # Don't fail the request, just log the warning
            # Remove error from response
            del result["_error"]
        
        # Create response
        response = DocumentAnalysisResponse(**result)
        
        elapsed_time = time.time() - start_time
        logger.info(f"Document analysis completed in {elapsed_time:.2f}s")
        
        return response
        
    except ValueError as e:
        logger.error(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal processing error: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "service": "Multi-Agent Document Intelligence System"
    }


@router.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        API information
    """
    return {
        "service": "Multi-Agent Document Intelligence System",
        "version": "1.0.0",
        "description": "LangGraph-based multi-agent system for document analysis",
        "endpoints": {
            "analyze": "/analyze-document",
            "health": "/health",
            "docs": "/docs"
        }
    }
