"""
Response builder - formats final response for the frontend.
"""

import re
from typing import List
from app.models.schemas import SearchResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ResponseBuilder:
    """Build response in the format expected by frontend."""
    
    @staticmethod
    def build(answer: str, sources: List[str]) -> SearchResponse:
        """
        Build SearchResponse from answer and sources.
        
        Args:
            answer: Generated answer text
            sources: List of source URLs
        
        Returns:
            SearchResponse object
        """
        logger.info(f"Building response with {len(sources)} sources")
        
        # Clean and format answer
        cleaned_answer = ResponseBuilder._clean_answer(answer)
        
        # Extract sources from answer if mentioned
        extracted_sources = ResponseBuilder._extract_sources_from_answer(cleaned_answer)
        
        # Combine with provided sources
        all_sources = list(set(sources + extracted_sources))[:5]  # Limit to 5 sources
        
        response = SearchResponse(
            answer=cleaned_answer,
            sources=all_sources
        )
        
        logger.info("Response built successfully")
        return response
    
    @staticmethod
    def _clean_answer(answer: str) -> str:
        """
        Clean and format answer text.
        
        Args:
            answer: Raw answer text
        
        Returns:
            Cleaned answer
        """
        # Remove leading/trailing whitespace
        answer = answer.strip()
        
        # Remove "Answer:" prefix if present (sometimes LLMs add this)
        if answer.lower().startswith("answer:"):
            answer = answer[7:].strip()
        
        # Remove markdown code blocks if present
        answer = re.sub(r"```[\s\S]*?```", "", answer)
        
        # Clean up multiple newlines
        answer = re.sub(r"\n{3,}", "\n\n", answer)
        
        # Remove or replace "Sources:" section (will be added by response builder)
        answer = re.sub(r"\n*Sources?:.*$", "", answer, flags=re.IGNORECASE | re.DOTALL)
        
        return answer.strip()
    
    @staticmethod
    def _extract_sources_from_answer(answer: str) -> List[str]:
        """
        Extract URLs from answer text.
        
        Args:
            answer: Answer text containing potential URLs
        
        Returns:
            List of found URLs
        """
        # URL pattern
        url_pattern = r"https?://[^\s\]\)]+"
        urls = re.findall(url_pattern, answer)
        
        if urls:
            logger.debug(f"Extracted {len(urls)} URLs from answer")
        
        return urls
    
    @staticmethod
    def format_for_json(response: SearchResponse) -> dict:
        """
        Format response for JSON serialization.
        
        Args:
            response: SearchResponse object
        
        Returns:
            Dictionary compatible with JSON
        """
        return {
            "answer": response.answer,
            "sources": response.sources
        }
