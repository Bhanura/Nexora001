# Nexora001 🤖

<div align="center">

![Nexora001 Banner](https://img.shields.io/badge/Nexora001-AI_Knowledge_Base-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13+-green?style=for-the-badge&logo=python)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-blue?style=for-the-badge&logo=google)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-teal?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An intelligent multi-tenant AI-powered knowledge base with REST API and RAG**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [API](#-api-documentation) • [Architecture](#-architecture)

</div>

---

## 🌟 Overview

Nexora001 is a **production-ready multi-tenant AI knowledge base** that:
- 🕷️ **Crawls websites** (static HTML + JavaScript with Playwright)
- 📄 **Ingests documents** (PDF, DOCX)
- 🧠 **Generates vector embeddings** (384-dimensional)
- 🔍 **Performs semantic search** (cosine similarity)
- 💬 **Answers questions** using Google Gemini AI with RAG
- 🔐 **Multi-tenant architecture** with JWT authentication
- 🚀 **REST API** with FastAPI + Swagger documentation
- 🎨 **Beautiful console interface** with Rich UI

**Built with:** Python 3.13, FastAPI, Scrapy, Playwright, MongoDB Atlas, sentence-transformers, Google Gemini 2.5 Flash

---

## ✨ Features

### 🔐 **Multi-Tenant Architecture**
- JWT-based authentication
- User registration and login
- Per-user data isolation
- API key generation for widget integration
- Super admin controls

### 🌐 **REST API (FastAPI)**
- Full RESTful API with OpenAPI/Swagger docs
- Authentication endpoints (register, login, profile)
- Ingestion endpoints (URL crawling, file upload)
- Chat endpoints (RAG Q&A, streaming responses)
- System endpoints (status, documents, statistics)
- Admin endpoints (user management)
- Postman collection included

### 🕷️ **Intelligent Web Crawling**
- Static HTML crawling with Scrapy
- JavaScript-rendered pages with Playwright (Chromium)
- Configurable crawl depth
- Respects robots.txt
- Rate limiting & duplicate detection
- Background job processing

### 📄 **Multi-Format Document Processing**
- **PDF** extraction with PyMuPDF
- **DOCX** parsing with python-docx
- **HTML** content extraction
- Intelligent text chunking (500 chars, 50 overlap)

### 🧠 **Vector Search & RAG**
- Local embeddings with sentence-transformers (all-MiniLM-L6-v2)
- 384-dimensional vectors stored in MongoDB
- Semantic similarity search with cosine similarity
- Retrieval-Augmented Generation with Google Gemini 2.5 Flash
- Context-aware responses with source citations

### 💬 **Conversational AI**
- Multi-turn conversations with context
- Chat history tracking per session
- Streaming responses (Server-Sent Events)
- Source citation in answers
- Relevance scoring

### 🎨 **Beautiful Console UI**
- Rich terminal interface with colors
- Interactive commands
- Real-time progress indicators
- Clear error messages

---

## 🎬 Demo

### Console Interface
```bash
$ python run. py

╭──────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                      │
│     ███╗   ██╗███████╗██╗  ██╗ ██████╗ ██████╗  █████╗     ██████╗  ██████╗ ██╗      │
│     ████╗  ██║██╔════╝╚██╗██╔╝██╔═══██╗██╔══██╗██╔══██╗   ██╔═████╗██╔═████╗███║     │
│     ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║██████╔╝███████║   ██║██╔██║██║██╔██║╚██║     │
│     ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║██╔══██╗██╔══██║   ████╔╝██║████╔╝██║ ██║     │
│     ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝██║  ██║██║  ██║   ╚██████╔╝╚██████╔╝ ██║     │
│     ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═╝     │
│                                                                                      │
│            AI-Powered Knowledge Base Chatbot with RAG                                │
│                                                                                      │
╰──────────────────────────────────────────────────────────────────────────────────────╯
Welcome to Nexora001!
Type 'help' for available commands, 'exit' to quit.

nexora001> crawl https://devguide.python.org/ --depth 2

✅ Crawl completed successfully!
Pages crawled: 11
Chunks created: 297
Documents stored: 297

nexora001> ask How do I contribute to Python? 

🤖 Answer (from 5 sources):

You can contribute to Python in several ways:

1. Create an Issue - Describe your proposed change
2. Create a Branch - From the main branch in Git
3. Work on Changes - Implement your bug fix or feature
4. Run Tests - Ensure everything works
5. Create Pull Request - Submit for review
... 

📚 Sources:
  [1] Python Developer's Guide (relevance: 77%)
      https://devguide.python. org/
```

### Crawling JavaScript Sites
```bash
nexora001> crawl https://quotes.toscrape.com/js/ --playwright

🕷️ Starting crawler... 
✓ Playwright enabled (Chromium)
✓ Pages crawled: 10
✓ Chunks created: 37

nexora001> ask Tell me a random quote

🤖 "A day without sunshine is like, you know, night." 
   — Steve Martin
```

---

## 🚀 Installation

### Prerequisites
- Python 3.11 or higher
- MongoDB Atlas account (free tier works)
- Google AI Studio API key (free)

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/Nexora001.git
cd Nexora001
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt

# Install Playwright browsers (for JavaScript crawling)
playwright install chromium
```

### Step 4: Configure Environment
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your credentials
```

**. env file:**
```properties
# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster. mongodb.net/
MONGODB_DATABASE=nexora001

# Google AI
GOOGLE_API_KEY=your_google_api_key_here

# Optional
DEBUG=false
```

### Step 5: Run Application

**Option 1: Console Application**
```bash
python run.py
```

**Option 2: REST API Server**
```bash
python run_api.py
```

API will be available at:
- 📚 **Swagger Docs**: http://localhost:8000/docs
- 📖 **ReDoc**: http://localhost:8000/redoc
- 🔧 **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🌐 API Documentation

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user | ❌ |
| POST | `/api/auth/login` | Login and get JWT token | ❌ |
| GET | `/api/auth/me` | Get current user profile | ✅ |
| PUT | `/api/auth/me` | Update user profile | ✅ |
| POST | `/api/auth/api-key` | Generate widget API key | ✅ |

### Ingestion Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/ingest/url` | Start URL crawling job | ✅ |
| GET | `/api/ingest/url/{job_id}` | Get crawl job status | ❌ |
| POST | `/api/ingest/file` | Upload PDF/DOCX file | ✅ |

### Chat Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/chat/ask` | Ask question (RAG) | ✅ |
| POST | `/api/chat/ask/stream` | Ask question (streaming) | ✅ |
| POST | `/api/chat/widget/ask` | Widget endpoint | API Key |
| GET | `/api/chat/history/{session_id}` | Get chat history | ✅ |

### System Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/status` | Get system status | ❌ |
| GET | `/api/documents` | List documents (paginated) | ✅ |
| GET | `/api/documents/stats` | Get document statistics | ❌ |
| DELETE | `/api/documents?doc_id=X` | Delete document by ID | ✅ |
| DELETE | `/api/documents/by-source` | Delete by source URL | ✅ |
| DELETE | `/api/documents/all` | Delete all documents | ✅ |

### Admin Endpoints (Super Admin Only)

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/admin/users` | List all users | 👑 Super Admin |
| POST | `/api/admin/ban` | Ban user | 👑 Super Admin |
| POST | `/api/admin/unban` | Unban user | 👑 Super Admin |
| DELETE | `/api/admin/client` | Delete user | 👑 Super Admin |

### 📦 Postman Collection

Import the included `Nexora001_API.postman_collection.json` for ready-to-use API requests with:
- Pre-configured authentication
- Example payloads
- Environment variables
- Test scripts

---

## 📖 Usage

### Console Application

| Command | Description | Example |
|---------|-------------|---------|
| `crawl <url>` | Crawl a website | `crawl https://example.com` |
| `crawl <url> --playwright` | Crawl with JavaScript | `crawl https://quotes.toscrape.com/js/ --playwright` |
| `crawl <url> --depth N` | Set crawl depth | `crawl https://example.com --depth 2` |
| `ingest <file>` | Ingest PDF/DOCX | `ingest document.pdf` |
| `ask <question>` | Ask a question | `ask What is machine learning?` |
| `list` | List indexed documents | `list` |
| `stats` | Show statistics | `stats` |
| `history` | Show conversation | `history` |
| `clear-history` | Clear conversation | `clear-history` |
| `delete <url>` | Delete documents | `delete https://example.com` |
| `status` | System status | `status` |
| `help` | Show help | `help` |
| `exit` | Exit application | `exit` |

### REST API Examples

**Register and Login:**
```bash
# Register new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123!","name":"Test User"}'

# Login to get JWT token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"SecurePass123!"}'
```

**Crawl a Website:**
```bash
curl -X POST http://localhost:8000/api/ingest/url \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://docs.python.org/3/",
    "max_depth": 1,
    "follow_links": true,
    "use_playwright": false
  }'
```

**Ask a Question:**
```bash
curl -X POST http://localhost:8000/api/chat/ask \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is Python?",
    "session_id": "my-session-123",
    "top_k": 5
  }'
```

**Upload a File:**
```bash
curl -X POST http://localhost:8000/api/ingest/file \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@document.pdf"
```

### Advanced Examples

**Crawl documentation site:**
```bash
nexora001> crawl https://docs.python.org/ --depth 2
```

**Crawl JavaScript application:**
```bash
nexora001> crawl https://react-app.com --playwright --depth 1
```

**Ingest research paper:**
```bash
nexora001> ingest research-paper.pdf
```

**Ask contextual questions:**
```bash
nexora001> ask What is Python?
nexora001> ask How do I contribute to it?  # Understands "it" = Python
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Console Application (Rich UI)                 │   │
│  │  Commands: crawl, ingest, ask, list, stats, etc.    │   │
│  └────────────────────┬─────────────────────────────────┘   │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────┼─────────────────────────────────────┐
│                  PROCESSING LAYER                            │
│                        │                                     │
│  ┌─────────────────────┴────────────────────────────────┐   │
│  │              Web Crawler (Scrapy)                     │   │
│  │  • Scrapy Spider (static HTML)                        │   │
│  │  • Playwright Integration (JavaScript)                │   │
│  └────────────────────┬──────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────────┐   │
│  │          Document Processors                           │   │
│  │  • PDF Processor (PyMuPDF)                            │   │
│  │  • DOCX Processor (python-docx)                       │   │
│  │  • HTML Parser                                        │   │
│  └────────────────────┬──────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────────┐   │
│  │          Text Chunker                                  │   │
│  │  • Intelligent splitting (500 chars)                  │   │
│  │  • Overlap (50 chars)                                 │   │
│  │  • Metadata preservation                              │   │
│  └────────────────────┬──────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────────┐   │
│  │      Embedding Generator                               │   │
│  │  • sentence-transformers (all-MiniLM-L6-v2)           │   │
│  │  • 384-dimensional vectors                            │   │
│  │  • Local processing (offline capable)                 │   │
│  └────────────────────┬──────────────────────────────────┘   │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────┼─────────────────────────────────────┐
│                   STORAGE LAYER                              │
│  ┌─────────────────────┴────────────────────────────────┐   │
│  │            MongoDB Atlas                              │   │
│  │  • Documents collection (content + metadata)          │   │
│  │  • Embeddings (384-dim vectors)                       │   │
│  │  • Vector similarity search (cosine)                  │   │
│  └────────────────────┬──────────────────────────────────┘   │
└────────────────────────┼─────────────────────────────────────┘
                         │
┌────────────────────────┼─────────────────────────────────────┐
│                     RAG LAYER                                │
│  ┌─────────────────────┴────────────────────────────────┐   │
│  │          Document Retriever                           │   │
│  │  • Query embedding generation                         │   │
│  │  • Vector similarity search                           │   │
│  │  • Top-K retrieval (default: 5)                       │   │
│  └────────────────────┬──────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────────┐   │
│  │       Answer Generator (Google Gemini)                 │   │
│  │  • Gemini 2.5 Flash                                   │   │
│  │  • Context-aware generation                           │   │
│  │  • Source citation                                    │   │
│  └────────────────────┬──────────────────────────────────┘   │
│                       │                                      │
│  ┌────────────────────┴──────────────────────────────────┐   │
│  │          RAG Pipeline                                  │   │
│  │  • Retrieve relevant context                          │   │
│  │  • Augment with conversation history                  │   │
│  │  • Generate answer with citations                     │   │
│  └───────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## 📊 Project Structure

```
Nexora001/
├── .env                      # Secret configuration (NEVER COMMIT)
├── .env.example              # Example configuration
├── .gitignore                # Git ignore rules
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── run.py                    # Console application entry point
├── run_api.py                # REST API server entry point
├── Nexora001_API.postman_collection.json  # Postman collection
│
├── docs/
│   └── SRS.md                # Software Requirements Specification
│
├── src/
│   └── nexora001/
│       ├── __init__.py
│       ├── main.py           # Console application
│       ├── config.py         # Configuration management
│       │
│       ├── api/              # REST API (FastAPI)
│       │   ├── __init__.py
│       │   ├── app.py        # FastAPI application
│       │   ├── dependencies.py  # Dependency injection
│       │   ├── models.py     # Pydantic models
│       │   ├── security.py   # JWT authentication
│       │   └── routes/
│       │       ├── auth.py   # Authentication endpoints
│       │       ├── chat.py   # Chat/RAG endpoints
│       │       ├── ingest.py # Ingestion endpoints
│       │       ├── system.py # System/documents endpoints
│       │       └── admin.py  # Admin endpoints
│       │
│       ├── crawler/
│       │   ├── __init__.py
│       │   ├── spider.py     # Scrapy spider with Playwright
│       │   ├── manager.py    # Crawler manager with crochet
│       │   └── settings.py   # Scrapy settings
│       │
│       ├── processors/
│       │   ├── __init__.py
│       │   ├── chunker.py        # Text chunking
│       │   ├── embeddings.py     # Embedding generation
│       │   ├── pdf_processor.py  # PDF processing
│       │   └── docx_processor.py # DOCX processing
│       │
│       ├── storage/
│       │   ├── __init__.py
│       │   └── mongodb.py    # MongoDB operations (multi-tenant)
│       │
│       └── rag/
│           ├── __init__.py
│           ├── retriever.py  # Document retrieval
│           ├── generator.py  # Answer generation (Gemini)
│           └── pipeline.py   # Complete RAG pipeline
│
└── tests/
    ├── __init__.py
    └── test_config.py
```

---

## 🧪 Testing

Run the complete test suite:

```bash
python test_phase1_complete.py
```

**Test Coverage:**
- ✅ Static HTML crawling
- ✅ JavaScript crawling (Playwright)
- ✅ PDF ingestion
- ✅ DOCX ingestion
- ✅ Vector embeddings
- ✅ Vector similarity search
- ✅ RAG question answering
- ✅ Conversation history
- ✅ Source citations
- ✅ Console interface

---

## 🎯 Performance

| Metric | Value |
|--------|-------|
| **Crawl Speed (Static)** | 1-2 pages/second |
| **Crawl Speed (Playwright)** | 0.3-0.5 pages/second |
| **Query Response Time** | < 5 seconds |
| **Vector Search Latency** | < 500ms |
| **Embedding Dimension** | 384 |
| **Chunk Size** | 500 characters |
| **Chunk Overlap** | 50 characters |

---

## 🗺️ Roadmap

### ✅ Phase 1: Console Application (COMPLETED)
- [x] Web crawling (static & JavaScript)
- [x] Document ingestion (PDF, DOCX)
- [x] Vector embeddings & search
- [x] RAG question answering
- [x] Console interface

### ✅ Phase 2: Backend API (COMPLETED)
- [x] FastAPI REST API with OpenAPI/Swagger
- [x] JWT authentication & user management
- [x] Multi-tenant architecture
- [x] /api/auth endpoints (register, login, profile)
- [x] /api/ingest endpoints (URL crawling, file upload)
- [x] /api/chat endpoints (RAG Q&A, streaming)
- [x] /api/documents endpoints (CRUD operations)
- [x] /api/admin endpoints (super admin controls)
- [x] Background job processing with crochet
- [x] Postman collection
- [x] Widget API key support

### 🚧 Phase 3: Deployment (In Progress)
- [ ] Docker containerization
- [ ] Docker Compose for local deployment
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Deploy to cloud (Railway/Render/Heroku)
- [ ] Production environment configuration
- [ ] Monitoring and logging

### 📅 Phase 4: Chat Frontend (Planned)
- [ ] React/Vue web application
- [ ] Chat interface
- [ ] Source display with citations
- [ ] Responsive design
- [ ] Real-time streaming responses
- [ ] Session management

### 📅 Phase 5: Admin Dashboard (Planned)
- [ ] Admin web interface
- [ ] URL submission form
- [ ] File upload interface
- [ ] Job status dashboard
- [ ] Content management
- [ ] User management UI
- [ ] Analytics and statistics

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

---

## 🙏 Acknowledgments

- **Python** - Core language
- **Scrapy** - Web crawling framework
- **Playwright** - Browser automation
- **MongoDB Atlas** - Cloud database
- **sentence-transformers** - Local embeddings
- **Google Gemini** - AI generation
- **Rich** - Beautiful console UI

---

## 📧 Contact

**Bhanura** - [LinkedIn](https://www.linkedin.com/in/bhanura-waduge-44b7611a7/)

Project Link: [https://github.com/Bhanura/Nexora001](https://github.com/Bhanura/Nexora001)

---

<div align="center">

**Made with ❤️ by Bhanura**

⭐ Star this repo if you find it helpful! 

</div>
