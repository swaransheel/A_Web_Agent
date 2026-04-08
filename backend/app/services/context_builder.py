"""
Context builder - combines search results into structured context for LLM.
"""

from typing import List, Tuple
from app.config import Config
from app.models.schemas import SearchResult, ContextItem
from app.utils.logger import get_logger

logger = get_logger(__name__)


class ContextBuilder:
    """Build context from search results for LLM prompt."""
    
    APPROXIMATE_TOKEN_PER_WORD = 1.3  # Rough conversion rate
    
    def __init__(self, max_tokens: int = Config.MAX_CONTEXT_TOKENS):
        self.max_tokens = max_tokens
    
    def build(self, search_results: List[SearchResult]) -> Tuple[str, List[str]]:
        """
        Build context string from search results.
        
        Args:
            search_results: List of search results from Tavily
        
        Returns:
            Tuple of (context_string, source_urls)
        """
        logger.info(f"Building context from {len(search_results)} results")
        
        context_items = []
        source_urls = []
        total_tokens = 0
        
        for idx, result in enumerate(search_results):
            # Check if we're approaching token limit
            item_tokens = self._estimate_tokens(result.title + result.content)
            
            if total_tokens + item_tokens > self.max_tokens:
                logger.warning(f"Context token limit reached at result {idx}")
                break
            
            context_item = ContextItem(
                title=result.title,
                content=result.content[:500],  # Truncate long content
                url=result.url,
                source_index=idx + 1
            )
            context_items.append(context_item)
            source_urls.append(result.url)
            total_tokens += item_tokens
        
        # Format context for LLM
        context_text = self._format_context(context_items)
        
        logger.info(f"Built context with {len(context_items)} items (~{total_tokens} tokens)")
        return context_text, source_urls
    
    def _format_context(self, items: List[ContextItem]) -> str:
        """Format context items into readable text."""
        if not items:
            return ""
        
        formatted_parts = []
        for item in items:
            part = f"[Source {item.source_index}]\n"
            part += f"Title: {item.title}\n"
            part += f"Content: {item.content}\n"
            part += f"URL: {item.url}\n"
            formatted_parts.append(part)
        
        return "\n".join(formatted_parts)
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count for text."""
        words = len(text.split())
        return int(words * self.APPROXIMATE_TOKEN_PER_WORD)
    
    def truncate_context(self, context: str, max_tokens: int = None) -> str:
        """
        Truncate context to fit within token limit.
        
        Args:
            context: Context string to truncate
            max_tokens: Maximum tokens (uses self.max_tokens if None)
        
        Returns:
            Truncated context
        """
        if max_tokens is None:
            max_tokens = self.max_tokens
        
        estimated_tokens = self._estimate_tokens(context)
        
        if estimated_tokens <= max_tokens:
            return context
        
        # Truncate by character proportion
        char_limit = int(len(context) * (max_tokens / estimated_tokens) * 0.95)
        truncated = context[:char_limit]
        
        # Find last complete sentence
        last_period = truncated.rfind(".")
        if last_period > len(truncated) * 0.8:  # Only if not too early
            truncated = truncated[:last_period + 1]
        
        logger.warning(f"Context truncated to ~{self._estimate_tokens(truncated)} tokens")
        return truncated
