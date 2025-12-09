# Nexora001 🤖

<div align="center">

![Nexora001 Banner](https://img.shields.io/badge/Nexora001-AI_Knowledge_Base-blue? style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.13+-green?style=for-the-badge&logo=python)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?style=for-the-badge&logo=mongodb)
![Gemini](https://img.shields.io/badge/Google-Gemini_AI-blue?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An intelligent AI-powered knowledge base chatbot using Retrieval-Augmented Generation (RAG)**

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Roadmap](#-roadmap)

</div>

---

## 🌟 Overview

Nexora001 is a production-ready AI chatbot that:
- 🕷️ **Crawls websites** (including JavaScript-rendered pages)
- 📄 **Ingests documents** (PDF, DOCX)
- 🧠 **Generates vector embeddings** (384-dimensional)
- 🔍 **Performs semantic search** (cosine similarity)
- 💬 **Answers questions** using Google Gemini AI with source citations
- 🎨 **Beautiful console interface** with Rich UI

**Built with:** Python, Scrapy, Playwright, MongoDB Atlas, sentence-transformers, Google Gemini API

---

## ✨ Features

### 🕷️ **Intelligent Web Crawling**
- Static HTML crawling with Scrapy
- JavaScript-rendered pages with Playwright (Chromium)
- Configurable crawl depth
- Respects robots.txt
- Rate limiting & duplicate detection

### 📄 **Multi-Format Document Processing**
- **PDF** extraction with PyMuPDF
- **DOCX** parsing with python-docx
- **HTML** content extraction
- Intelligent text chunking (500 chars, 50 overlap)

### 🧠 **Vector Search & RAG**
- Local embeddings with sentence-transformers (all-MiniLM-L6-v2)
- 384-dimensional vectors stored in MongoDB
- Semantic similarity search
- Retrieval-Augmented Generation with Google Gemini 2.5 Flash

### 💬 **Conversational AI**
- Context-aware multi-turn conversations
- Conversation history tracking
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
```bash
python run.py
```

---

## 📖 Usage

### Basic Commands

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
├── . env                    # Secret configuration (NEVER COMMIT)
├── .env. example           # Example configuration
├── . gitignore            # Git ignore rules
├── README.md             # This file
├── requirements. txt      # Python dependencies
├── run.py                # Console application entry point
│
├── docs/
│   ├── SRS.md           # Software Requirements Specification
│   └── ARCHITECTURE.md  # Detailed architecture
│
├── src/
│   └── nexora001/
│       ├── __init__.py
│       ├── main.py           # Console application
│       ├── config.py         # Configuration management
│       │
│       ├── crawler/
│       │   ├── __init__.py
│       │   ├── spider.py     # Scrapy spider
│       │   ├── manager.py    # Crawler manager
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
│       │   └── mongodb. py    # MongoDB operations
│       │
│       └── rag/
│           ├── __init__.py
│           ├── retriever.py  # Document retrieval
│           ├── generator.py  # Answer generation
│           └── pipeline.py   # Complete RAG pipeline
│
└── tests/
    ├── __init__.py
    ├── test_crawler.py
    ├── test_processors.py
    └── test_rag.py
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

### 🚧 Phase 2: Backend API (In Progress)
- [ ] FastAPI REST API
- [ ] /api/chat endpoint
- [ ] /api/ingest endpoint
- [ ] Background job processing
- [ ] Deployment to Heroku/Railway

### 📅 Phase 3: Chat Frontend (Planned)
- [ ] React/Vue web application
- [ ] Chat interface
- [ ] Source display
- [ ] Responsive design

### 📅 Phase 4: Admin Frontend (Planned)
- [ ] URL submission form
- [ ] File upload interface
- [ ] Job status dashboard
- [ ] Content management

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
