# Software Requirements Specification (SRS)
# Nexora001 - AI-Powered Multi-Tenant Knowledge Base

**Version:** 2.0  
**Date:** December 2, 2025  
**Last Updated:** Current  
**Author:** Development Team  
**Document Status:** Phase 2 Complete - Multi-Tenant REST API Operational

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
Nexora001 is an AI-powered multi-tenant knowledge base system that provides intelligent document retrieval and question-answering capabilities through a comprehensive REST API. The system crawls websites, processes documents (PDF, DOCX), generates embeddings, and provides context-aware answers using Retrieval-Augmented Generation (RAG) with Google Gemini.

### 1.2 Scope
The system currently consists of:
- **✅ Console Application** (Phase 1): CLI-based interaction for testing - COMPLETED
- **✅ Backend REST API** (Phase 2): FastAPI-based multi-tenant API with JWT authentication - COMPLETED
  - User Management & Authentication
  - Multi-tenant Document Ingestion (File Upload & Web Crawling)
  - RAG-based Chat System with Session Management
  - Widget API Keys for Embedding
  - Admin Controls & System Monitoring
- **📋 Chat Frontend** (Phase 3): Web application for chatting with AI - PLANNED
- **📋 Admin Frontend** (Phase 4): Web application for data ingestion management - PLANNED

### 1.3 Definitions & Acronyms
| Term | Definition |
|------|------------|
| RAG | Retrieval-Augmented Generation |
| LLM | Large Language Model |
| Vector Search | Similarity search using embeddings |
| Embedding | Numerical representation of text (384-dim) |
| Chunking | Splitting documents into smaller pieces |
| JWT | JSON Web Token for authentication |
| Multi-tenant | Isolated data per client/organization |
| Widget API Key | Authentication key for embedded chat widgets |

