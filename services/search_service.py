import requests
from typing import List, Dict
from config import TAVILY_API_KEY, MAX_SEARCH_RESULTS, SEARCH_TIMEOUT


def search_web(query: str) -> List[Dict]:
    """
    Search the web using Tavily API
    
    Args:
        query: Search query string
    
    Returns:
        List of search results with title, content, and url
    """
    try:
        url = "https://api.tavily.com/search"
        
        payload = {
            "api_key": TAVILY_API_KEY,
            "query": query,
            "max_results": MAX_SEARCH_RESULTS
        }
        
        response = requests.post(url, json=payload, timeout=SEARCH_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        results = []
        
        if "results" in data:
            for result in data["results"]:
                results.append({
                    "title": result.get("title", "No title"),
                    "content": result.get("content", "No content"),
                    "url": result.get("url", "#")
                })
        
        return results
    
    except requests.exceptions.Timeout:
        raise Exception("Search API timeout - request took too long")
    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to search API")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"Search API error: {e.response.status_code}")
    except Exception as e:
        raise Exception(f"Search failed: {str(e)}")
