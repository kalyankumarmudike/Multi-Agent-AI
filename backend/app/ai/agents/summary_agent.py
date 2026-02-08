"""
Summary Agent - Context-Aware Document Summarization.
Generates comprehensive summaries preserving intent and critical decisions.
"""

import logging
from typing import Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models import BaseChatModel

from ...utils.validation import get_validator, ValidationError
from ..prompts import PromptTemplates

logger = logging.getLogger(__name__)


class SummaryAgent:
    """
    Context-aware document summarization agent.
    
    Operates independently but uses shared context from chunking.
    Returns structured JSON output.
    """
    
    def __init__(self, llm: BaseChatModel):
        """
        Initialize summary agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
        self.validator = get_validator()
        self.agent_name = "SummaryAgent"
    
    async def analyze(
        self,
        document_text: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze document and generate summary.
        
        Args:
            document_text: Original or chunked document text
            context: Additional context from chunking/processing
            
        Returns:
            Dict with success status, data, and error info
        """
        try:
            logger.info(f"{self.agent_name}: Starting analysis")
            
            # Prepare messages
            messages = [
                SystemMessage(content=PromptTemplates.SUMMARY_AGENT_SYSTEM),
                HumanMessage(
                    content=PromptTemplates.format_summary_prompt(
                        context=context,
                        document_text=document_text
                    )
                )
            ]
            
            # Call LLM
            response = await self.llm.ainvoke(messages)
            response_text = response.content
            
            logger.debug(f"{self.agent_name}: Raw response: {response_text[:200]}...")
            
            # Parse and validate JSON
            parsed_data = self.validator.validate_json(response_text)
            summary = self.validator.validate_summary(parsed_data)
            
            logger.info(f"{self.agent_name}: Successfully generated summary")
            
            return {
                "success": True,
                "data": {"summary": summary},
                "error": None,
                "agent_name": self.agent_name
            }
            
        except ValidationError as e:
            logger.error(f"{self.agent_name}: Validation error: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Validation failed: {str(e)}",
                "agent_name": self.agent_name
            }
        
        except Exception as e:
            logger.error(f"{self.agent_name}: Unexpected error: {e}", exc_info=True)
            return {
                "success": False,
                "data": None,
                "error": f"Processing failed: {str(e)}",
                "agent_name": self.agent_name
            }
    
    def analyze_sync(
        self,
        document_text: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Synchronous version of analyze.
        
        Args:
            document_text: Original or chunked document text
            context: Additional context from chunking/processing
            
        Returns:
            Dict with success status, data, and error info
        """
        try:
            logger.info(f"{self.agent_name}: Starting analysis (sync)")
            
            # Prepare messages
            messages = [
                SystemMessage(content=PromptTemplates.SUMMARY_AGENT_SYSTEM),
                HumanMessage(
                    content=PromptTemplates.format_summary_prompt(
                        context=context,
                        document_text=document_text
                    )
                )
            ]
            
            # Call LLM
            response = self.llm.invoke(messages)
            response_text = response.content
            
            logger.debug(f"{self.agent_name}: Raw response: {response_text[:200]}...")
            
            # Parse and validate JSON
            parsed_data = self.validator.validate_json(response_text)
            summary = self.validator.validate_summary(parsed_data)
            
            logger.info(f"{self.agent_name}: Successfully generated summary")
            
            return {
                "success": True,
                "data": {"summary": summary},
                "error": None,
                "agent_name": self.agent_name
            }
            
        except ValidationError as e:
            logger.error(f"{self.agent_name}: Validation error: {e}")
            return {
                "success": False,
                "data": None,
                "error": f"Validation failed: {str(e)}",
                "agent_name": self.agent_name
            }
        
        except Exception as e:
            logger.error(f"{self.agent_name}: Unexpected error: {e}", exc_info=True)
            return {
                "success": False,
                "data": None,
                "error": f"Processing failed: {str(e)}",
                "agent_name": self.agent_name
            }