### 1.4 References
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MongoDB Atlas Vector Search](https://www.mongodb.com/docs/atlas/atlas-vector-search/)
- [Google Gemini API](https://ai.google.dev/)
- [Scrapy Documentation](https://docs.scrapy.org/)
- [Sentence Transformers](https://www.sbert.net/)

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
2. MongoDB Atlas storage limitations (managed via multi-tenant isolation)
3. Twisted reactor conflicts between crochet and Scrapy (under investigation)
4. Website anti-scraping measures
5. JWT token expiration (60 minutes)

### 2.6 Assumptions
1. Users have stable internet connection
2. Target websites allow scraping (robots.txt compliant)
3. Google Gemini API remains available
4. MongoDB Atlas vector search is available
5. Clients manage their own user authentication and widget integration

---

## 3. System Features

### 3.1 Authentication & User Management

#### 3.1.1 Description
Multi-tenant user authentication system with JWT tokens and role-based access control.

#### 3.1.2 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| AUTH-001 | System shall register users with email and password | High | ✅ Complete |
| AUTH-002 | System shall authenticate users with JWT tokens | High | ✅ Complete |
| AUTH-003 | System shall hash passwords using bcrypt | High | ✅ Complete |
| AUTH-004 | System shall validate email format | High | ✅ Complete |
| AUTH-005 | System shall expire tokens after 60 minutes | High | ✅ Complete |
| AUTH-006 | System shall provide token refresh endpoint | Medium | ✅ Complete |
| AUTH-007 | System shall support admin role for user management | High | ✅ Complete |

### 3.2 Web Crawling System

#### 3.2.1 Description
Automated web crawler that extracts content from websites, including JavaScript-rendered pages, with multi-tenant isolation.

#### 3.2.2 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| CR-001 | System shall crawl static HTML pages | High | ✅ Complete |
| CR-002 | System shall render JavaScript using Playwright | High | ✅ Complete |
| CR-003 | System shall respect robots.txt | High | ✅ Complete |
| CR-004 | System shall implement rate limiting | High | ✅ Complete |
| CR-005 | System shall extract text content from HTML | High | ✅ Complete |
| CR-006 | System shall follow internal links (configurable depth) | Medium | ✅ Complete |
| CR-007 | System shall handle pagination | Medium | ✅ Complete |
| CR-008 | System shall detect and skip duplicate content | Medium | ✅ Complete |
| CR-009 | System shall isolate crawled data per client | High | ✅ Complete |
| CR-010 | System shall run crawling as background job | High | ✅ Complete |

### 3.3 Document Processing System

#### 3.3.1 Description
Multi-format document parser that extracts text from various file types with client isolation.

#### 3.3.2 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| DP-001 | System shall parse PDF documents | High | ✅ Complete |
| DP-002 | System shall extract text from images (OCR) | Medium | 📋 Planned |
| DP-003 | System shall parse Word documents (.docx) | Medium | ✅ Complete |
| DP-004 | System shall handle HTML content | High | ✅ Complete |
| DP-005 | System shall preserve document structure/metadata | Medium | ✅ Complete |
| DP-006 | System shall chunk documents intelligently | High | ✅ Complete |
| DP-007 | System shall accept file uploads via API | High | ✅ Complete |
| DP-008 | System shall isolate processed documents per client | High | ✅ Complete |

### 3.4 Vector Storage System

#### 3.4.1 Description
MongoDB-based multi-tenant storage with vector embeddings for semantic search using sentence-transformers.

#### 3.4.2 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| VS-001 | System shall generate 384-dim embeddings using sentence-transformers | High | ✅ Complete |
| VS-002 | System shall store embeddings in MongoDB Atlas | High | ✅ Complete |
| VS-003 | System shall perform vector similarity search | High | ✅ Complete |
| VS-004 | System shall store document metadata | High | ✅ Complete |
| VS-005 | System shall support filtering by source/date | Medium | ✅ Complete |
| VS-006 | System shall handle embedding updates | Medium | ✅ Complete |
| VS-007 | System shall isolate document storage per client | High | ✅ Complete |
| VS-008 | System shall provide document statistics per client | Medium | ✅ Complete |

### 3.5 RAG Query System

#### 3.5.1 Description
Retrieval-Augmented Generation system that answers questions using crawled knowledge with chat session management.

#### 3.5.2 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| RAG-001 | System shall retrieve relevant context from vector store | High | ✅ Complete |
| RAG-002 | System shall generate responses using Google Gemini 2.5 Flash | High | ✅ Complete |
| RAG-003 | System shall cite sources in responses | High | ✅ Complete |
| RAG-004 | System shall maintain chat session history | High | ✅ Complete |
| RAG-005 | System shall provide session management endpoints | High | ✅ Complete |
| RAG-006 | System shall handle no-context scenarios | High | ✅ Complete |
| RAG-007 | System shall isolate chat sessions per client | High | ✅ Complete |

### 3.6 Widget API System

#### 3.6.1 Description
API key-based authentication system for embedding chat widgets in client applications.

#### 3.6.2 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| WID-001 | System shall generate unique API keys for clients | High | ✅ Complete |
| WID-002 | System shall validate API keys for widget requests | High | ✅ Complete |
| WID-003 | System shall allow API key rotation | Medium | ✅ Complete |
| WID-004 | System shall track API key usage | Medium | 📋 Planned |
| WID-005 | System shall provide chat endpoint for widgets | High | ✅ Complete |

### 3.7 Admin System

#### 3.7.1 Description
Administrative controls for user and system management.

#### 3.7.2 Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| ADM-001 | System shall list all users (admin only) | High | ✅ Complete |
| ADM-002 | System shall update user roles | High | ✅ Complete |
| ADM-003 | System shall delete users | High | ✅ Complete |
| ADM-004 | System shall provide system statistics | Medium | ✅ Complete |
| ADM-005 | System shall enforce role-based access | High | ✅ Complete |

---

## 4. External Interface Requirements

### 4.1 User Interfaces

#### 4.1.1 Console Interface (Phase 1) - ✅ COMPLETE
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

#### 4.1.2 REST API Interface (Phase 2) - ✅ COMPLETE

The system provides a comprehensive REST API with the following endpoint categories:

**Authentication Endpoints:**
- POST `/api/auth/register` - User registration
- POST `/api/auth/login` - User login with JWT token
- POST `/api/auth/refresh` - Token refresh
- GET `/api/auth/me` - Get current user info

**Chat Endpoints:**
- POST `/api/chat` - Send chat message with RAG
- GET `/api/chat/sessions` - List user's chat sessions
- GET `/api/chat/sessions/{id}` - Get session details
- DELETE `/api/chat/sessions/{id}` - Delete session

**Widget Endpoints:**
- POST `/api/widget/chat` - Chat via API key (for embedded widgets)
- POST `/api/widget/keys` - Generate new widget API key
- GET `/api/widget/keys` - List widget API keys
- DELETE `/api/widget/keys/{key_id}` - Delete API key

**Ingestion Endpoints:**
- POST `/api/ingest/file` - Upload PDF/DOCX for processing
- POST `/api/ingest/crawl` - Start web crawling job
- GET `/api/ingest/status` - Get ingestion job status
- GET `/api/documents` - List indexed documents
- DELETE `/api/documents/{doc_id}` - Delete document

**Admin Endpoints:**
- GET `/api/admin/users` - List all users
- PUT `/api/admin/users/{user_id}` - Update user
- DELETE `/api/admin/users/{user_id}` - Delete user
- GET `/api/admin/stats` - System statistics

**System Endpoints:**
- GET `/api/status` - System health check
- GET `/api/health` - Detailed health status

See [Nexora001_API.postman_collection.json](../Nexora001_API.postman_collection.json) for complete API testing collection.

#### 4.1.3 Web Interfaces (Phase 3 & 4) - 📋 PLANNED

Frontend applications planned for future phases.

### 4.2 Hardware Interfaces
Not applicable (cloud-based system).

### 4.3 Software Interfaces

| Interface | Description | Protocol | Status |
|-----------|-------------|----------|--------|
| MongoDB Atlas | Multi-tenant vector database | MongoDB Wire Protocol | ✅ Active |
| Google Gemini 2.5 Flash | LLM for generation | REST | ✅ Active |
| Sentence Transformers | Local text embeddings (all-MiniLM-L6-v2) | Python API | ✅ Active |
| Scrapy + Playwright | Web crawling with JS rendering | Python API | ✅ Active |

### 4.4 Communication Interfaces

| Interface | Protocol | Port | Status |
|-----------|----------|------|--------|
| Backend REST API | HTTP/HTTPS | 8000 | ✅ Active |
| MongoDB Connection | TCP | 27017 | ✅ Active |

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| PF-001 | Query response time | < 5 seconds | ✅ Met |
| PF-002 | Crawl rate | 1-2 pages/second | ✅ Met |
| PF-003 | Concurrent users | 50+ | ✅ Met |
| PF-004 | Vector search latency | < 500ms | ✅ Met |
| PF-005 | Token generation | 60 min expiration | ✅ Met |

### 5.2 Security Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| SC-001 | All API keys in environment variables | Critical | ✅ Complete |
| SC-002 | No secrets in Git repository | Critical | ✅ Complete |
| SC-003 | HTTPS for production deployments | High | 📋 Deployment |
| SC-004 | Input sanitization | High | ✅ Complete |
| SC-005 | Rate limiting on API endpoints | Medium | 📋 Planned |
| SC-006 | Password hashing with bcrypt | Critical | ✅ Complete |
| SC-007 | JWT token authentication | Critical | ✅ Complete |
| SC-008 | Multi-tenant data isolation | Critical | ✅ Complete |

### 5.3 Reliability Requirements

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| RL-001 | System uptime | 99% | 📋 Deployment |
| RL-002 | Graceful error handling | All errors logged | ✅ Complete |
| RL-003 | Data backup | MongoDB Atlas auto-backup | ✅ Active |
| RL-004 | Background job resilience | Retry on failure | ✅ Complete |

### 5.4 Scalability Requirements

| ID | Requirement | Description | Status |
|----|-------------|-------------|--------|
| SL-001 | Horizontal scaling | Support multiple Uvicorn workers | ✅ Ready |
| SL-002 | Database scaling | MongoDB Atlas auto-scaling | ✅ Active |
| SL-003 | Multi-tenant architecture | Isolated client data | ✅ Complete |

---

## 6. Technical Architecture

### 6.1 System Architecture Diagram
```
┌────────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                                │
├────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌──────────────────┐         ┌──────────────────┐               │
│    │   Chat Widget    │         │  Admin Frontend  │               │
│    │   (Embedded)     │         │   (React/Vue)    │               │
│    │   API Key Auth   │         │   JWT Auth       │               │
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
│                  FASTAPI REST API LAYER (Port 8000)                 │
├──────────────────────────┼──────────────────────────────────────────┤
│                          ▼                                          │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │              Authentication Middleware                       │  │
│    │              (JWT Bearer Token / API Key)                    │  │
│    └───────────────────────┬─────────────────────────────────────┘  │
│                            │                                        │
│    ┌───────────────────────┼─────────────────────────────────────┐  │
│    │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────────┐  │  │
│    │  │  Auth    │  │  Chat    │  │  Ingest  │  │   Admin    │  │  │
│    │  │  Routes  │  │  Routes  │  │  Routes  │  │   Routes   │  │  │
│    │  └──────────┘  └──────────┘  └──────────┘  └────────────┘  │  │
│    │                                                              │  │
│    │  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │  │
│    │  │  Widget  │  │  System  │  │Documents │                  │  │
│    │  │  Routes  │  │  Routes  │  │  Routes  │                  │  │
│    │  └──────────┘  └──────────┘  └──────────┘                  │  │
│    └─────────────────────────────────────────────────────────────┘  │
│                          │                                          │
└──────────────────────────┼──────────────────────────────────────────┘
                           │
┌──────────────────────────┼──────────────────────────────────────────┐
│                    SERVICE LAYER                                    │
├──────────────────────────┼──────────────────────────────────────────┤
│                          ▼                                          │
│    ┌─────────────────────────────────────────────────────────────┐  │
│    │                    RAG Pipeline                              │  │
│    ├─────────────────────────────────────────────────────────────┤  │
│    │                                                              │  │
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │  │
│    │  │   Document   │  │  Embeddings  │  │    Retriever     │   │  │
│    │  │  Processors  │  │  Generator   │  │   (Vector        │   │  │
│    │  │ (PDF/DOCX)   │  │ (sentence-   │  │    Search)       │   │  │
│    │  │              │  │ transformers)│  │                  │   │  │
│    │  └──────────────┘  └──────────────┘  └──────────────────┘   │  │
│    │                                                              │  │
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │  │
│    │  │   Chunker    │  │   Generator  │  │   MongoDB        │   │  │
│    │  │  (Smart      │  │  (Google     │  │   Storage        │   │  │
│    │  │   Split)     │  │   Gemini)    │  │  (Multi-tenant)  │   │  │
│    │  └──────────────┘  └──────────────┘  └──────────────────┘   │  │
│    │                                                              │  │
│    └─────────────────────────────────────────────────────────────┘  │
│                          │                                          │
│    ┌─────────────────────┼───────────────────────────────────────┐  │
│    │                     ▼                                        │  │
│    │  ┌──────────────────────────────────────────────────────┐   │  │
│    │  │              Scrapy + Playwright + Crochet           │   │  │
│    │  │              (Web Crawling Engine)                    │   │  │
│    │  └──────────────────────────────────────────────────────┘   │  │
│    │                                                              │  │
│    │  ┌──────────────────────────────────────────────────────┐   │  │
│    │  │              PyMuPDF + python-docx                    │   │  │
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
│    │                  MongoDB Atlas (Multi-Tenant)                │  │
│    ├─────────────────────────────────────────────────────────────┤  │
│    │                                                              │  │
│    │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │  │
│    │  │   users      │  │  documents   │  │  chat_sessions   │   │  │
│    │  │  collection  │  │  collection  │  │   collection     │   │  │
│    │  │  (with pwd)  │  │  (+ vectors) │  │                  │   │  │
│    │  └──────────────┘  └──────────────┘  └──────────────────┘   │  │
│    │                                                              │  │
│    │  ┌──────────────┐  ┌──────────────────────────────────────┐ │  │
│    │  │  api_keys    │  │     Atlas Vector Search Index        │ │  │
│    │  │  collection  │  │     (384-dim cosine similarity)      │ │  │
│    │  └──────────────┘  └──────────────────────────────────────┘ │  │
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
│    │                  Google Cloud AI + Local Models                 │ │
│    ├──────────────────────────────────────────────────────────────┤ │
│    │                                                               │ │
│    │  ┌─────────────────────┐    ┌─────────────────────────────┐  │ │
│    │  │ Gemini 2.5 Flash    │    │  Sentence Transformers      │  │ │
│    │  │   (Generation)      │    │  all-MiniLM-L6-v2 (Local)   │  │ │
│    │  └─────────────────────┘    └─────────────────────────────┘  │ │
│    │                                                               │ │
│    └──────────────────────────────────────────────────────────────┘ │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Technology Stack

| Layer | Technology | Version | Status |
|-------|------------|---------|--------|
| Language | Python | 3.13 | ✅ Active |
| Web Framework | FastAPI | 0.123.5 | ✅ Active |
| ASGI Server | Uvicorn | 0.38.0 | ✅ Active |
| Authentication | PyJWT + bcrypt + passlib | Latest | ✅ Active |
| Web Crawling | Scrapy | 2.13.4 | ✅ Active |
| Browser Automation | Playwright | 1.56.0 | ✅ Active |
| Async Management | crochet + Twisted | 2.2.0 / 25.5.0 | ✅ Active |
| PDF Parsing | PyMuPDF (fitz) | 1.26.6 | ✅ Active |
| DOCX Parsing | python-docx | 1.2.0 | ✅ Active |
| Vector Database | MongoDB Atlas | 7.0+ | ✅ Active |
| MongoDB Driver | PyMongo + Motor | 4.15.5 / 3.7.1 | ✅ Active |
| Embeddings (Local) | sentence-transformers | 5.1.2 | ✅ Active |
| Embedding Model | all-MiniLM-L6-v2 | Latest | ✅ Active |
| LLM | Google Gemini 2.5 Flash | Latest | ✅ Active |
| LLM SDK | google-generativeai | 0.3.2 | ✅ Active |
| Frontend (Planned) | React or Vue.js | 18+ / 3+ | 📋 Planned |
| Deployment | Railway/Render/Azure | - | 📋 Planned |

### 6.3 Database Schema

#### Multi-Tenant Collections

```javascript
// Collection: users
{
  "_id": ObjectId,
  "email": String,              // Unique email
  "password_hash": String,      // bcrypt hashed password
  "client_id": String,          // Unique tenant identifier
  "role": String,               // "user" or "admin"
  "created_at": DateTime
}

// Collection: documents
{
  "_id": ObjectId,
  "client_id": String,          // Tenant isolation
  "content": String,            // Chunked text content
  "embedding": [Float],         // Vector embedding (384 dimensions)
  "metadata": {
  "client_id": String,          // Tenant isolation
  "content": String,            // Chunked text content
  "embedding": [Float],         // Vector embedding (384 dimensions)
  "metadata": {
    "source_url": String,
    "source_type": String,      // "web", "pdf", "docx"
    "title": String,
    "crawled_at": DateTime,
    "chunk_index": Number,
    "total_chunks": Number
  }
}

// Collection: chat_sessions
{
  "_id": ObjectId,
  "client_id": String,          // Tenant isolation
  "session_id": String,         // UUID
  "user_email": String,
  "messages": [
    {
      "role": String,           // "user" or "assistant"
      "content": String,
      "sources": [String],      // URLs cited
      "timestamp": DateTime
    }
  ],
  "created_at": DateTime,
  "updated_at": DateTime
}

// Collection: api_keys
{
  "_id": ObjectId,
  "client_id": String,          // Tenant isolation
  "key": String,                // Hashed API key
  "name": String,               // Key description
  "created_at": DateTime,
  "last_used": DateTime
}

// Vector Search Index: vector_index
{
  "type": "vectorSearch",
  "fields": [
    {
      "type": "vector",
      "path": "embedding",
      "numDimensions": 384,
      "similarity": "cosine"
    }
  ]
}
```

### 6.4 API Endpoints (Phase 2 - ✅ COMPLETE)

#### Authentication Endpoints
```yaml
POST /api/auth/register
  Request: { "email": string, "password": string }
  Response: { "message": string, "client_id": string }

POST /api/auth/login
  Request: { "email": string, "password": string }
  Response: { "access_token": string, "token_type": "bearer" }

POST /api/auth/refresh
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "access_token": string }

GET /api/auth/me
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "email": string, "client_id": string, "role": string }
```

#### Chat Endpoints
```yaml
POST /api/chat
  Headers: { "Authorization": "Bearer <token>" }
  Request: { "message": string, "session_id": string? }
  Response: { "response": string, "sources": string[], "session_id": string }

GET /api/chat/sessions
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "sessions": [{ "session_id": string, "created_at": string, "message_count": number }] }

GET /api/chat/sessions/{session_id}
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "messages": [{ "role": string, "content": string, "timestamp": string }] }

DELETE /api/chat/sessions/{session_id}
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "message": string }
```

#### Widget Endpoints
```yaml
POST /api/widget/chat
  Headers: { "X-API-Key": "<widget_api_key>" }
  Request: { "message": string, "session_id": string? }
  Response: { "response": string, "sources": string[], "session_id": string }

