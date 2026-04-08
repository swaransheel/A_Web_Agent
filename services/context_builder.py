from typing import List, Dict, Tuple
from config import MAX_CONTEXT_LENGTH


def build_context(results: List[Dict]) -> Tuple[str, List[str]]:
    """
    Combine search results into context for LLM
    
    Args:
        results: List of search results from Tavily API
    
    Returns:
        Tuple of (formatted context string, list of source URLs)
    """
    context_parts = []
    sources = []
    
    for idx, result in enumerate(results, 1):
        source_entry = f"""
Source {idx}:
Title: {result.get('title', 'No title')}
Content: {result.get('content', 'No content')}
URL: {result.get('url', '#')}
---"""
        context_parts.append(source_entry)
        sources.append(result.get('url', '#'))
    
    context = "\n".join(context_parts)
    
    # Truncate context if it exceeds max length
    if len(context) > MAX_CONTEXT_LENGTH:
        context = context[:MAX_CONTEXT_LENGTH] + "..."
    
    return context, sources


def format_sources_for_display(sources: List[str]) -> List[Dict]:
    """
    Format sources for display in Streamlit
    
    Args:
        sources: List of source URLs
    
    Returns:
        List of formatted source dictionaries
    """
    formatted_sources = []
    for idx, url in enumerate(sources, 1):
        formatted_sources.append({
            "number": idx,
            "url": url,
            "display_text": url.split("//")[-1].split("/")[0]  # Extract domain
        })
    
    return formatted_sources
