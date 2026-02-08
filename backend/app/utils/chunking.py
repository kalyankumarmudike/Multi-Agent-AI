"""
Document chunking utility.
Implements semantic chunking for long documents.
"""

import re
from typing import List
import tiktoken


class DocumentChunker:
    """
    Chunks documents into semantically meaningful segments.
    Maintains context and ordering for downstream processing.
    """
    
    def __init__(
        self,
        min_chunk_size: int = 800,
        max_chunk_size: int = 1200,
        encoding_name: str = "cl100k_base"
    ):
        self.min_chunk_size = min_chunk_size
        self.max_chunk_size = max_chunk_size
        try:
            self.encoding = tiktoken.get_encoding(encoding_name)
        except Exception:
            # Fallback to simple word counting
            self.encoding = None
    
    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoding:
            return len(self.encoding.encode(text))
        else:
            # Fallback: approximate 1.3 words per token
            return int(len(text.split()) * 1.3)
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences using regex."""
        # Simple sentence splitter
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_document(self, document_text: str) -> List[str]:
        """
        Chunk document into semantic segments.
        
        Strategy:
        1. Split into sentences
        2. Group sentences into chunks based on token count
        3. Maintain semantic coherence
        4. Ensure chunks are within size limits
        
        Args:
            document_text: Raw document text
            
        Returns:
            List of text chunks
        """
        if not document_text or not document_text.strip():
            return []
        
        # Check if document is small enough to process as single chunk
        total_tokens = self.count_tokens(document_text)
        if total_tokens <= self.max_chunk_size:
            return [document_text]
        
        # Split into sentences
        sentences = self.split_into_sentences(document_text)
        
        if not sentences:
            return [document_text]
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)
            
            # If single sentence exceeds max, split it further
            if sentence_tokens > self.max_chunk_size:
                # Flush current chunk if exists
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_tokens = 0
                
                # Split long sentence by words
                words = sentence.split()
                temp_chunk = []
                temp_tokens = 0
                
                for word in words:
                    word_tokens = self.count_tokens(word)
                    if temp_tokens + word_tokens > self.max_chunk_size:
                        if temp_chunk:
                            chunks.append(' '.join(temp_chunk))
                        temp_chunk = [word]
                        temp_tokens = word_tokens
                    else:
                        temp_chunk.append(word)
                        temp_tokens += word_tokens
                
                if temp_chunk:
                    chunks.append(' '.join(temp_chunk))
                
                continue
            
            # Check if adding sentence exceeds max chunk size
            if current_tokens + sentence_tokens > self.max_chunk_size:
                # Flush current chunk if it meets minimum size
                if current_tokens >= self.min_chunk_size:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = [sentence]
                    current_tokens = sentence_tokens
                else:
                    # Add sentence even if it exceeds max slightly
                    current_chunk.append(sentence)
                    current_tokens += sentence_tokens
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_tokens = 0
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
        
        # Add remaining chunk
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks
    
    def create_chunk_summary(self, chunk: str, max_length: int = 150) -> str:
        """
        Create a brief summary of a chunk.
        Used for building consolidated context.
        
        Args:
            chunk: Text chunk
            max_length: Maximum summary length in characters
            
        Returns:
            Brief summary
        """
        # Simple extractive summary: first N characters
        if len(chunk) <= max_length:
            return chunk
        
        # Try to break at sentence boundary
        truncated = chunk[:max_length]
        last_period = truncated.rfind('.')
        
        if last_period > max_length * 0.6:  # If period is reasonably close
            return truncated[:last_period + 1]
        
        return truncated + "..."


# Singleton instance
_chunker_instance = None


def get_chunker() -> DocumentChunker:
    """Get or create chunker instance."""
    global _chunker_instance
    if _chunker_instance is None:
        _chunker_instance = DocumentChunker()
    return _chunker_instance