POST /api/widget/keys
  Headers: { "Authorization": "Bearer <token>" }
  Request: { "name": string }
  Response: { "api_key": string, "key_id": string }

GET /api/widget/keys
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "keys": [{ "id": string, "name": string, "created_at": string }] }

DELETE /api/widget/keys/{key_id}
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "message": string }
```

#### Ingestion Endpoints
```yaml
POST /api/ingest/crawl
  Headers: { "Authorization": "Bearer <token>" }
  Request: { "url": string, "depth": number? }
  Response: { "job_id": string, "status": "started" }

POST /api/ingest/file
  Headers: { "Authorization": "Bearer <token>" }
  Request: FormData (file: PDF/DOCX, source_url: string)
  Response: { "message": string, "documents_processed": number }

GET /api/ingest/status
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "status": string, "jobs": [{ "job_id": string, "status": string }] }
```

#### Document Management Endpoints
```yaml
GET /api/documents
  Headers: { "Authorization": "Bearer <token>" }
  Query: ?page=1&limit=50
  Response: { "documents": [{ "id": string, "title": string, "source_url": string, "created_at": string }] }

DELETE /api/documents/{doc_id}
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "message": string }
```

#### Admin Endpoints
```yaml
GET /api/admin/users
  Headers: { "Authorization": "Bearer <admin_token>" }
  Response: { "users": [{ "email": string, "client_id": string, "role": string, "created_at": string }] }

