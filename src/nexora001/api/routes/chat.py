"""
Chat endpoints for RAG question answering.
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent. parent.parent. parent))

from nexora001. api.models import (
    ChatRequest,
    ChatResponse,
    Source,
    ErrorResponse
)
from nexora001.api.dependencies import get_rag_pipeline
from nexora001. rag.pipeline import RAGPipeline

router = APIRouter()


@router.post(
    "/",
    response_model=ChatResponse,
    responses={
        200: {"description": "Successful response"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="Ask a question",
    description="Ask a question and get an AI-generated answer with source citations"
)
async def chat(
    request: ChatRequest,
    rag: RAGPipeline = Depends(get_rag_pipeline)
):
    """
    Ask a question to the AI chatbot.
    
    The system will:
    1. Search for relevant documents in the knowledge base
    2.  Retrieve the most similar content
    3. Generate an answer using Google Gemini AI
    4. Return the answer with source citations
    """
    try:
        # Ask the RAG system
        result = rag.ask(
            query=request.message,
            use_history=request.use_history
        )
        
        # Convert sources to response model
        sources = [
            Source(
                number=src['number'],
                title=src['title'],
                url=src['url'],
                score=src['score'],
                chunk_index=src. get('chunk_index')
            )
            for src in result['sources']
        ]
        
        return ChatResponse(
            answer=result['answer'],
            sources=sources,
            found_documents=result['found_documents'],
            session_id=request.session_id
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


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
        raise HTTPException(status_code=500, detail=str(e))


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
        raise HTTPException(status_code=500, detail=str(e))