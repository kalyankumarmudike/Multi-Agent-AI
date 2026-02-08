"""
FastAPI application entry point.
Multi-Agent Deep Document Intelligence System.
"""

import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api.endpoints import router

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler for startup and shutdown.
    """
    # Startup
    logger.info("Starting Multi-Agent Document Intelligence System")
    logger.info(f"LLM Provider: {os.getenv('LLM_PROVIDER', 'groq')}")
    
    # Verify API key
    provider = os.getenv("LLM_PROVIDER", "groq").lower()
    key_var = f"{provider.upper()}_API_KEY"
    
    if not os.getenv(key_var):
        logger.warning(f"{key_var} not found in environment. API calls will fail.")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Multi-Agent Document Intelligence System")


# Create FastAPI app
app = FastAPI(
    title="Multi-Agent Document Intelligence System",
    description=(
        "A production-ready multi-agent AI system using LangGraph for orchestrating "
        "autonomous agents that analyze long unstructured documents and generate "
        "structured insights."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router, tags=["Document Analysis"])


# Error handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return {
        "error": "Internal server error",
        "detail": str(exc)
    }


if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
