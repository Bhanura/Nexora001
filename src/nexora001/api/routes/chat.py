"""
Chat endpoints for RAG question answering.
"""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from nexora001.api.models import ChatRequest, ChatResponse, Source, ErrorResponse
from nexora001.api.dependencies import get_rag_pipeline, get_current_user, get_user_from_api_key
from nexora001.rag.pipeline import RAGPipeline

router = APIRouter()


# ============================================================================
# INTERNAL DASHBOARD ENDPOINT (JWT Authentication)
# ============================================================================

@router.post(
    "/",
    response_model=ChatResponse,
    responses={
        200: {"description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Ask a question (Dashboard)",
    description="Ask a question and get an AI-generated answer with source citations. Requires JWT authentication."
)
async def chat_dashboard(
    request: ChatRequest,
    rag: RAGPipeline = Depends(get_rag_pipeline),
    current_user: dict = Depends(get_current_user)  # <--- JWT Authentication
):
    """
    Internal Chat (Dashboard): Uses JWT Authentication.
    
    The system will:
    1. Search for relevant documents in the knowledge base
    2. Retrieve the most similar content
    3. Generate an answer using Google Gemini AI
    4. Return the answer with source citations
    
    Only searches documents belonging to the authenticated user.
    """
    try:
        # Create a session ID linked to the user
        session_id = request.session_id or f"dash-{current_user['_id']}"
        
        # Ask the RAG system with client_id for data isolation
        result = rag.ask(
            query=request.message,
            client_id=current_user["_id"],  # <--- Data Isolation
            session_id=session_id,
            use_history=request.use_history
        )
        
        # Convert sources to response model
        sources = [
            Source(
                number=src['number'],
                title=src['title'],
                url=src['url'],
                score=src['score'],
                chunk_index=src.get('chunk_index')
            )
            for src in result['sources']
        ]
        
        return ChatResponse(
            answer=result['answer'],
            sources=sources,
            found_documents=result['found_documents'],
            session_id=session_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


# ============================================================================
# PUBLIC WIDGET ENDPOINT (API Key Authentication)
# ============================================================================

@router.post(
    "/widget",
    response_model=ChatResponse,
    responses={
        200: {"description": "Successful response"},
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Ask a question (Widget)",
    description="Public Chat (Widget): Uses API Key Authentication via X-API-Key header."
)
async def chat_widget(
    request: ChatRequest,
    x_api_key: str = Header(..., description="Client API Key"),
    rag: RAGPipeline = Depends(get_rag_pipeline),
    client_id: str = Depends(get_user_from_api_key)  # <--- Validates Key
):
    """
    Public Chat (Widget): Uses API Key Authentication.
    
    The system will:
    1. Validate the API key from X-API-Key header
    2. Search for relevant documents belonging to the API key owner
    3. Retrieve the most similar content
    4. Generate an answer using Google Gemini AI
    5. Return the answer with source citations
    """
    try:
        # For public widgets, we rely on the client_id extracted from the key
        session_id = request.session_id or "anonymous-visitor"
        
        result = rag.ask(
            query=request.message,
            client_id=client_id,
            session_id=session_id,
            use_history=request.use_history
        )
        
        sources = [
            Source(
                number=src['number'],
                title=src['title'],
                url=src['url'],
                score=src['score'],
                chunk_index=src.get('chunk_index')
            )
            for src in result['sources']
        ]
        
        return ChatResponse(
            answer=result['answer'],
            sources=sources,
            found_documents=result['found_documents'],
            session_id=session_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


# ============================================================================
# HISTORY MANAGEMENT ENDPOINTS
# ============================================================================

@router.post(
    "/clear-history",
    summary="Clear conversation history",
    description="Clear the conversation history for a fresh start"
)
async def clear_history(rag: RAGPipeline = Depends(get_rag_pipeline)):
    """Clear conversation history."""
    try:
        rag.clear_history()
        return {"success": True, "message": "Conversation history cleared"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


@router.get(
    "/history",
    summary="Get conversation history",
    description="Retrieve the conversation history"
)
async def get_history(rag: RAGPipeline = Depends(get_rag_pipeline)):
    """Get conversation history."""
    try:
        history = rag.get_history()
        return {"messages": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )