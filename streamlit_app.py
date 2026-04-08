import streamlit as st
import requests
import os

# Page config
st.set_page_config(page_title="AI Web Search Agent", page_icon="🔍", layout="centered")

st.title("🔍 AI Web Search Agent")
st.markdown("Search the web and get AI-powered answers")

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Search input
query = st.text_input("Ask anything:", placeholder="What is artificial intelligence?")

if st.button("🔍 Search"):
    if query.strip():
        try:
            with st.spinner("Searching and generating answer..."):
                response = requests.post(
                    f"{API_URL}/api/search",
                    json={"query": query},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.subheading("📝 Answer")
                    st.write(data.get("answer", "No answer generated"))
                    
                    st.subheader("📚 Sources")
                    sources = data.get("sources", [])
                    if sources:
                        for i, src in enumerate(sources, 1):
                            st.markdown(f"{i}. [{src}]({src})")
                    else:
                        st.info("No sources found")
                else:
                    st.error(f"API Error: {response.status_code}")
        
        except requests.exceptions.ConnectionError:
            st.error(f"Cannot connect to backend at {API_URL}")
            st.info("Make sure the backend is running: `python -m uvicorn app.main:app --reload`")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a search query")

