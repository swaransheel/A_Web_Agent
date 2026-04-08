import streamlit as st
from services.search_service import search_web
from services.context_builder import build_context
from services.gemini_service import get_gemini_response, clean_response
from utils.helpers import (
    validate_query, display_answer, display_sources,
    display_error, display_info
)

# Page configuration
st.set_page_config(
    page_title="AI Web Search Agent",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# Main title and subtitle
st.markdown('<h1 class="main-header">🔍 AI Web Search Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Search the web and get AI-powered answers</p>', unsafe_allow_html=True)

# Input section
st.markdown("---")
query = st.text_input(
    "Ask anything:",
    placeholder="What is artificial intelligence? How does photosynthesis work?",
    label_visibility="collapsed"
)

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔍 Search", use_container_width=True)

st.markdown("---")

# Main execution
if search_button:
    if not validate_query(query):
        st.stop()
    
    try:
        # Step 1: Search the web
        with st.spinner("🔎 Searching the web..."):
            results = search_web(query)
        
        if not results:
            display_info("No search results found. Please try a different query.")
            st.stop()
        
        # Step 2: Build context from results
        with st.spinner("📚 Processing search results..."):
            context, sources = build_context(results)
        
        # Step 3: Get AI-generated answer
        with st.spinner("🤖 Generating answer with AI..."):
            raw_response = get_gemini_response(context, query)
            response = clean_response(raw_response)
        
        # Step 4: Display results
        st.markdown("---")
        display_answer(response)
        st.markdown("---")
        display_sources(sources)
        
        # Display metadata
        with st.expander("📊 Search Details"):
            st.write(f"**Query:** {query}")
            st.write(f"**Results Found:** {len(results)}")
            st.write(f"**Context Length:** {len(context)} characters")
        
    except Exception as e:
        st.markdown("---")
        error_msg = str(e)
        
        if "API" in error_msg:
            display_error(
                f"API Error: {error_msg}\n\nPlease check your API keys in .env file.",
                "🔌 Connection Error"
            )
        elif "timeout" in error_msg.lower():
            display_error(
                f"Request timeout: {error_msg}\n\nPlease try again later.",
                "⏱️ Timeout Error"
            )
        else:
            display_error(error_msg, "❌ Error")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 12px;'>"
    "Powered by Streamlit • Gemini • Tavily Search"
    "</p>",
    unsafe_allow_html=True
)
