"""
LLM factory for creating LLM instances.
Supports multiple providers: OpenAI, Groq, OpenRouter.
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.language_models import BaseChatModel


class LLMFactory:
    """Factory for creating LLM instances based on provider."""
    
    @staticmethod
    def create_llm(
        provider: Optional[str] = None,
        temperature: float = 0.0,
        timeout: int = 30,
        max_retries: int = 3
    ) -> BaseChatModel:
        """
        Create LLM instance based on provider.
        
        Args:
            provider: LLM provider (openai, groq, openrouter)
            temperature: Sampling temperature
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            
        Returns:
            LLM instance
            
        Raises:
            ValueError: If provider is not supported or API key is missing
        """
        provider = provider or os.getenv("LLM_PROVIDER", "groq").lower()
        
        if provider == "openai":
            return LLMFactory._create_openai_llm(temperature, timeout, max_retries)
        elif provider == "groq":
            return LLMFactory._create_groq_llm(temperature, timeout, max_retries)
        elif provider == "openrouter":
            return LLMFactory._create_openrouter_llm(temperature, timeout, max_retries)
        else:
            raise ValueError(
                f"Unsupported LLM provider: {provider}. "
                f"Supported providers: openai, groq, openrouter"
            )
    
    @staticmethod
    def _create_openai_llm(
        temperature: float,
        timeout: int,
        max_retries: int
    ) -> ChatOpenAI:
        """Create OpenAI LLM instance."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            timeout=timeout,
            max_retries=max_retries,
            api_key=api_key
        )
    
    @staticmethod
    def _create_groq_llm(
        temperature: float,
        timeout: int,
        max_retries: int
    ) -> ChatGroq:
        """Create Groq LLM instance."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment")
        
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        
        return ChatGroq(
            model=model,
            temperature=temperature,
            timeout=timeout,
            max_retries=max_retries,
            groq_api_key=api_key
        )
    
    @staticmethod
    def _create_openrouter_llm(
        temperature: float,
        timeout: int,
        max_retries: int
    ) -> ChatOpenAI:
        """Create OpenRouter LLM instance (uses OpenAI-compatible API)."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
        
        model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3-sonnet")
        
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            timeout=timeout,
            max_retries=max_retries,
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )


def get_llm(temperature: float = 0.0, timeout: int = 30) -> BaseChatModel:
    """
    Convenience function to get LLM instance.
    
    Args:
        temperature: Sampling temperature
        timeout: Request timeout in seconds
        
    Returns:
        LLM instance
    """
    return LLMFactory.create_llm(temperature=temperature, timeout=timeout)
