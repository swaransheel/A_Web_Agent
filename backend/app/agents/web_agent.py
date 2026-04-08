"""
Web agent - orchestrates the entire search and generation pipeline.
"""

from typing import Optional
import uuid
from app.services.query_processor import QueryProcessor, QueryValidator
from app.services.search_service import SearchService
from app.services.context_builder import ContextBuilder
from app.services.gemini_service import GeminiService
from app.services.response_builder import ResponseBuilder
from app.models.schemas import SearchResponse
from app.utils.logger import get_logger

logger = get_logger(__name__)


class WebAgent:
    """Central agent that orchestrates the search pipeline."""
    
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.query_validator = QueryValidator()
        self.search_service = SearchService()
        self.context_builder = ContextBuilder()
        self.gemini_service = GeminiService()
        self.response_builder = ResponseBuilder()
    
    async def run(self, raw_query: str) -> SearchResponse:
        """
        Execute the agent pipeline to search and generate answer.
        
        Args:
            raw_query: Raw user query from frontend
        
        Returns:
            SearchResponse with answer and sources
        
        Raises:
            Exception: If pipeline fails
        """
        request_id = str(uuid.uuid4())[:8]
        logger.info(f"[{request_id}] Starting agent pipeline for query: {raw_query[:100]}")
        
        try:
            # Step 1: Validate query
            is_valid, error_msg = self.query_validator.validate(raw_query)
            if not is_valid:
                logger.warning(f"[{request_id}] Query validation failed: {error_msg}")
                raise ValueError(error_msg)
            
            # Step 2: Process query
            processed_query = self.query_processor.process(raw_query)
            logger.debug(f"[{request_id}] Step 1: Query processed")
            
            # Step 3: Search web
            search_results = await self.search_service.search_with_retry(processed_query)
            if not search_results:
                logger.warning(f"[{request_id}] No search results found")
                raise Exception("No relevant information found for this query")
            logger.debug(f"[{request_id}] Step 2: Web search completed ({len(search_results)} results)")
            
            # Step 4: Build context
            context, source_urls = self.context_builder.build(search_results)
            if not context:
                logger.warning(f"[{request_id}] Context is empty")
                raise Exception("Unable to build context from search results")
            logger.debug(f"[{request_id}] Step 3: Context built ({len(source_urls)} sources)")
            
            # Step 5: Generate answer
            answer = self.gemini_service.generate_answer(processed_query, context)
            if not answer:
                logger.error(f"[{request_id}] Empty answer generated")
                raise Exception("Failed to generate answer")
            logger.debug(f"[{request_id}] Step 4: Answer generated from Gemini")
            
            # Step 6: Validate and format response
            is_valid = self.gemini_service.validate_response(answer)
            if not is_valid:
                logger.warning(f"[{request_id}] Answer validation failed")
                raise Exception("Generated answer failed validation")
            
            # Step 7: Build response
            response = self.response_builder.build(answer, source_urls)
            logger.info(f"[{request_id}] Agent pipeline completed successfully")
            
            return response
        
        except ValueError as e:
            logger.error(f"[{request_id}] Validation error: {str(e)}")
            raise Exception(f"Invalid query: {str(e)}")
        
        except Exception as e:
            logger.error(f"[{request_id}] Pipeline error: {str(e)}")
            raise Exception(f"Search processing failed: {str(e)}")
    
    def get_pipeline_status(self) -> dict:
        """Get status of all services in the pipeline."""
        return {
            "agent": "ready",
            "services": {
                "query_processor": "ready",
                "search_service": "configured",
                "context_builder": "ready",
                "gemini_service": "configured",
                "response_builder": "ready"
            }
        }
