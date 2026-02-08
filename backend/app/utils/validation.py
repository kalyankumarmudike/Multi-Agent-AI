"""
Validation utilities for agent outputs and final results.
"""

import json
import logging
from typing import Dict, Any, List, Optional
from ..schemas.document import ActionItem, RiskOrIssue, DocumentAnalysisResponse

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error."""
    pass


class OutputValidator:
    """Validates agent outputs and final results."""
    
    @staticmethod
    def validate_json(json_string: str) -> Dict[str, Any]:
        """
        Validate and parse JSON string.
        
        Args:
            json_string: JSON string to validate
            
        Returns:
            Parsed JSON dict
            
        Raises:
            ValidationError: If JSON is invalid
        """
        try:
            # Strip markdown code fences if present
            cleaned = json_string.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned[7:]
            if cleaned.startswith("```"):
                cleaned = cleaned[3:]
            if cleaned.endswith("```"):
                cleaned = cleaned[:-3]
            
            cleaned = cleaned.strip()
            
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            raise ValidationError(f"Invalid JSON: {str(e)}")
    
    @staticmethod
    def validate_summary(summary_data: Dict[str, Any]) -> str:
        """
        Validate summary agent output.
        
        Args:
            summary_data: Summary data from agent
            
        Returns:
            Validated summary string
            
        Raises:
            ValidationError: If summary is invalid
        """
        if not isinstance(summary_data, dict):
            raise ValidationError("Summary data must be a dictionary")
        
        if "summary" not in summary_data:
            raise ValidationError("Summary key not found in output")
        
        summary = summary_data["summary"]
        
        if not isinstance(summary, str):
            raise ValidationError("Summary must be a string")
        
        if not summary.strip():
            raise ValidationError("Summary cannot be empty")
        
        return summary.strip()
    
    @staticmethod
    def validate_action_items(action_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate action items agent output.
        
        Args:
            action_data: Action items data from agent
            
        Returns:
            Validated list of action items
            
        Raises:
            ValidationError: If action items are invalid
        """
        if not isinstance(action_data, dict):
            raise ValidationError("Action data must be a dictionary")
        
        if "action_items" not in action_data:
            raise ValidationError("action_items key not found in output")
        
        action_items = action_data["action_items"]
        
        if not isinstance(action_items, list):
            raise ValidationError("action_items must be a list")
        
        validated_items = []
        
        for idx, item in enumerate(action_items):
            try:
                # Validate using Pydantic model
                validated_item = ActionItem(**item)
                validated_items.append(validated_item.model_dump())
            except Exception as e:
                logger.warning(f"Invalid action item at index {idx}: {e}")
                # Skip invalid items instead of failing completely
                continue
        
        return validated_items
    
    @staticmethod
    def validate_risks_and_issues(risk_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Validate risks and open issues agent output.
        
        Args:
            risk_data: Risk data from agent
            
        Returns:
            Validated list of risks and issues
            
        Raises:
            ValidationError: If risks/issues are invalid
        """
        if not isinstance(risk_data, dict):
            raise ValidationError("Risk data must be a dictionary")
        
        if "risks_and_open_issues" not in risk_data:
            raise ValidationError("risks_and_open_issues key not found in output")
        
        risks = risk_data["risks_and_open_issues"]
        
        if not isinstance(risks, list):
            raise ValidationError("risks_and_open_issues must be a list")
        
        validated_risks = []
        
        for idx, item in enumerate(risks):
            try:
                # Validate using Pydantic model
                validated_risk = RiskOrIssue(**item)
                validated_risks.append(validated_risk.model_dump())
            except Exception as e:
                logger.warning(f"Invalid risk/issue at index {idx}: {e}")
                # Skip invalid items instead of failing completely
                continue
        
        return validated_risks
    
    @staticmethod
    def validate_final_output(
        summary: str,
        action_items: List[Dict[str, Any]],
        risks_and_open_issues: List[Dict[str, Any]]
    ) -> DocumentAnalysisResponse:
        """
        Validate final combined output.
        
        Args:
            summary: Document summary
            action_items: List of action items
            risks_and_open_issues: List of risks and issues
            
        Returns:
            Validated DocumentAnalysisResponse
            
        Raises:
            ValidationError: If output is invalid
        """
        try:
            response = DocumentAnalysisResponse(
                summary=summary,
                action_items=[ActionItem(**item) for item in action_items],
                risks_and_open_issues=[RiskOrIssue(**item) for item in risks_and_open_issues]
            )
            return response
        except Exception as e:
            raise ValidationError(f"Final output validation failed: {str(e)}")


# Singleton instance
_validator_instance = None


def get_validator() -> OutputValidator:
    """Get or create validator instance."""
    global _validator_instance
    if _validator_instance is None:
        _validator_instance = OutputValidator()
    return _validator_instance
