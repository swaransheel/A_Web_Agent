import streamlit as st
from typing import List, Dict


def display_error(error_message: str, title: str = "⚠️ Error"):
    """Display error message in Streamlit"""
    st.error(f"{title}\n{error_message}")


def display_success(message: str, title: str = "✅ Success"):
    """Display success message in Streamlit"""
    st.success(f"{title}\n{message}")


def display_info(message: str, title: str = "ℹ️ Info"):
    """Display info message in Streamlit"""
    st.info(f"{title}\n{message}")


def display_answer(answer: str):
    """Display AI-generated answer with formatting"""
    st.markdown("## 🧠 Answer")
    st.markdown(answer)


def display_sources(sources: List[str]):
    """Display clickable sources list"""
    if not sources:
        st.info("No sources found")
        return
    
    st.markdown("## 🔗 Sources")
    for idx, url in enumerate(sources, 1):
        try:
            # Extract domain for display
            domain = url.split("//")[-1].split("/")[0]
            st.markdown(f"{idx}. [{domain}]({url})")
        except Exception:
            st.markdown(f"{idx}. [Link]({url})")


def validate_query(query: str) -> bool:
    """Validate user query"""
    if not query or len(query.strip()) == 0:
        st.warning("Please enter a search query")
        return False
    
    if len(query) > 500:
        st.warning("Query too long (max 500 characters)")
        return False
    
    return True


def format_timestamp():
    """Get current timestamp for logging"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
