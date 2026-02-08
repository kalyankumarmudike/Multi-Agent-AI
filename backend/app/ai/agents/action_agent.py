"""
Action Agent - Action & Dependency Extraction.
Extracts structured tasks with owners, deadlines, and dependencies.
"""

import logging
from typing import Dict, Any, List
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.language_models import BaseChatModel

from ...utils.validation import get_validator, ValidationError
from ..prompts import PromptTemplates

logger = logging.getLogger(__name__)


class ActionAgent:
    """
    Action and dependency extraction agent.
    
    Identifies tasks, owners, deadlines, and dependencies.
    Operates independently with shared context.
    """
    
    def __init__(self, llm: BaseChatModel):
        """
        Initialize action agent.
        
        Args:
            llm: Language model instance
        """
        self.llm = llm
        self.validator = get_validator()
        self.agent_name = "ActionAgent"
    
    async def analyze(
        self,
        document_text: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze document and extract action items.
        
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
                SystemMessage(content=PromptTemplates.ACTION_AGENT_SYSTEM),
                HumanMessage(
                    content=PromptTemplates.format_action_prompt(
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
            action_items = self.validator.validate_action_items(parsed_data)
            
            logger.info(
                f"{self.agent_name}: Successfully extracted {len(action_items)} action items"
            )
            
            return {
                "success": True,
                "data": {"action_items": action_items},
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
                SystemMessage(content=PromptTemplates.ACTION_AGENT_SYSTEM),
                HumanMessage(
                    content=PromptTemplates.format_action_prompt(
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
            action_items = self.validator.validate_action_items(parsed_data)
            
            logger.info(
                f"{self.agent_name}: Successfully extracted {len(action_items)} action items"
            )
            
            return {
                "success": True,
                "data": {"action_items": action_items},
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
