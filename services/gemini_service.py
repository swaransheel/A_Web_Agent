import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL


def initialize_gemini():
    """Initialize Gemini API"""
    genai.configure(api_key=GEMINI_API_KEY)


def get_gemini_response(context: str, query: str) -> str:
    """
    Get AI-generated response from Gemini
    
    Args:
        context: Combined search results context
        query: Original user query
    
    Returns:
        AI-generated answer
    """
    try:
        initialize_gemini()
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        prompt = f"""You are a factual AI assistant.

Use ONLY the provided context to answer the question.

Context:
{context}

Question:
{query}

Instructions:
- Be concise and accurate
- Do not hallucinate
- If unsure, say "Insufficient data"
- List sources clearly"""
        
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text
        else:
            return "Unable to generate response - API returned empty result"
    
    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")


def clean_response(response: str) -> str:
    """
    Clean and format Gemini response
    
    Args:
        response: Raw response from Gemini
    
    Returns:
        Cleaned response
    """
    # Remove excessive whitespace
    response = "\n".join(line.strip() for line in response.split("\n"))
    response = "\n".join(line for line in response.split("\n") if line)
    
    return response
