"""
Search service - integrates with Tavily API for web search.
"""

import httpx
import asyncio
from typing import List
from app.config import Config
from app.models.schemas import SearchResult
from app.utils.logger import get_logger

logger = get_logger(__name__)


class SearchService:
    """Service for web search via Tavily API."""
    
    BASE_URL = "https://api.tavily.com/search"
    
    def __init__(self):
        self.api_key = Config.TAVILY_API_KEY
        self.max_results = Config.TAVILY_MAX_RESULTS
        self.timeout = Config.API_TIMEOUT
    
    async def search(self, query: str) -> List[SearchResult]:
        """
        Search the web using Tavily API.
        
        Args:
            query: Search query string
        
        Returns:
            List of search results
        
        Raises:
            Exception: If search fails
        """
        logger.info(f"Searching: {query}")
        
        payload = {
            "api_key": self.api_key,
            "query": query,
            "max_results": self.max_results,
            "include_raw_content": True,
            "include_domains": [],
            "exclude_domains": []
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.BASE_URL, json=payload)
                response.raise_for_status()
                data = response.json()
            
            # Parse results
            results = []
            for item in data.get("results", []):
                result = SearchResult(
                    title=item.get("title", ""),
                    content=item.get("content", "") or item.get("snippet", ""),
                    url=item.get("url", "")
                )
                results.append(result)
            
            logger.info(f"Found {len(results)} search results")
            return results
        
        except httpx.TimeoutException:
            logger.error(f"Search timeout for query: {query}")
            raise Exception("Search service timeout - please try again")
        
        except httpx.HTTPError as e:
            logger.error(f"Search service error: {str(e)}")
            raise Exception(f"Search service unavailable: {str(e)}")
        
        except Exception as e:
            logger.error(f"Unexpected error during search: {str(e)}")
            raise Exception(f"Search failed: {str(e)}")
    
    async def search_with_retry(self, query: str, max_retries: int = 2) -> List[SearchResult]:
        """
        Search with retry logic.
        
        Args:
            query: Search query
            max_retries: Maximum retry attempts
        
        Returns:
            List of search results
        """
        for attempt in range(max_retries):
            try:
                return await self.search(query)
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Search attempt {attempt + 1} failed, retrying...")
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"Search failed after {max_retries} attempts")
                    raise
