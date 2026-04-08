"""
Main FastAPI application.
Initializes the app, configures middleware, mounts routes, and sets up exception handling.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import Config
from app.routes import search
from app.utils.logger import get_logger

logger = get_logger(__name__)

# Validate configuration on startup
try:
    Config.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration validation failed: {str(e)}")
    raise


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=Config.APP_NAME,
        description="Production-ready backend for AI Web Search Agent",
        version=Config.APP_VERSION,
        debug=Config.DEBUG
    )
    
    # Configure CORS - VERY IMPORTANT for frontend connection
    logger.info(f"Configuring CORS for origins: {Config.CORS_ORIGINS}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[origin.strip() for origin in Config.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        max_age=600  # Cache preflight for 10 minutes
    )
    
    # Add request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log all incoming requests."""
        logger.debug(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.debug(f"Response status: {response.status_code}")
        return response
    
    # Include routes
    app.include_router(search.router)
    
    # Global exception handler
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        """Handle HTTP exceptions."""
        logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "path": str(request.url.path)
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle unexpected exceptions."""
        logger.error(f"Unexpected exception: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "path": str(request.url.path)
            }
        )
    
    # Startup event
    @app.on_event("startup")
    async def startup_event():
        """Called when application starts."""
        logger.info(f"Starting {Config.APP_NAME} v{Config.APP_VERSION}")
        logger.info(f"Configuration: {Config.to_dict()}")
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        """Called when application shuts down."""
        logger.info("Shutting down application")
    
    return app


# Create application instance
app = create_app()