PUT /api/admin/users/{user_id}
  Headers: { "Authorization": "Bearer <admin_token>" }
  Request: { "role": string }
  Response: { "message": string }

DELETE /api/admin/users/{user_id}
  Headers: { "Authorization": "Bearer <admin_token>" }
  Response: { "message": string }

GET /api/admin/stats
  Headers: { "Authorization": "Bearer <admin_token>" }
  Response: { "total_users": number, "total_documents": number, "total_sessions": number }
```

#### System Endpoints
```yaml
GET /api/status
  Headers: { "Authorization": "Bearer <token>" }
  Response: { "total_documents": number, "unique_sources": number, "avg_chunk_size": number, "sources": [string] }

GET /api/health
  Response: { "status": "healthy", "version": string, "uptime": number }
```

---

## 7. Development Phases

### Phase 1: Console Application - ✅ COMPLETED
```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1 - ✅ COMPLETED                    │
│                   Console Application                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ Week 1: Setup & Basic Crawling                          │
│  ✅ Project structure setup                                 │
│  ✅ Environment configuration (.env)                        │
│  ✅ MongoDB Atlas setup                                     │
│  ✅ Basic Scrapy spider                                     │
│  ✅ Google Gemini API integration                           │
│                                                              │
│  ✅ Week 2: Document Processing & RAG                       │
│  ✅ Text chunking implementation                            │
│  ✅ Embedding generation (sentence-transformers)            │
│  ✅ Vector storage in MongoDB                               │
│  ✅ Basic RAG query pipeline                                │
│  ✅ Custom RAG pipeline (without LangChain)                 │
│                                                              │
│  ✅ Week 3: Console Interface & Polish                      │
│  ✅ Interactive console menu (Rich UI)                      │
│  ✅ PDF ingestion support (PyMuPDF)                         │
│  ✅ DOCX ingestion support (python-docx)                    │
│  ✅ Playwright integration for JS sites                     │
│  ✅ Error handling & logging                                │
│  ✅ Testing & documentation                                 │
│                                                              │
│  ✅ Deliverable: Working CLI application                    │
└─────────────────────────────────────────────────────────────┘
```

### Phase 2: Backend REST API - ✅ COMPLETED
```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 2 - ✅ COMPLETED                    │
│                Multi-Tenant REST API                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ Authentication & User Management                         │
│  ✅ JWT token-based authentication                           │
│  ✅ User registration and login                              │
│  ✅ Password hashing with bcrypt                             │
│  ✅ Role-based access control (user/admin)                   │
│  ✅ Multi-tenant architecture with client_id isolation       │
│                                                              │
│  ✅ Chat System                                              │
│  ✅ RAG-based chat endpoint with context retrieval           │
│  ✅ Chat session management                                  │
│  ✅ Conversation history storage                             │
│  ✅ Source citation in responses                             │
│                                                              │
│  ✅ Widget API System                                        │
│  ✅ API key generation for widget embedding                  │
│  ✅ API key-based authentication                             │
│  ✅ Separate widget chat endpoint                            │
│  ✅ Key management (create, list, delete)                    │
│                                                              │
│  ✅ Document Ingestion                                       │
│  ✅ File upload endpoint (PDF/DOCX)                          │
│  ✅ Web crawling endpoint (background jobs)                  │
│  ✅ Document listing and deletion                            │
│  ✅ Client-isolated document storage                         │
│                                                              │
│  ✅ Admin Controls                                           │
│  ✅ User management (list, update, delete)                   │
│  ✅ System statistics dashboard                              │
│  ✅ Role-based admin restrictions                            │
│                                                              │
│  ✅ System Monitoring                                        │
│  ✅ Health check endpoints                                   │
│  ✅ Status endpoints with document statistics                │
│  ✅ Comprehensive error logging                              │
│                                                              │
│  ✅ Deliverable: Production-ready multi-tenant REST API      │
│  ✅ Documentation: Postman collection with 30+ endpoints     │
└─────────────────────────────────────────────────────────────┘
```

### Phase 3: Chat Frontend - 📋 PLANNED
```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 3 - 📋 PLANNED                      │
│                    Chat Frontend                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📋 Week 7: Frontend Setup & Auth                           │
│  ├── React/Vue.js project setup                             │
│  ├── Authentication UI (login/register)                     │
│  ├── JWT token management                                   │
│  ├── Protected routes                                       │
│  └── User profile page                                      │
│                                                              │
│  📋 Week 8: Chat Interface                                  │
│  ├── Chat message components                                │
│  ├── Real-time message display                              │
│  ├── Session management UI                                  │
│  ├── Source citation display                                │
│  └── Responsive design                                      │
│                                                              │
│  📋 Week 9: Polish & Deploy                                 │
│  ├── Error handling & loading states                        │
│  ├── Dark mode support                                      │
│  ├── Mobile optimization                                    │
│  ├── Frontend deployment (Vercel/Netlify)                   │
│  └── Integration testing                                    │
│                                                              │
│  📋 Deliverable: User-facing chat web application           │
└─────────────────────────────────────────────────────────────┘
```

### Phase 4: Admin Frontend - 📋 PLANNED
```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 4 - 📋 PLANNED                      │
│                   Admin Frontend                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  📋 Week 10: Admin Dashboard                                │
│  ├── Admin authentication & authorization                    │
│  ├── User management dashboard                              │
│  ├── Document management interface                          │
│  ├── System statistics visualization                        │
│  └── API key management UI                                  │
│                                                              │
│  📋 Week 11: Data Ingestion UI                              │
│  ├── URL submission form with validation                    │
│  ├── File upload interface (drag & drop)                    │
│  ├── Crawl job status monitoring                            │
│  ├── Document preview and editing                           │
│  └── Bulk operations support                                │
│                                                              │
│  📋 Week 12: Integration & Launch                           │
│  ├── Full system integration testing                        │
│  ├── Admin role enforcement                                 │
│  ├── Production deployment                                  │
│  ├── Documentation and training materials                   │
│  └── Final testing & launch                                 │
│                                                              │
│  📋 Deliverable: Complete admin dashboard for data mgmt     │
│  ├── Final testing                                          │
│  └── Documentation                                          │
│                                                              │
│  Deliverable: Complete Nexora system                        │
└─────────────────────────────────────────────────────────────┘
```

---

---

## 8. Risk Analysis

### 8.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Twisted reactor conflicts | High | Medium | ✅ Investigating crochet configuration, considering alternative async approaches |
| Google Gemini API rate limits | Medium | High | ✅ Implement request queuing and caching strategies |
| MongoDB Atlas vector search performance | Medium | Low | ✅ Proper indexing, query optimization, monitoring |
| Large-scale crawling failures | Medium | Medium | ✅ Background jobs with retry logic, comprehensive error handling |
| JWT token security vulnerabilities | High | Low | ✅ Using industry-standard PyJWT with proper secret management |
| Multi-tenant data leakage | Critical | Low | ✅ Strict client_id filtering in all database queries |

### 8.2 Operational Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| API key exposure | Critical | Low | ✅ Environment variables, .env in .gitignore, documentation |
| Unauthorized data access | High | Medium | ✅ JWT authentication, role-based access control |
| Database backup failures | High | Low | ✅ MongoDB Atlas automated backups, tested restore procedures |
| Service downtime | Medium | Low | 📋 Implement health checks, monitoring, redundancy |
| Scalability bottlenecks | Medium | Medium | ✅ Multi-tenant architecture, horizontal scaling support |

---

## 9. Glossary

| Term | Definition |
|------|------------|
| **Multi-tenant** | Architecture where single instance serves multiple isolated clients |
| **JWT** | JSON Web Token - secure token format for authentication |
| **Chunking** | Splitting large documents into smaller, manageable pieces for embedding |
| **Embedding** | A vector (array of numbers) representing the semantic meaning of text (384-dim) |
| **Vector Search** | Finding similar items by comparing their vector representations |
| **RAG** | Retrieval-Augmented Generation - combining search with LLM generation |
| **LLM** | Large Language Model - AI model that generates text (e.g., Gemini) |
| **Spider** | A Scrapy component that defines how to crawl a website |
| **Playwright** | Browser automation tool for rendering JavaScript-heavy pages |
| **Client ID** | Unique identifier for tenant isolation in multi-tenant system |
| **Widget API Key** | Authentication key for embedded chat widgets |

---

## Appendix A: Environment Variables

```bash
# .env.example (SAFE TO COMMIT - Template only)

