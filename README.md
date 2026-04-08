# 🚀 AI Web Search Agent - Production Ready

A production-ready AI-powered web search agent combining real-time web search with LLM intelligence to provide accurate, source-backed answers.

**Status**: ✅ **FULLY INTEGRATED AND READY TO USE**

---

## ⚡ Quick Start (30 seconds)

### Start Backend
```bash
cd backend
python run_server.py
```

### Open Frontend
```
search_home/code.html
```

Done! Start searching. 🔍

---

## 📋 What's Included

### Backend (FastAPI - Production Ready)
- ✅ Google Gemini LLM integration
- ✅ Tavily web search integration  
- ✅ Query validation & sanitization
- ✅ Context optimization
- ✅ Error handling & logging
- ✅ Async endpoints
- ✅ CORS enabled
- ✅ Retry logic with exponential backoff

### Frontend (Beautiful HTML + JavaScript)
- ✅ Dark theme UI (Tailwind CSS)
- ✅ Homepage with search box
- ✅ Results page with answer + sources
- ✅ Follow-up questions (no reload)
- ✅ Copy to clipboard
- ✅ Responsive design
- ✅ NO HTML/CSS changes (JavaScript only)

### Integration
- ✅ Frontend ↔ Backend API
- ✅ Full error handling
- ✅ Session persistence
- ✅ Input validation both sides

---

## 📁 Project Structure

```
AI_web_agent/
├── backend/                    # FastAPI Server
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── config.py          # Configuration
│   │   ├── routes/search.py   # API endpoints
│   │   ├── services/          # Business logic
│   │   ├── agents/web_agent.py # Pipeline
│   │   ├── models/schemas.py  # Validation
│   │   └── utils/logger.py    # Logging
│   ├── .env                   # API KEYS ✅
│   ├── requirements.txt
│   └── run_server.py
├── search_home/
│   ├── code.html              # Homepage (integrated)
│   └── screen.png
├── search_results/
│   ├── code.html              # Results page (integrated)
│   └── screen.png
├── lumina_intelligence/
│   └── DESIGN.md              # System architecture
├── verify_setup.py            # Configuration checker
├── test_integration.py        # Integration tests
├── run_backend.bat            # Windows quick start
└── README.md                  # This file
```

---

## 🔄 How It Works

### Complete User Flow

```
1. USER ON HOMEPAGE
   └─ Types query → Clicks Search or presses Enter

2. FRONTEND VALIDATION
   └─ Check query length, no injections

3. API CALL
   └─ POST http://localhost:8000/api/search
      {"query": "What is AI?"}

4. BACKEND PIPELINE
   ├─ Validate query
   ├─ Search web (Tavily) → 5 results
   ├─ Build context
   ├─ Generate answer (Gemini)
   └─ Format response

5. RESPONSE
   └─ {"answer": "...", "sources": [...]}

6. RESULTS PAGE
   ├─ Display answer
   ├─ Show 5 sources
   └─ Follow-up search box

7. FOLLOW-UP (Optional)
   └─ Ask new question
   └─ Results update instantly
   └─ No page reload
```

### API Endpoint

```
POST /api/search

Request:
{
  "query": "Your question here"
}

Response:
{
  "answer": "AI-generated answer with research...",
  "sources": [
    "https://example.com/url1",
    "https://example.com/url2",
    ...
  ]
}

Error:
{
  "detail": "Error message"
}
```

---

## ✨ Features

| Feature | Frontend | Backend | Status |
|---------|----------|---------|--------|
| Search | ✅ Input box | ✅ Validation | ✅ |
| Web Search | — | ✅ Tavily | ✅ |
| AI Answer | — | ✅ Gemini | ✅ |
| Sources | ✅ Links | ✅ Tracking | ✅ |
| Follow-up | ✅ No reload | ✅ New query | ✅ |
| Copy | ✅ Button | — | ✅ |
| Error handling | ✅ Yes | ✅ Yes | ✅ |
| Input validation | ✅ Client | ✅ Server | ✅ |
| Logging | — | ✅ Yes | ✅ |
| CORS | — | ✅ Enabled | ✅ |

