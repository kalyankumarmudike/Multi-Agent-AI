"""
Risk Agent - Risk & Open-Issues Detection.
Identifies risks, open questions, and assumptions with impact assessment.
"""

import logging
from typing import Dict, Any, List
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models import BaseChatModel

from ...utils.validation import get_validator, ValidationError
from ..prompts import PromptTemplates

logger = logging.getLogger(__name__)


class RiskAgent:
    """
    Risk analysis and open issues detection agent.
    
    Identifies unresolved questions, risks, and assumptions.
    Operates independently with shared context.
    """
    
    def __init__(self, llm: BaseChatModel):
        """
        Initialize risk agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
        self.validator = get_validator()
        self.agent_name = "RiskAgent"
    
    async def analyze(
        self,
        document_text: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze document and identify risks and open issues.
        
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
                SystemMessage(content=PromptTemplates.RISK_AGENT_SYSTEM),
                HumanMessage(
                    content=PromptTemplates.format_risk_prompt(
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
            risks_and_issues = self.validator.validate_risks_and_issues(parsed_data)
            
            logger.info(
                f"{self.agent_name}: Successfully identified {len(risks_and_issues)} risks/issues"
            )
            
            return {
                "success": True,
                "data": {"risks_and_open_issues": risks_and_issues},
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
                SystemMessage(content=PromptTemplates.RISK_AGENT_SYSTEM),
                HumanMessage(
                    content=PromptTemplates.format_risk_prompt(
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
            risks_and_issues = self.validator.validate_risks_and_issues(parsed_data)
            
            logger.info(
                f"{self.agent_name}: Successfully identified {len(risks_and_issues)} risks/issues"
            )
            
            return {
                "success": True,
                "data": {"risks_and_open_issues": risks_and_issues},
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
