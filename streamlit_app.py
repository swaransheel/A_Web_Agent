"""
Streamlit Frontend for AI Web Agent
"""
import streamlit as st
import requests
import os
from typing import List, Dict

# Page config
st.set_page_config(
    page_title="AI Web Search Agent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Styling
st.markdown("""
<style>
    .main { max-width: 900px; margin: 0 auto; }
    h1 { text-align: center; color: #1f77e4; }
    .stTextInput { max-width: 100%; }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")
SEARCH_ENDPOINT = f"{API_URL}/api/search"

# Title and description
st.title("🔍 AI Web Search Agent")
st.markdown("Search the web and get AI-powered answers with verified sources")

# Initialize session state
if "search_history" not in st.session_state:
    st.session_state.search_history = []

# Search input
col1, col2 = st.columns([5, 1])
with col1:
    query = st.text_input(
        "Ask anything...",
        placeholder="What is artificial intelligence?",
        key="search_input"
    )

with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

# Search function
def perform_search(search_query: str):
    """Make API call to search endpoint"""
    if not search_query.strip():
        st.warning("Please enter a search query")
        return None
    
    try:
        with st.spinner("Searching and generating answer..."):
            response = requests.post(
                SEARCH_ENDPOINT,
                json={"query": search_query},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code}")
                return None
    
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to API at {API_URL}")
        st.info("Make sure the backend server is running:")
        st.code("cd backend && python -m uvicorn app.main:app --reload")
        return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Handle search
if search_button or (query and st.session_state.get("last_query") != query):
    st.session_state.last_query = query
    result = perform_search(query)
    
    if result:
        # Store in history
        st.session_state.search_history.append({
            "query": query,
            "answer": result.get("answer", ""),
            "sources": result.get("sources", [])
        })
        
        # Display results
        st.divider()
        
        # Answer section
        st.subheading("📝 Answer")
        st.write(result.get("answer", "No answer generated"))
        
        # Sources section
        sources = result.get("sources", [])
        if sources:
            st.subheader("📚 Sources")
            for i, source in enumerate(sources, 1):
                try:
                    # Extract domain from URL
                    from urllib.parse import urlparse
                    domain = urlparse(source).netloc or source
                    st.markdown(f"{i}. [{domain}]({source})")
                except:
                    st.markdown(f"{i}. {source}")
        else:
            st.info("No sources found")

# Sidebar - History
if st.session_state.search_history:
    with st.sidebar:
        st.header("📋 Search History")
        
        for i, item in enumerate(reversed(st.session_state.search_history[-5:]), 1):
            with st.expander(f"{i}. {item['query'][:50]}..."):
                st.write("**Answer:**")
                st.write(item['answer'])
                if item['sources']:
                    st.write("**Sources:**")
                    for src in item['sources']:
                        st.markdown(f"- {src}")
        
        if st.button("🗑️ Clear History"):
            st.session_state.search_history = []
            st.rerun()

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: gray; font-size: 12px;">
    <p>AI Web Search Agent | Powered by FastAPI, Streamlit, Google Gemini & Tavily</p>
</div>
""", unsafe_allow_html=True)
