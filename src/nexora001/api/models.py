"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime


# ============================================================================
# CHAT MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User's question", min_length=1, max_length=1000)
    session_id: Optional[str] = Field(None, description="Session ID for conversation tracking")
    use_history: bool = Field(True, description="Whether to use conversation history")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is machine learning?",
                "session_id": "user123",
                "use_history": True
            }
        }


class Source(BaseModel):
    """Source citation model."""
    number: int
    title: str
    url: str
    score: float = Field(... , ge=0.0, le=1.0, description="Relevance score (0-1)")
    chunk_index: Optional[int] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str = Field(..., description="AI-generated answer")
    sources: List[Source] = Field(default_factory=list, description="Source citations")
    found_documents: int = Field(... , description="Number of documents found")
    session_id: Optional[str] = Field(None, description="Session ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Machine learning is a branch of AI.. .",
                "sources": [
                    {
                        "number": 1,
                        "title": "ML Guide",
                        "url": "https://example.com/ml",
                        "score": 0.85,
                        "chunk_index": 0
                    }
                ],
                "found_documents": 5,
                "session_id": "user123"
            }
        }


class ConversationHistory(BaseModel):
    """Conversation history model."""
    session_id: str
    messages: List[Dict[str, str]]


# ============================================================================
# INGEST MODELS
# ============================================================================

class CrawlRequest(BaseModel):
    """Request model for URL crawling."""
    url: HttpUrl = Field(..., description="URL to crawl")
    max_depth: int = Field(2, ge=0, le=5, description="Maximum crawl depth (0-5)")
    follow_links: bool = Field(True, description="Whether to follow internal links")
    use_playwright: bool = Field(False, description="Use browser for JavaScript rendering")
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://example.com",
                "max_depth": 2,
                "follow_links": True,
                "use_playwright": False
            }
        }


class CrawlResponse(BaseModel):
    """Response model for crawl request."""
    job_id: str = Field(..., description="Unique job identifier")
    status: str = Field(..., description="Job status: queued, running, completed, failed")
    url: str
    message: str = Field(..., description="Status message")


class IngestResponse(BaseModel):
    """Response model for file ingestion."""
    success: bool
    filename: str
    title: Optional[str] = None
    chunks_created: int
    total_characters: int
    message: str

class CrawlJobInfo(BaseModel):
    """Crawl job information model."""
    id: str = Field(..., alias="_id")
    url: str
    status: str  # running, completed, failed
    pages_crawled: int
    documents_created: int
    started_at: str
    completed_at: Optional[str] = None
    error_message: Optional[str] = None
    options: Optional[Dict[str, Any]] = None
    
    class Config:
        populate_by_name = True

class CrawlJobListResponse(BaseModel):
    """Response for crawl job listing."""
    jobs: List[CrawlJobInfo]
    total: int


# ============================================================================
# SYSTEM MODELS
# ============================================================================

class SystemStatus(BaseModel):
    """System status model."""
    status: str = Field(..., description="System status: operational, degraded, down")
    database_connected: bool
    total_documents: int
    unique_sources: int
    embeddings_enabled: bool
    embedding_dimension: Optional[int] = None
    llm_provider: str
    version: str


class DocumentInfo(BaseModel):
    """Document information model."""
    id: str
    title: str
    url: str
    source_type: str = Field(..., description="Type: web, pdf, docx")
    created_at: datetime
    chunk_count: int
    total_characters: int


class DocumentListResponse(BaseModel):
    """Response for document listing."""
    documents: List[DocumentInfo]
    total: int
    page: int
    page_size: int


class DeleteResponse(BaseModel):
    """Response for delete operation."""
    success: bool
    deleted_count: int
    message: str


# ============================================================================
# ERROR MODELS
# ============================================================================

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid URL format",
                "details": {"field": "url"}
            }
        }


# ============================================================================
# CHATBOT SETTINGS MODELS
# ============================================================================

class ChatbotSettings(BaseModel):
    """Response model for chatbot configuration."""
    chatbot_name: str = Field(default="AI Assistant", description="Custom chatbot name")
    chatbot_greeting: str = Field(default="Hello! How can I help you today?", description="Welcome message")
    chatbot_personality: str = Field(default="friendly and helpful", description="Bot personality traits")
    
    class Config:
        json_schema_extra = {
            "example": {
                "chatbot_name": "TechSupport Pro",
                "chatbot_greeting": "Welcome to TechCorp! How can we assist you?",
                "chatbot_personality": "professional and technical"
            }
        }


class UpdateChatbotSettingsRequest(BaseModel):
    """Request model for updating chatbot settings."""
    chatbot_name: Optional[str] = Field(None, min_length=1, max_length=100, description="Custom chatbot name")
    chatbot_greeting: Optional[str] = Field(None, min_length=1, max_length=500, description="Welcome message")
    chatbot_personality: Optional[str] = Field(None, min_length=1, max_length=500, description="Bot personality")
    
    class Config:
        json_schema_extra = {
            "example": {
                "chatbot_name": "TechSupport Pro",
                "chatbot_greeting": "Welcome! How can we help?",
                "chatbot_personality": "professional, concise, and technical"
            }
        }