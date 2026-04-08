"""
Pydantic models for request and response schemas.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class SearchRequest(BaseModel):
    """Schema for search request from frontend."""
    
    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    
    @field_validator("query")
    @classmethod
    def validate_query(cls, v: str) -> str:
        """Validate and sanitize query input."""
        # Remove excessive whitespace
        v = " ".join(v.split())
        
        # Check for obvious injection attempts
        dangerous_patterns = ["<script", "javascript:", "eval(", "exec("]
        if any(pattern in v.lower() for pattern in dangerous_patterns):
            raise ValueError("Query contains potentially malicious content")
        
        return v


class SearchResponse(BaseModel):
    """Schema for search response to frontend."""
    
    answer: str = Field(..., description="AI-generated answer")
    sources: List[str] = Field(default_factory=list, description="List of source URLs")


class SearchResult(BaseModel):
    """Schema for individual search result from Tavily."""
    
    title: str
    content: str
    url: str
    score: Optional[float] = None


class ContextItem(BaseModel):
    """Schema for context item used in LLM prompt."""
    
    title: str
    content: str
    url: str
    source_index: int


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    request_id: Optional[str] = Field(None, description="Request ID for tracking")