---

## 🚀 Installation & Setup

### 1. Backend Dependencies

```bash
cd backend

# Create virtual environment (first time)
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### 2. Configuration

Backend `.env` already has:
```
GEMINI_API_KEY=...        ✅ Configured
TAVILY_API_KEY=...        ✅ Configured
CORS_ORIGINS=localhost    ✅ Configured
```

To add more origins:
```
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 3. Start Backend

```bash
python run_server.py
```

Expected:
```
✅ Configuration validated
🚀 Starting AI Web Search Agent Backend...
📍 Server at: http://localhost:8000
📖 Docs: http://localhost:8000/docs
```

### 4. Open Frontend

```
search_home/code.html
```

Or with Python server:
```bash
python -m http.server 8080
# Visit: http://localhost:8080/search_home/code.html
```

---

## 🧪 Testing

### Verify Setup
```bash
python verify_setup.py
```

Checks:
- ✅ Configuration valid
- ✅ Dependencies installed
- ✅ Frontend files exist

### Run Integration Tests
```bash
python test_integration.py
```

Tests:
- ✅ Backend connection
- ✅ Search API
- ✅ Frontend files
- ✅ CORS headers
- ✅ Input validation

### Manual Testing

**Test 1: Basic Search**
1. Open `search_home/code.html`
2. Type: "What is machine learning?"
3. Click Search
4. Should see results with answer + sources

**Test 2: Quick Suggestions**
1. Click a suggestion button
2. Results load immediately

**Test 3: Follow-up**
1. Type a follow-up question
2. Click "Research"
3. Results update (no page reload)

**Test 4: Copy**
1. Click "Copy to Clipboard"
2. Paste - should have answer text

**Test 5: Sources**
1. Click a source URL
2. Opens in new tab

**Test 6: Errors**
1. Try empty query
2. Try very long query
3. Should show error messages

---

## 🔌 API Details

### Health Check
```bash
GET http://localhost:8000/api/health

Response:
{
  "status": "healthy",
  "message": "Server is running",
  "pipeline": { ... }
}
```

### Search
```bash
POST http://localhost:8000/api/search
Content-Type: application/json

{
  "query": "What is artificial intelligence?"
}
```

### Response Format
```json
{
  "answer": "Artificial intelligence (AI) is the simulation of human intelligence...",
  "sources": [
    "https://en.wikipedia.org/wiki/Artificial_intelligence",
    "https://www.ibm.com/cloud/learn/what-is-artificial-intelligence",
    ...
  ]
}
```

---

## ⚙️ Configuration

### Backend `.env` Options

```
# API Keys (REQUIRED)
GEMINI_API_KEY=your_key
TAVILY_API_KEY=your_key

# LLM Settings
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.3          # 0=deterministic, 1=creative
GEMINI_MAX_TOKENS=1024

# Search Settings
TAVILY_MAX_RESULTS=5
API_TIMEOUT=30                  # seconds

# Context Settings
MAX_CONTEXT_TOKENS=8000

# CORS (for different origins)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Logging
LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR

# App Settings
DEBUG=False
```

---

## 🐛 Troubleshooting

### Backend won't start

**Check Python:**
```bash
python --version
```

**Check Environment:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

**Check Config:**
```bash
cat backend/.env
```

**Check Port:**
```bash
netstat -ano | findstr :8000
```

### Cannot connect to backend

```bash
# Is backend running?
python run_server.py

# Test endpoint
curl http://localhost:8000/api/health

# Check port availability
netstat -ano | findstr :8000
```

### Search returns no results

**Check API Keys:**
- Gemini: https://makersuite.google.com/app/apikey
- Tavily: https://tavily.com

**Enable Debug Logging:**
```bash
# In backend/.env
LOG_LEVEL=DEBUG
python run_server.py
```

**Check Browser Console:**
- Press F12
- Go to Console tab
- Look for JavaScript errors

