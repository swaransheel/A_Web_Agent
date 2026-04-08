import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Validate API keys
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file")

# Model configuration
GEMINI_MODEL = "gemini-2.5-flash"
MAX_CONTEXT_LENGTH = 8000
MAX_SEARCH_RESULTS = 5
SEARCH_TIMEOUT = 10
