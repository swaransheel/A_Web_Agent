"""
Query processing service - handles input validation and normalization.
"""

from typing import Tuple
from app.utils.logger import get_logger

logger = get_logger(__name__)


class QueryProcessor:
    """Process and normalize user queries."""
    
    # Common stop words to remove for better search results
    STOP_WORDS = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "as", "is", "was", "are"
    }
    
    @staticmethod
    def process(raw_query: str) -> str:
        """
        Process and normalize a query.
        
        Args:
            raw_query: Raw user query string
        
        Returns:
            Processed query string
        """
        logger.debug(f"Processing query: {raw_query[:100]}")
        
        # Strip whitespace
        query = raw_query.strip()
        
        # Remove excessive whitespace
        query = " ".join(query.split())
        
        # Convert to lowercase for processing
        query_lower = query.lower()
        
        # Return original query (with normalization)
        # Don't remove stop words as they may be important for meaning
        logger.debug(f"Processed query: {query}")
        return query
    
    @staticmethod
    def extract_keywords(query: str) -> list[str]:
        """
        Extract important keywords from query.
        
        Args:
            query: Search query
        
        Returns:
            List of keywords
        """
        words = query.lower().split()
        # Filter out stop words and short words
        keywords = [
            word for word in words
            if word not in QueryProcessor.STOP_WORDS and len(word) > 2
        ]
        return keywords[:5]  # Return top 5 keywords


class QueryValidator:
    """Validate query input."""
    
    MIN_LENGTH = 1
    MAX_LENGTH = 500
    
    @staticmethod
    def validate(query: str) -> Tuple[bool, str]:
        """
        Validate query input.
        
        Args:
            query: Query string to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check empty
        if not query or not query.strip():
            return False, "Query cannot be empty"
        
        # Check length
        if len(query) < QueryValidator.MIN_LENGTH:
            return False, f"Query too short (minimum {QueryValidator.MIN_LENGTH} character)"
        
        if len(query) > QueryValidator.MAX_LENGTH:
            return False, f"Query too long (maximum {QueryValidator.MAX_LENGTH} characters)"
        
        # Check for dangerous patterns
        dangerous_patterns = ["<script", "javascript:", "eval(", "exec(", "DROP ", "DELETE "]
        if any(pattern in query.upper() for pattern in dangerous_patterns):
            return False, "Query contains potentially malicious content"
        
        return True, ""