### CORS errors

**CORS already enabled for localhost**

If using different origin:
```
CORS_ORIGINS=http://your-origin:port
```

Restart backend after changing `.env`

### Slow responses

**Expected timing:**
- Tavily: 2-5 seconds
- Gemini: 2-10 seconds
- Total: 4-15 seconds typical

Check internet connection and API status.

---

## 🔐 Security Features

| Aspect | Implementation |
|--------|-----------------|
| API Keys | ✅ `.env` file only |
| Input | ✅ Length + pattern validation |
| Injection | ✅ Sanitization both sides |
| XSS | ✅ HTML escaping |
| CORS | ✅ Configured |
| Errors | ✅ User-friendly messages |
| Logs | ✅ No sensitive data |

---

## 📊 Performance

- **Search**: 4-15 seconds (Tavily + Gemini)
- **Follow-up**: 4-15 seconds
- **Copy**: Instant
- **Concurrent**: Scales with workers

---

## 🚀 Production Deployment

### Backend Deployment

**Using Gunicorn:**
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

**Using Docker:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Deployment

Deploy `search_home/code.html` and `search_results/code.html` to:
- Vercel, Netlify, GitHub Pages
- Any static hosting
- Update API_BASE_URL in code

### Environment Setup

```bash
# Production .env
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
API_TIMEOUT=30
```

---

## 📚 Key Concepts

### Query Processor
- Validates input length (1-500 chars)
- Detects injection attempts
- Extracts keywords
- Normalizes whitespace

### Search Service
- Calls Tavily API
- Gets top 5 results
- Includes retry logic
- Handles timeouts

### Context Builder
- Combines results
- Estimates token count
- Respects token limits
- Preserves URLs

### Gemini Service
- Sends context + query
- Generates answer
- Validates response
- Handles errors

### Response Builder
- Formats answer
- Extracts sources
- Cleans text
- Returns JSON

---

## 📖 Code Structure

```
Backend Pipeline:
Query Processor (validate)
    ↓
Search Service (web search)
    ↓
Context Builder (format)
    ↓
Gemini Service (generate)
    ↓
Response Builder (format)
    ↓
Return to Frontend
```

**Each service:**
- ✅ Single responsibility
- ✅ Proper error handling
- ✅ Logging
- ✅ Type hints
- ✅ Documentation

---

## 📞 Support & Resources

**Getting Help:**
1. Run `python verify_setup.py`
2. Run `python test_integration.py`
3. Check browser console (F12)
4. Check backend logs
5. See troubleshooting section above

**Resources:**
- FastAPI: https://fastapi.tiangolo.com/
- Gemini API: https://ai.google.dev/
- Tavily: https://tavily.com/
- Tailwind CSS: https://tailwindcss.com/

**Files:**
- Architecture: `lumina_intelligence/DESIGN.md`
- Integration: `test_integration.py`
- Verification: `verify_setup.py`

---

## 🎯 What Changed

### Frontend
- ✅ Added JavaScript integration
- ❌ NO HTML changes
- ❌ NO CSS changes
- ❌ NO styling changes

### Backend
- ✅ Created complete system
- ✅ Production-ready
- ✅ Fully documented
- ✅ Tested and verified

---

## ✅ Verification Checklist

- [x] Backend framework (FastAPI)
- [x] LLM integration (Gemini)
- [x] Search integration (Tavily)
- [x] Frontend JS integration
- [x] CORS configured
- [x] Error handling
- [x] Input validation
- [x] Logging
- [x] Documentation
- [x] Testing tools
- [x] Production ready
- [x] API keys configured

---

## 🎉 Ready to Go!

```bash
# 1. Start backend
cd backend && python run_server.py

# 2. Open frontend
search_home/code.html

# 3. Search!
```

**Enjoy intelligent web search!** 🔍

---

**AI Web Search Agent v1.0.0**  
Production Ready • Fully Integrated • Battle Tested  
Built with FastAPI, Gemini, Tavily
