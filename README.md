# 🔍 AI Web Search Agent (Streamlit)

A powerful AI-powered web search agent built with **Streamlit**, **Gemini API**, and **Tavily Search**. Get accurate, context-based answers to any query using real-time web information.

---

## 🌟 Features

✅ **Real-time Web Search** - Integrated with Tavily API for up-to-date information  
✅ **AI-Powered Answers** - Uses Gemini 1.5 Flash for intelligent response generation  
✅ **Source Attribution** - Every answer includes clickable source links  
✅ **Error Handling** - Graceful failure modes with helpful error messages  
✅ **Clean UI** - Simple, intuitive Streamlit interface  
✅ **Fast Execution** - Optimized for quick response times  

---

## 📋 Prerequisites

- Python 3.8+
- Gemini API Key ([Get it here](https://ai.google.dev))
- Tavily API Key ([Get it here](https://tavily.com))

---

## 🚀 Quick Start

### 1. Clone / Setup

```bash
cd AI_web_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🏗️ Project Structure

```
ai-web-agent-streamlit/
├── app.py                           # Main Streamlit app
├── config.py                        # API configuration
│
├── services/
│   ├── search_service.py           # Tavily integration
│   ├── context_builder.py          # Context formatting
│   └── gemini_service.py           # Gemini API wrapper
│
├── utils/
│   └── helpers.py                  # UI helper functions
│
├── .env                            # API keys (gitignored)
├── requirements.txt                # Dependencies
└── README.md                       # This file
```

---

## ⚙️ How It Works

### Execution Flow

```
User Input
    ↓
Search Web (Tavily API)
    ↓
Build Context
    ↓
Call Gemini
    ↓
Display Answer + Sources
```

### Step-by-Step

1. **User Input** - Enter a query in Streamlit UI
2. **Web Search** - Tavily API retrieves top 5 relevant results
3. **Context Build** - Search results formatted for LLM
4. **AI Generation** - Gemini processes context and generates answer
5. **Display** - Answer shown with clickable sources

---

## 🧠 Architecture Highlights

### Search Service (`search_service.py`)
- Uses Tavily API for web search
- Returns structured results (title, content, URL)
- Timeout handling (10 seconds)

### Context Builder (`context_builder.py`)
- Combines search results into LLM-friendly format
- Limits context to 8000 characters (cost optimization)
- Extracts source URLs for display

### Gemini Service (`gemini_service.py`)
- Calls `gemini-1.5-flash` model
- Uses factual prompting to prevent hallucination
- Handles API errors gracefully

### Streamlit UI (`app.py`)
- Clean, centered layout
- Real-time search with spinner
- Error handling with helpful messages
- Source link display

---

## 🔐 Security & Best Practices

✅ API keys stored in `.env` (not committed to git)  
✅ Input validation for query length (500 char max)  
✅ Prompt injection prevention (strict instructions)  
✅ Error handling for all external APIs  
✅ Timeout protection (10s for search, 30s for Gemini)  

---

## 📊 Configuration

Edit `config.py` to customize:

```python
GEMINI_MODEL = "gemini-1.5-flash"        # LLM model
MAX_CONTEXT_LENGTH = 8000                # Context token limit
MAX_SEARCH_RESULTS = 5                   # Results per query
SEARCH_TIMEOUT = 10                      # Search timeout (seconds)
```

---

## 🚨 Troubleshooting

### "API Key not found"
- Ensure `.env` file exists in root directory
- Check `.env` has both `GEMINI_API_KEY` and `TAVILY_API_KEY`

### "Connection Error" or "Timeout"
- Check internet connection
- Verify API keys are valid
- Try a simpler query

### No search results
- Query might be too specific
- Try rephrasing the question
- Tavily service might be down (check status page)

---

## 🎨 UI Features

- **Centered Layout** - Focus on content
- **Spinners** - Visual feedback during processing
- **Error Messages** - Clear, actionable error text
- **Expandable Details** - Optional search metadata
- **Clickable Sources** - Direct links to source websites

---

## 📈 Advanced Features (Future)

- Query history sidebar
- Copy-to-clipboard for answers
- Streaming responses (typewriter effect)
- Result caching
- Multi-query comparison

---

## 🤝 Contributing

Found a bug? Have suggestions? Feel free to open an issue or submit a PR!

---

## 📝 License

MIT

---

## 🔗 Resources

- [Streamlit Docs](https://docs.streamlit.io)
- [Gemini API Docs](https://ai.google.dev/docs)
- [Tavily Search API](https://tavily.com/docs)

---

**Built with ❤️ using Streamlit, Gemini & Tavily**
