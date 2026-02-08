"""
LangGraph Orchestrator - Central coordination for multi-agent document analysis.
Implements the complete workflow with all nodes and state management.
"""

import asyncio
import logging
import os
from typing import Dict, Any, List
from langgraph.graph import StateGraph, END
from langchain_core.language_models import BaseChatModel

from ..models.state import DocumentState, AgentOutput
from ..utils.chunking import get_chunker
from ..utils.llm_factory import get_llm
from ..utils.validation import get_validator, ValidationError
from .agents import SummaryAgent, ActionAgent, RiskAgent

logger = logging.getLogger(__name__)


class DocumentOrchestrator:
    """
    Central orchestrator using LangGraph for multi-agent coordination.
    
    Workflow:
    1. Document Chunking
    2. Context Building
    3. Agent Execution (Summary, Action, Risk)
    4. Aggregation
    5. Validation
    6. Output / Error Handling
    """
    
    def __init__(self, llm: BaseChatModel = None):
        """
        Initialize orchestrator.
        
        Args:
            llm: Language model instance (optional, will use factory if not provided)
        """
        self.llm = llm or get_llm()
        self.chunker = get_chunker()
        self.validator = get_validator()
        
        # Initialize agents
        self.summary_agent = SummaryAgent(self.llm)
        self.action_agent = ActionAgent(self.llm)
        self.risk_agent = RiskAgent(self.llm)
        
        # Build graph
        self.graph = self._build_graph()
        
        # Configuration
        self.parallel_agents = os.getenv("PARALLEL_AGENTS", "true").lower() == "true"
        
        logger.info("DocumentOrchestrator initialized")
    
    def _build_graph(self) -> StateGraph:
        """
        Build LangGraph workflow.
        
        Returns:
            Compiled StateGraph
        """
        # Create state graph
        workflow = StateGraph(DocumentState)
        
        # Add nodes
        workflow.add_node("chunk_document", self._chunk_document_node)
        workflow.add_node("build_context", self._build_context_node)
        workflow.add_node("summary_agent", self._summary_agent_node)
        workflow.add_node("action_agent", self._action_agent_node)
        workflow.add_node("risk_agent", self._risk_agent_node)
        workflow.add_node("aggregate", self._aggregate_node)
        workflow.add_node("validate", self._validate_node)
        workflow.add_node("error_handler", self._error_handler_node)
        
        # Set entry point
        workflow.set_entry_point("chunk_document")
        
        # Define edges
        workflow.add_edge("chunk_document", "build_context")
        workflow.add_edge("build_context", "summary_agent")
        workflow.add_edge("summary_agent", "action_agent")
        workflow.add_edge("action_agent", "risk_agent")
        workflow.add_edge("risk_agent", "aggregate")
        workflow.add_edge("aggregate", "validate")
        
        # Conditional edge from validate
        workflow.add_conditional_edges(
            "validate",
            self._should_error_handle,
            {
                "error": "error_handler",
                "success": END
            }
        )
        
        workflow.add_edge("error_handler", END)
        
        # Compile graph
        return workflow.compile()
    
    def _chunk_document_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Chunk document into manageable pieces.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with chunks
        """
        try:
            logger.info("Node: chunk_document - Starting")
            
            document_text = state["document_text"]
            chunks = self.chunker.chunk_document(document_text)
            
            logger.info(f"Node: chunk_document - Created {len(chunks)} chunks")
            
            state["chunks"] = chunks
            state["chunk_summaries"] = []
            
            return state
            
        except Exception as e:
            logger.error(f"Node: chunk_document - Error: {e}", exc_info=True)
            state["error"] = f"Chunking failed: {str(e)}"
            return state
    
    def _build_context_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Build consolidated context from chunks.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with consolidated context
        """
        try:
            logger.info("Node: build_context - Starting")
            
            chunks = state.get("chunks", [])
            
            if not chunks:
                logger.warning("Node: build_context - No chunks found")
                state["consolidated_context"] = state["document_text"]
                return state
            
            # Create chunk summaries for context
            chunk_summaries = []
            for idx, chunk in enumerate(chunks):
                summary = self.chunker.create_chunk_summary(chunk)
                chunk_summaries.append(f"Chunk {idx + 1}: {summary}")
            
            state["chunk_summaries"] = chunk_summaries
            
            # Build consolidated context
            if len(chunks) == 1:
                consolidated_context = ""
            else:
                consolidated_context = (
                    f"Document split into {len(chunks)} chunks. "
                    f"Chunk summaries:\n" + "\n".join(chunk_summaries)
                )
            
            state["consolidated_context"] = consolidated_context
            
            logger.info("Node: build_context - Context built successfully")
            
            return state
            
        except Exception as e:
            logger.error(f"Node: build_context - Error: {e}", exc_info=True)
            state["error"] = f"Context building failed: {str(e)}"
            return state
    
    def _summary_agent_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Execute summary agent.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with summary
        """
        try:
            logger.info("Node: summary_agent - Starting")
            
            # Use full document text or first chunk
            chunks = state.get("chunks", [])
            document_text = " ".join(chunks) if chunks else state["document_text"]
            
            context = state.get("consolidated_context", "")
            
            # Execute agent (sync for now, can be async)
            result = self.summary_agent.analyze_sync(
                document_text=document_text,
                context=context
            )
            
            if result["success"]:
                state["summary"] = result["data"]["summary"]
                logger.info("Node: summary_agent - Success")
            else:
                logger.error(f"Node: summary_agent - Failed: {result['error']}")
                state["error"] = f"Summary agent failed: {result['error']}"
            
            return state
            
        except Exception as e:
            logger.error(f"Node: summary_agent - Error: {e}", exc_info=True)
            state["error"] = f"Summary agent error: {str(e)}"
            return state
    
    def _action_agent_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Execute action extraction agent.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with action items
        """
        try:
            logger.info("Node: action_agent - Starting")
            
            # Use full document text or join chunks
            chunks = state.get("chunks", [])
            document_text = " ".join(chunks) if chunks else state["document_text"]
            
            context = state.get("consolidated_context", "")
            
            # Execute agent
            result = self.action_agent.analyze_sync(
                document_text=document_text,
                context=context
            )
            
            if result["success"]:
                state["action_items"] = result["data"]["action_items"]
                logger.info(
                    f"Node: action_agent - Success, "
                    f"found {len(state['action_items'])} items"
                )
            else:
                logger.error(f"Node: action_agent - Failed: {result['error']}")
                state["error"] = f"Action agent failed: {result['error']}"
            
            return state
            
        except Exception as e:
            logger.error(f"Node: action_agent - Error: {e}", exc_info=True)
            state["error"] = f"Action agent error: {str(e)}"
            return state
    
    def _risk_agent_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Execute risk detection agent.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with risks and issues
        """
        try:
            logger.info("Node: risk_agent - Starting")
            
            # Use full document text or join chunks
            chunks = state.get("chunks", [])
            document_text = " ".join(chunks) if chunks else state["document_text"]
            
            context = state.get("consolidated_context", "")
            
            # Execute agent
            result = self.risk_agent.analyze_sync(
                document_text=document_text,
                context=context
            )
            
            if result["success"]:
                state["risks_and_open_issues"] = result["data"]["risks_and_open_issues"]
                logger.info(
                    f"Node: risk_agent - Success, "
                    f"found {len(state['risks_and_open_issues'])} items"
                )
            else:
                logger.error(f"Node: risk_agent - Failed: {result['error']}")
                state["error"] = f"Risk agent failed: {result['error']}"
            
            return state
            
        except Exception as e:
            logger.error(f"Node: risk_agent - Error: {e}", exc_info=True)
            state["error"] = f"Risk agent error: {str(e)}"
            return state
    
    def _aggregate_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Aggregate results from all agents.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with aggregated results
        """
        try:
            logger.info("Node: aggregate - Starting")
            
            # Check if all required outputs are present
            if not state.get("summary"):
                logger.warning("Node: aggregate - Missing summary")
                state["error"] = "Missing summary from agent"
                return state
            
            if state.get("action_items") is None:
                logger.warning("Node: aggregate - Missing action items")
                state["action_items"] = []
            
            if state.get("risks_and_open_issues") is None:
                logger.warning("Node: aggregate - Missing risks and issues")
                state["risks_and_open_issues"] = []
            
            # Store metadata
            state["processing_metadata"] = {
                "total_chunks": len(state.get("chunks", [])),
                "action_items_count": len(state.get("action_items", [])),
                "risks_count": len(state.get("risks_and_open_issues", []))
            }
            
            logger.info("Node: aggregate - Aggregation complete")
            
            return state
            
        except Exception as e:
            logger.error(f"Node: aggregate - Error: {e}", exc_info=True)
            state["error"] = f"Aggregation failed: {str(e)}"
            return state
    
    def _validate_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Validate final output.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with validation status
        """
        try:
            logger.info("Node: validate - Starting")
            
            # Check for errors
            if state.get("error"):
                logger.error(f"Node: validate - Error in state: {state['error']}")
                return state
            
            # Validate final output
            summary = state.get("summary", "")
            action_items = state.get("action_items", [])
            risks_and_open_issues = state.get("risks_and_open_issues", [])
            
            # Use validator to ensure output is correct
            validated_response = self.validator.validate_final_output(
                summary=summary,
                action_items=action_items,
                risks_and_open_issues=risks_and_open_issues
            )
            
            logger.info("Node: validate - Validation successful")
            
            return state
            
        except ValidationError as e:
            logger.error(f"Node: validate - Validation failed: {e}")
            state["error"] = f"Output validation failed: {str(e)}"
            return state
        
        except Exception as e:
            logger.error(f"Node: validate - Error: {e}", exc_info=True)
            state["error"] = f"Validation error: {str(e)}"
            return state
    
    def _error_handler_node(self, state: DocumentState) -> DocumentState:
        """
        Node: Handle errors gracefully.
        
        Args:
            state: Current state
            
        Returns:
            Updated state with error handling
        """
        logger.error(f"Node: error_handler - Processing error: {state.get('error')}")
        
        # Ensure we have at least default values
        if not state.get("summary"):
            state["summary"] = "Error: Unable to generate summary"
        
        if state.get("action_items") is None:
            state["action_items"] = []
        
        if state.get("risks_and_open_issues") is None:
            state["risks_and_open_issues"] = []
        
        return state
    
    def _should_error_handle(self, state: DocumentState) -> str:
        """
        Decide whether to route to error handler or end.
        
        Args:
            state: Current state
            
        Returns:
            Next node name
        """
        if state.get("error"):
            return "error"
        return "success"
    
    async def analyze_document_async(self, document_text: str) -> Dict[str, Any]:
        """
        Analyze document asynchronously.
        
        Args:
            document_text: Document text to analyze
            
        Returns:
            Analysis results
        """
        logger.info("Starting document analysis (async)")
        
        # Initialize state
        initial_state: DocumentState = {
            "document_text": document_text,
            "chunks": [],
            "chunk_summaries": [],
            "consolidated_context": "",
            "summary": None,
            "action_items": None,
            "risks_and_open_issues": None,
            "intermediate_notes": {},
            "processing_metadata": {},
            "error": None,
            "retry_count": 0
        }
        
        # Execute graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Extract results
        result = {
            "summary": final_state.get("summary", ""),
            "action_items": final_state.get("action_items", []),
            "risks_and_open_issues": final_state.get("risks_and_open_issues", [])
        }
        
        if final_state.get("error"):
            logger.warning(f"Analysis completed with errors: {final_state['error']}")
            result["_error"] = final_state["error"]
        
        logger.info("Document analysis complete")
        
        return result
    
    def analyze_document(self, document_text: str) -> Dict[str, Any]:
        """
        Analyze document synchronously.
        
        Args:
            document_text: Document text to analyze
            
        Returns:
            Analysis results
        """
        logger.info("Starting document analysis (sync)")
        
        # Initialize state
        initial_state: DocumentState = {
            "document_text": document_text,
            "chunks": [],
            "chunk_summaries": [],
            "consolidated_context": "",
            "summary": None,
            "action_items": None,
            "risks_and_open_issues": None,
            "intermediate_notes": {},
            "processing_metadata": {},
            "error": None,
            "retry_count": 0
        }
        
        # Execute graph
        final_state = self.graph.invoke(initial_state)
        
        # Extract results
        result = {
            "summary": final_state.get("summary", ""),
            "action_items": final_state.get("action_items", []),
            "risks_and_open_issues": final_state.get("risks_and_open_issues", [])
        }
        
        if final_state.get("error"):
            logger.warning(f"Analysis completed with errors: {final_state['error']}")
            result["_error"] = final_state["error"]
        
        logger.info("Document analysis complete")
        
        return result


# Singleton instance
_orchestrator_instance = None


def get_orchestrator() -> DocumentOrchestrator:
    """Get or create orchestrator instance."""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = DocumentOrchestrator()
    return _orchestrator_instance
