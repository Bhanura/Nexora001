# Software Requirements Specification (SRS)
# Nexora - AI-Powered Knowledge Base Chatbot

**Version:** 1.0  
**Date:** December 2, 2025  
**Author:** Bhanura  
**Document Status:** Draft

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features](#3-system-features)
4. [External Interface Requirements](#4-external-interface-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6.  [Technical Architecture](#6-technical-architecture)
7. [Development Phases](#7-development-phases)
8. [Risk Analysis](#8-risk-analysis)
9. [Glossary](#9-glossary)

---

## 1. Introduction

### 1.1 Purpose
Nexora is an AI-powered knowledge base chatbot that crawls websites, extracts content from various formats (HTML, PDF, images), stores them in a vector database, and provides intelligent answers using Retrieval-Augmented Generation (RAG) with Google Gemini. 

### 1.2 Scope
The system consists of:
- **Console Application** (Phase 1): CLI-based interaction for testing
- **Backend API** (Phase 2): FastAPI-based REST API
- **Chat Frontend** (Phase 3): Web application for chatting with AI
- **Admin Frontend** (Phase 4): Web application for data ingestion management

### 1.3 Definitions & Acronyms
| Term | Definition |
|------|------------|
| RAG | Retrieval-Augmented Generation |
| LLM | Large Language Model |
| Vector Search | Similarity search using embeddings |
| Embedding | Numerical representation of text |
| Chunking | Splitting documents into smaller pieces |

### 1.4 References
- [LangChain Documentation](https://python.langchain.com/)
- [MongoDB Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/)
- [Google Gemini API](https://ai.google.dev/)
- [Scrapy Documentation](https://docs.scrapy.org/)

---

## 2. Overall Description

### 2.1 Product Perspective
Nexora is a standalone system designed to:
1. **Crawl** websites and extract multi-format content
2. **Process** content into vector embeddings
3. **Store** data in MongoDB with vector search capability
4. **Retrieve** relevant context for user queries
5. **Generate** AI-powered responses using Google Gemini

### 2.2 Product Features Summary
```
┌─────────────────────────────────────────────────────────┐
│                    NEXORA FEATURES                       │
├─────────────────────────────────────────────────────────┤
│ 🌐 Web Crawling      - Scrapy + Playwright              │
│ 📄 Document Parsing  - PDF, DOCX, HTML, Images          │
│ 🧠 Vector Storage    - MongoDB Atlas Vector Search      │
│ 🔍 Semantic Search   - Find relevant content            │
│ 💬 AI Chat           - Google Gemini responses          │
│ 🔐 Secure Config     - Environment variables            │
└─────────────────────────────────────────────────────────┘
```

### 2. 3 User Classes and Characteristics
| User Type | Description | Technical Level |
|-----------|-------------|-----------------|
| End User | Asks questions through chat interface | Low |
| Admin | Manages data ingestion (URLs, PDFs) | Medium |
| Developer | Maintains and extends the system | High |

### 2.4 Operating Environment
- **Backend**: Python 3.11+
- **Database**: MongoDB Atlas (Cloud)
- **Hosting**: Heroku/Railway/Render
- **Frontend**: Modern web browsers

### 2.5 Constraints
1. Google Gemini API rate limits and costs
2. MongoDB Atlas free tier limitations (512MB storage)
3. Heroku dyno sleeping on free tier
4. Website anti-scraping measures

### 2.6 Assumptions
1. Users have stable internet connection
2. Target websites allow scraping (robots.txt compliant)
3. Google Gemini API remains available
4. MongoDB Atlas vector search is available in free tier

---

## 3. System Features

### 3.1 Web Crawling System

#### 3.1.1 Description
Automated web crawler that extracts content from websites, including JavaScript-rendered pages. 

#### 3.1.2 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| CR-001 | System shall crawl static HTML pages | High |
| CR-002 | System shall render JavaScript using Playwright | High |
| CR-003 | System shall respect robots.txt | High |
| CR-004 | System shall implement rate limiting | High |
| CR-005 | System shall extract text content from HTML | High |
| CR-006 | System shall follow internal links (configurable depth) | Medium |
| CR-007 | System shall handle pagination | Medium |
| CR-008 | System shall detect and skip duplicate content | Medium |

### 3.2 Document Processing System

#### 3.2. 1 Description
Multi-format document parser that extracts text from various file types. 

#### 3.2.2 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| DP-001 | System shall parse PDF documents | High |
| DP-002 | System shall extract text from images (OCR) | Medium |
| DP-003 | System shall parse Word documents (. docx) | Medium |
| DP-004 | System shall handle HTML content | High |
| DP-005 | System shall preserve document structure/metadata | Medium |
| DP-006 | System shall chunk documents intelligently | High |

### 3.3 Vector Storage System

#### 3.3. 1 Description
MongoDB-based storage with vector embeddings for semantic search.

#### 3.3.2 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| VS-001 | System shall generate embeddings using Google Embedding API | High |
| VS-002 | System shall store embeddings in MongoDB Atlas | High |
| VS-003 | System shall perform vector similarity search | High |
| VS-004 | System shall store document metadata | High |
| VS-005 | System shall support filtering by source/date | Medium |
| VS-006 | System shall handle embedding updates | Medium |

### 3.4 RAG Query System

#### 3.4. 1 Description
Retrieval-Augmented Generation system that answers questions using crawled knowledge.

#### 3.4. 2 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| RAG-001 | System shall retrieve relevant context from vector store | High |
| RAG-002 | System shall generate responses using Google Gemini | High |
| RAG-003 | System shall cite sources in responses | High |
| RAG-004 | System shall handle conversation history | Medium |
| RAG-005 | System shall gracefully handle no-context scenarios | High |
| RAG-006 | System shall implement response streaming | Low |

### 3.5 Admin Ingestion System

#### 3.5.1 Description
Interface for administrators to add new data sources. 

#### 3.5.2 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| AI-001 | Admin shall submit URLs for crawling | High |
| AI-002 | Admin shall upload PDF documents | High |
| AI-003 | Admin shall view ingestion status | Medium |
| AI-004 | Admin shall delete indexed content | Medium |
| AI-005 | Admin shall configure crawl depth | Low |

### 3.6 Chat Interface System

#### 3.6.1 Description
User-facing chat interface for asking questions.

#### 3.6.2 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| CI-001 | User shall send text queries | High |
| CI-002 | User shall receive AI-generated responses | High |
| CI-003 | User shall see source citations | High |
| CI-004 | User shall view conversation history | Medium |
| CI-005 | User shall start new conversations | Medium |

---

## 4. External Interface Requirements

### 4.1 User Interfaces

#### 4.1. 1 Console Interface (Phase 1)
```
┌─────────────────────────────────────────────────────────┐
│                    NEXORA CONSOLE                        │
├─────────────────────────────────────────────────────────┤
│ Commands:                                                │
│   crawl <url>     - Crawl a website                     │
│   ingest <file>   - Ingest a PDF file                   │
│   ask <question>  - Ask a question                      │
│   status          - View system status                  │
│   exit            - Exit application                    │
│                                                          │
│ nexora> ask What is machine learning?                   │
│                                                          │
│ 🤖 Based on the crawled content from example.com:       │
│    Machine learning is a subset of AI that...            │
│    [Source: https://example.com/ml-guide]               │
└─────────────────────────────────────────────────────────┘
```

#### 4.1.2 Chat Web Interface (Phase 3)
- Clean, modern chat UI
- Message bubbles for user/AI
- Source citations as expandable cards
- Dark/Light mode support

#### 4.1.3 Admin Web Interface (Phase 4)
- URL input form with crawl options
- File upload with drag-and-drop
- Ingestion job status table
- Content management dashboard

### 4.2 Hardware Interfaces
None required (cloud-based deployment)

### 4.3 Software Interfaces

| Interface | Description | Protocol |
|-----------|-------------|----------|
| MongoDB Atlas | Vector database | MongoDB Wire Protocol |
| Google Gemini API | LLM for generation | REST/gRPC |
| Google Embedding API | Text embeddings | REST |

### 4.4 Communication Interfaces

| Interface | Protocol | Port |
|-----------|----------|------|
| Backend API | HTTPS/REST | 443 |
| WebSocket (optional) | WSS | 443 |

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| PF-001 | Query response time | < 5 seconds |
| PF-002 | Crawl rate | 1-2 pages/second |
| PF-003 | Concurrent users | 10+ |
| PF-004 | Vector search latency | < 500ms |

### 5.2 Security Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| SC-001 | All API keys in environment variables | Critical |
| SC-002 | No secrets in Git repository | Critical |
| SC-003 | HTTPS for all communications | High |
| SC-004 | Input sanitization | High |
| SC-005 | Rate limiting on API endpoints | Medium |

### 5.3 Reliability Requirements

| ID | Requirement | Target |
|----|-------------|--------|
| RL-001 | System uptime | 99% |
| RL-002 | Graceful error handling | All errors logged |
| RL-003 | Data backup | Daily (MongoDB Atlas) |

### 5.4 Scalability Requirements

| ID | Requirement | Description |
|----|-------------|-------------|
| SL-001 | Horizontal scaling | Support multiple workers |
| SL-002 | Database scaling | MongoDB Atlas auto-scaling |

---

## 6. Technical Architecture

### 6.1 System Architecture Diagram
```
┌────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌──────────────────┐         ┌──────────────────┐               │
│    │   Chat Frontend  │         │  Admin Frontend  │               │
│    │   (React/Vue)    │         │   (React/Vue)    │               │
│    │   Port: 3000     │         │   Port: 3001     │               │
│    └────────┬─────────┘         └────────┬─────────┘               │
│             │                            │                          │
└─────────────┼────────────────────────────┼──────────────────────────┘
              │         HTTPS/REST         │
              └──────────────┬─────────────┘
                             │
┌────────────────────────────┼────────────────────────────────────────┐
│                        API LAYER                                    │
├────────────────────────────┼────────────────────────────────────────┤
│                            ▼                                        │
│              ┌─────────────────────────┐                            │
│              │      FastAPI Server     │                            │
│              │      Port: 8000         │                            │
│              ├─────────────────────────┤                            │
│              │  /api/chat              │ ← Chat endpoints           │
│              │  /api/ingest            │ ← Ingestion endpoints      │
│              │  /api/status            │ ← Status endpoints         │
│              └───────────┬─────────────┘                            │
│                          │                                          │
└──────────────────────────┼──────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────────┐
│                    SERVICE LAYER                                    │
├──────────────────────────┼──────────────────────────────────────────┤
│                          ▼                                          │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │                    LangChain Pipeline                        │  │
│    ├─────────────────────────────────────────────────────────────┤  │
│    │                                                              │  │
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │  │
│    │  │   Document   │  │   Vector     │  │    RAG Chain     │   │  │
│    │  │   Loaders    │  │   Store      │  │   (Retrieval +   │   │  │
│    │  │              │  │   Interface  │  │    Generation)   │   │  │
│    │  └──────────────┘  └──────────────┘  └──────────────────┘   │  │
│    │                                                              │  │
│    └─────────────────────────────────────────────────────────────┘  │
│                          │                                          │
│    ┌─────────────────────┼───────────────────────────────────────┐  │
│    │                     ▼                                        │  │
│    │  ┌──────────────────────────────────────────────────────┐   │  │
│    │  │              Scrapy + Playwright                      │   │  │
│    │  │              (Web Crawling Engine)                    │   │  │
│    │  └──────────────────────────────────────────────────────┘   │  │
│    │                                                              │  │
│    │  ┌──────────────────────────────────────────────────────┐   │  │
│    │  │              Unstructured. io / PyMuPDF                │   │  │
│    │  │              (Document Parsing)                       │   │  │
│    │  └──────────────────────────────────────────────────────┘   │  │
│    └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────────┐
│                    DATA LAYER                                       │
├──────────────────────────┼──────────────────────────────────────────┤
│                          ▼                                          │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │                  MongoDB Atlas                               │  │
│    ├─────────────────────────────────────────────────────────────┤  │
│    │                                                              │  │
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │  │
│    │  │  documents   │  │  embeddings  │  │  crawl_jobs      │   │  │
│    │  │  collection  │  │  (vectors)   │  │  collection      │   │  │
│    │  └──────────────┘  └──────────────┘  └──────────────────┘   │  │
│    │                                                              │  │
│    │  ┌──────────────────────────────────────────────────────┐   │  │
│    │  │              Atlas Vector Search Index                │   │  │
│    │  └──────────────────────────────────────────────────────┘   │  │
│    │                                                              │  │
│    └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────────┐
│                 EXTERNAL SERVICES                                   │
├──────────────────────────┼──────────────────────────────────────────┤
│                          ▼                                          │
│    ┌──────────────────────────────────────────────────────────────┐ │
│    │                  Google Cloud AI                              │ │
│    ├──────────────────────────────────────────────────────────────┤ │
│    │                                                               │ │
│    │  ┌─────────────────────┐    ┌─────────────────────────────┐  │ │
│    │  │   Gemini Pro API    │    │   Text Embedding API        │  │ │
│    │  │   (Generation)      │    │   (Embeddings)              │  │ │
│    │  └─────────────────────┘    └─────────────────────────────┘  │ │
│    │                                                               │ │
│    └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Technology Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Language | Python | 3.11+ |
| Web Framework | FastAPI | 0. 104+ |
| Web Crawling | Scrapy | 2.11+ |
| Browser Automation | Playwright | 1. 40+ |
| Document Parsing | Unstructured.io | 0.11+ |
| PDF Parsing | PyMuPDF | 1.23+ |
| RAG Framework | LangChain | 0.1+ |
| Vector Database | MongoDB Atlas | 7.0+ |
| LLM | Google Gemini Pro | Latest |
| Embeddings | Google text-embedding | Latest |
| Frontend | React or Vue. js | 18+ / 3+ |
| Hosting | Heroku/Railway | - |

### 6.3 Database Schema

```javascript
// Collection: documents
{
  "_id": ObjectId,
  "content": String,           // Chunked text content
  "embedding": [Float],        // Vector embedding (768 dimensions)
  "metadata": {
    "source_url": String,
    "source_type": String,     // "web", "pdf", "docx"
    "title": String,
    "crawled_at": DateTime,
    "chunk_index": Number,
    "total_chunks": Number
  }
}

// Collection: crawl_jobs
{
  "_id": ObjectId,
  "url": String,
  "status": String,            // "pending", "running", "completed", "failed"
  "pages_crawled": Number,
  "documents_created": Number,
  "started_at": DateTime,
  "completed_at": DateTime,
  "error_message": String
}

// Collection: conversations (optional)
{
  "_id": ObjectId,
  "session_id": String,
  "messages": [
    {
      "role": String,          // "user" or "assistant"
      "content": String,
      "sources": [String],
      "timestamp": DateTime
    }
  ]
}
```

### 6.4 API Endpoints

```yaml
# Chat Endpoints
POST /api/chat
  Request: { "message": string, "session_id": string?  }
  Response: { "response": string, "sources": string[] }

GET /api/chat/history/{session_id}
  Response: { "messages": Message[] }

# Ingestion Endpoints
POST /api/ingest/url
  Request: { "url": string, "depth": number?, "follow_links": boolean? }
  Response: { "job_id": string, "status": string }

POST /api/ingest/file
  Request: FormData (file)
  Response: { "job_id": string, "status": string }

GET /api/ingest/status/{job_id}
  Response: { "status": string, "progress": number, "documents": number }

# Management Endpoints
GET /api/status
  Response: { "documents": number, "sources": string[] }

DELETE /api/documents/{source_url}
  Response: { "deleted": number }
```

---

## 7.  Development Phases

### Phase 1: Console Application (Weeks 1-3)
```
┌─────────────────────────────────────────────────────────────┐
│                        PHASE 1                               │
│                   Console Application                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Week 1: Setup & Basic Crawling                             │
│  ├── Project structure setup                                │
│  ├── Environment configuration (. env)                       │
│  ├── MongoDB Atlas setup                                    │
│  ├── Basic Scrapy spider                                    │
│  └── Google Gemini API integration                          │
│                                                              │
│  Week 2: Document Processing & RAG                          │
│  ├── Text chunking implementation                           │
│  ├── Embedding generation                                   │
│  ├── Vector storage in MongoDB                              │
│  ├── Basic RAG query pipeline                               │
│  └── LangChain integration                                  │
│                                                              │
│  Week 3: Console Interface & Polish                         │
│  ├── Interactive console menu                               │
│  ├── PDF ingestion support                                  │
│  ├── Playwright integration for JS sites                    │
│  ├── Error handling & logging                               │
│  └── Testing & documentation                                │
│                                                              │
│  Deliverable: Working CLI application                       │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Backend API (Weeks 4-5)
```
┌─────────────────────────────────────────────────────────────┐
│                        PHASE 2                               │
│                      Backend API                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Week 4: API Development                                    │
│  ├── FastAPI setup                                          │
│  ├── Chat endpoints                                         │
│  ├── Ingestion endpoints                                    │
│  ├── Background job processing                              │
│  └── API documentation (OpenAPI)                            │
│                                                              │
│  Week 5: Deployment & Testing                               │
│  ├── Heroku/Railway setup                                   │
│  ├── Environment configuration                              │
│  ├── API testing                                            │
│  └── Performance optimization                               │
│                                                              │
│  Deliverable: Deployed REST API                             │
└─────────────────────────────────────────────────────────────┘
```

### Phase 3: Chat Frontend (Weeks 6-7)
```
┌─────────────────────────────────────────────────────────────┐
│                        PHASE 3                               │
│                    Chat Frontend                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Week 6: UI Development                                     │
│  ├── Frontend project setup (React/Vue)                     │
│  ├── Chat interface design                                  │
│  ├── API integration                                        │
│  └── Source citation display                                │
│                                                              │
│  Week 7: Polish & Deployment                                │
│  ├── Responsive design                                      │
│  ├── Error handling                                         │
│  ├── Deployment to hosting                                  │
│  └── Testing                                                │
│                                                              │
│  Deliverable: Live chat web application                     │
└─────────────────────────────────────────────────────────────┘
```

### Phase 4: Admin Frontend (Weeks 8-9)
```
┌─────────────────────────────────────────────────────────────┐
│                        PHASE 4                               │
│                   Admin Frontend                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Week 8: Admin Interface                                    │
│  ├── URL submission form                                    │
│  ├── File upload interface                                  │
│  ├── Job status dashboard                                   │
│  └── Content management                                     │
│                                                              │
│  Week 9: Integration & Launch                               │
│  ├── Full system integration                                │
│  ├── User authentication (optional)                         │
│  ├── Final testing                                          │
│  └── Documentation                                          │
│                                                              │
│  Deliverable: Complete Nexora system                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 8. Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API rate limits | High | Medium | Implement caching, rate limiting |
| Anti-bot measures | Medium | High | Use Playwright, rotating user agents |
| MongoDB storage limits | Medium | Medium | Efficient chunking, cleanup old data |
| Heroku dyno sleeping | High | Low | Consider paid tier or alternative |
| Poor search relevance | Medium | High | Tune chunk size, embedding model |
| LLM hallucinations | Medium | Medium | Strict RAG prompting, source verification |

---

## 9. Glossary

| Term | Definition |
|------|------------|
| **Chunking** | Splitting large documents into smaller, manageable pieces for embedding |
| **Embedding** | A vector (array of numbers) representing the semantic meaning of text |
| **Vector Search** | Finding similar items by comparing their vector representations |
| **RAG** | Retrieval-Augmented Generation - combining search with LLM generation |
| **LLM** | Large Language Model - AI model that generates text (e.g., Gemini) |
| **Spider** | A Scrapy component that defines how to crawl a website |
| **Playwright** | Browser automation tool for rendering JavaScript-heavy pages |

---

## Appendix A: Environment Variables

```bash
# .env. example (SAFE TO COMMIT)

# MongoDB Configuration
MONGODB_URI=mongodb+srv://<username>:<password>@cluster. mongodb.net/
MONGODB_DATABASE=nexora

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key_here

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO

# Crawling Configuration
CRAWL_DELAY=1.0
MAX_CRAWL_DEPTH=2
USER_AGENT=Nexora-Bot/1.0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

---

## Appendix B: Project Structure

```
nexora/
├── . env                    # Secret configuration (NEVER COMMIT)
├── .env. example           # Example configuration (SAFE TO COMMIT)
├── . gitignore             # Git ignore rules
├── README.md              # Project documentation
├── requirements. txt       # Python dependencies
├── setup.py               # Package setup
│
├── docs/
│   ├── SRS.md            # This document
│   └── API.md            # API documentation
│
├── src/
│   └── nexora/
│       ├── __init__.py
│       ├── main.py           # Console application entry
│       ├── config.py         # Configuration management
│       │
│       ├── crawler/
│       │   ├── __init__.py
│       │   ├── spider.py     # Scrapy spider
│       │   └── settings.py   # Scrapy settings
│       │
│       ├── processors/
│       │   ├── __init__.py
│       │   ├── chunker.py    # Text chunking
│       │   ├── pdf. py        # PDF processing
│       │   └── html.py       # HTML processing
│       │
│       ├── storage/
│       │   ├── __init__.py
│       │   ├── mongodb.py    # MongoDB operations
│       │   └── vectors.py    # Vector operations
│       │
│       ├── rag/
│       │   ├── __init__. py
│       │   ├── chain.py      # LangChain RAG chain
│       │   ├── embeddings.py # Embedding generation
│       │   └── prompts.py    # Prompt templates
│       │
│       └── api/              # Phase 2
│           ├── __init__. py
│           ├── app.py        # FastAPI application
│           └── routes/
│               ├── chat.py
│               └── ingest.py
│
├── frontend-chat/            # Phase 3
│   └── ... 
│
├── frontend-admin/           # Phase 4
│   └── ...
│
└── tests/
    ├── __init__.py
    ├── test_crawler.py
    ├── test_processors.py
    └── test_rag.py
```

---

*End of Software Requirements Specification*