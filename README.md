# Nexora001 🤖

AI-Powered Knowledge Base Chatbot with RAG (Retrieval-Augmented Generation)

[![Python 3.11+](https://img. shields.io/badge/python-3. 11+-blue.svg)](https://www. python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

Nexora001 is an intelligent chatbot that:
- 🕷️ **Crawls** websites and extracts content (including JavaScript-rendered pages)
- 📄 **Processes** documents (PDF, DOCX, HTML)
- 🧠 **Stores** data in MongoDB with vector embeddings
- 🔍 **Searches** using semantic similarity
- 💬 **Answers** questions using Google Gemini AI

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐
│  Chat Frontend  │     │  Admin Frontend │
└────────┬────────┘     └────────┬────────┘
         │                       │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │    FastAPI Backend    │
         │    + LangChain RAG    │
         └───────────┬───────────┘
                     │
    ┌────────────────┼────────────────┐
    │                │                │
    ▼                ▼                ▼
┌─────────┐   ┌───────────┐   ┌───────────┐
│ Scrapy  │   │  MongoDB  │   │  Gemini   │
│Playwright│   │  Atlas    │   │   API     │
└─────────┘   └───────────┘   └───────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- MongoDB Atlas account (free tier works)
- Google AI API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github. com/YOUR_USERNAME/Nexora001.git
   cd Nexora001
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   playwright install chromium
   ```

4. **Configure environment**
   ```bash
   # Copy example configuration
   copy .env.example . env   # Windows
   cp .env.example . env     # macOS/Linux
   
   # Edit .env with your actual values
   ```

5. **Run the application**
   ```bash
   python -m nexora001. main
   ```

## ⚙️ Configuration

Create a `.env` file with:

```env
# MongoDB Atlas
MONGODB_URI=mongodb+srv://username:password@cluster. mongodb.net/
MONGODB_DATABASE=nexora001

# Google AI
GOOGLE_API_KEY=your_api_key_here
```

## 📖 Usage

### Console Commands

```
nexora001> help                    # Show available commands
nexora001> crawl https://example. com    # Crawl a website
nexora001> ingest document.pdf     # Ingest a PDF file
nexora001> ask What is AI?         # Ask a question
nexora001> status                  # View system status
nexora001> exit                    # Exit application
```

## 🗺️ Development Roadmap

- [x] Phase 1: Project Setup
- [ ] Phase 1: Console Application
- [ ] Phase 2: Backend API
- [ ] Phase 3: Chat Frontend
- [ ] Phase 4: Admin Frontend

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3. 11+ |
| Web Crawling | Scrapy + Playwright |
| Document Processing | Unstructured. io, PyMuPDF |
| Database | MongoDB Atlas |
| Vector Search | MongoDB Atlas Vector Search |
| AI/RAG | LangChain + Google Gemini |
| API Framework | FastAPI |

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

- Author: Bhanura
- Project Link: https://github. com/YOUR_USERNAME/Nexora001