# MongoDB Configuration
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
MONGODB_DATABASE=nexora001

# Google AI Configuration
GOOGLE_API_KEY=your_google_api_key_here

# JWT Configuration
SECRET_KEY=your_super_secret_jwt_key_here_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Application Configuration
DEBUG=false
LOG_LEVEL=INFO

# Crawling Configuration
CRAWL_DELAY=1.0
MAX_CRAWL_DEPTH=2
USER_AGENT=Nexora-Bot/2.0

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

---

## Appendix B: Project Structure (Current - Phase 2)

```
nexora001/
├── .env                      # Secret configuration (NEVER COMMIT)
├── .env.example             # Example configuration (SAFE TO COMMIT)
├── .gitignore               # Git ignore rules
├── README.md                # Project documentation
├── requirements.txt         # Python dependencies (organized by category)
├── pyproject.toml           # Python project metadata
├── LICENSE                  # Project license
├── run.py                   # Console app entry point
├── run_api.py               # API server entry point
├── scrapy.cfg               # Scrapy configuration
│
├── docs/
│   ├── SRS.md               # This document (Software Requirements Spec)
│   └── Nexora001_API.postman_collection.json  # Complete API test collection
│
├── src/
│   └── nexora001/
│       ├── __init__.py
│       ├── main.py          # Console application
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