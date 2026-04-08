"""
Configuration management for the AI Web Search Agent backend.
Loads environment variables and validates required API keys.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""

    # API Keys
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    TAVILY_API_KEY: str = os.getenv("TAVILY_API_KEY", "")

    # LLM Configuration
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    GEMINI_TEMPERATURE: float = float(os.getenv("GEMINI_TEMPERATURE", "0.3"))
    GEMINI_MAX_TOKENS: int = int(os.getenv("GEMINI_MAX_TOKENS", "1024"))

    # API Configuration
    TAVILY_MAX_RESULTS: int = int(os.getenv("TAVILY_MAX_RESULTS", "5"))
    API_TIMEOUT: int = int(os.getenv("API_TIMEOUT", "30"))

    # Context Configuration
    MAX_CONTEXT_TOKENS: int = int(os.getenv("MAX_CONTEXT_TOKENS", "8000"))

    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Application
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    APP_NAME: str = "AI Web Search Agent"
    APP_VERSION: str = "1.0.0"

    @classmethod
    def validate(cls) -> None:
        """Validate that required configuration values are set."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is not set")
        if not cls.TAVILY_API_KEY:
            raise ValueError("TAVILY_API_KEY environment variable is not set")

    @classmethod
    def to_dict(cls) -> dict:
        """Return configuration as dictionary (excluding sensitive keys)."""
        return {
            "app_name": cls.APP_NAME,
            "app_version": cls.APP_VERSION,
            "gemini_model": cls.GEMINI_MODEL,
            "tavily_max_results": cls.TAVILY_MAX_RESULTS,
            "api_timeout": cls.API_TIMEOUT,
            "debug": cls.DEBUG,
        }
