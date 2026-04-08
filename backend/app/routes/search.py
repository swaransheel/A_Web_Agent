"""
Search routes - main API endpoints for the application.
"""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import uuid
from app.models.schemas import SearchRequest, SearchResponse, ErrorResponse
from app.agents.web_agent import WebAgent
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Initialize agent
agent = WebAgent()

# Create router
router = APIRouter(
    prefix="/api",
    tags=["search"],
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}}
)


@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """
    Main search endpoint.
    
    This endpoint receives a search query, processes it through the agent pipeline,
    performs web search, generates an AI answer, and returns structured response.
    
    Args:
        request: SearchRequest containing the user query
    
    Returns:
        SearchResponse with answer and sources
    
    Raises:
        HTTPException: If processing fails
    """
    request_id = str(uuid.uuid4())[:8]
    
    try:
        logger.info(f"[{request_id}] /search endpoint called with query: {request.query[:100]}")
        
        # Run agent pipeline
        response = await agent.run(request.query)
        
        logger.info(f"[{request_id}] /search endpoint returning response")
        return response
    
    except ValueError as e:
        logger.warning(f"[{request_id}] Validation error: {str(e)}")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    
    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while processing your search. Please try again."
        )


@router.get("/health")
async def health_check() -> dict:
    """
    Health check endpoint.
    
    Returns:
        Status information
    """
    try:
        pipeline_status = agent.get_pipeline_status()
        return {
            "status": "healthy",
            "message": "Server is running",
            "pipeline": pipeline_status
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service is unhealthy"
        )


@router.get("/")
async def root() -> dict:
    """Root endpoint with API information."""
    return {
        "name": "AI Web Search Agent API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/api/search (POST)",
            "health": "/api/health (GET)",
            "docs": "/docs (SwaggerUI)",
            "redoc": "/redoc (ReDoc)"
        }
    }
