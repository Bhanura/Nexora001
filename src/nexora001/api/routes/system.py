"""
System endpoints for status, documents management, etc.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent. parent. parent))

from nexora001.api.models import (
    SystemStatus,
    DocumentInfo,
    DocumentListResponse,
    DeleteResponse,
    ErrorResponse
)
from nexora001.api.dependencies import get_storage, get_rag_pipeline
from nexora001.storage.mongodb import MongoDBStorage
from nexora001.rag.pipeline import RAGPipeline

router = APIRouter()


# ============================================================================
# STATUS ENDPOINTS
# ============================================================================

@router.get(
    "/status",
    response_model=SystemStatus,
    summary="Get system status",
    description="Get the current status of the Nexora001 system"
)
async def get_status(
    storage: MongoDBStorage = Depends(get_storage),
    rag:  RAGPipeline = Depends(get_rag_pipeline)
):
    """Get system status."""
    try:
        # Get document stats
        stats = storage. get_stats()
        
        # Check database connection
        db_connected = storage.db is not None
        
        # Get embedding info
        embeddings_enabled = rag.retriever. embedding_generator is not None
        embedding_dim = None
        if embeddings_enabled: 
            embedding_dim = rag.retriever.embedding_generator. get_dimension()
        
        return SystemStatus(
            status="operational" if db_connected else "down",
            database_connected=db_connected,
            total_documents=stats['total_documents'],
            unique_sources=stats['unique_sources'],
            embeddings_enabled=embeddings_enabled,
            embedding_dimension=embedding_dim,
            llm_provider="Google Gemini 2.5 Flash",
            version="1.0.0"
        )
        
    except Exception as e: 
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


# ============================================================================
# DOCUMENT MANAGEMENT ENDPOINTS
# ============================================================================

@router.get(
    "/documents",
    response_model=DocumentListResponse,
    summary="List all documents",
    description="Get a paginated list of all indexed documents"
)
async def list_documents(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    source_type: Optional[str] = Query(None, description="Filter by type:  web, pdf, docx"),
    storage: MongoDBStorage = Depends(get_storage)
):
    """List all indexed documents with pagination."""
    try:
        # Build filter
        filter_query = {}
        if source_type:
            filter_query['metadata.source_type'] = source_type
        
        # Get documents from database - use storage. documents
        skip = (page - 1) * page_size
        cursor = storage.documents.find(filter_query).skip(skip).limit(page_size)
        
        documents = []
        for doc in cursor:
            documents.append(DocumentInfo(
                id=str(doc['_id']),
                title=doc['metadata']. get('title', 'Untitled'),
                url=doc['metadata'].get('source_url', ''),
                source_type=doc['metadata'].get('source_type', 'unknown'),
                created_at=doc['metadata'].get('created_at', datetime.now()),
                chunk_count=1,
                total_characters=len(doc['content'])
            ))
        
        # Get total count
        total = storage.documents.count_documents(filter_query)
        
        return DocumentListResponse(
            documents=documents,
            total=total,
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


@router.get(
    "/documents/stats",
    summary="Get document statistics",
    description="Get detailed statistics about indexed documents"
)
async def get_documents_stats(storage: MongoDBStorage = Depends(get_storage)):
    """Get detailed document statistics."""
    try:
        # Get stats
        stats = storage.get_stats()
        
        # Get breakdown by type - use storage.documents
        type_pipeline = [
            {
                "$group": {
                    "_id": "$metadata.source_type",
                    "count": {"$sum": 1}
                }
            }
        ]
        type_stats = list(storage.documents.aggregate(type_pipeline))
        
        return {
            "total_documents":  stats['total_documents'],
            "unique_sources": stats['unique_sources'],
            "average_chunk_size": stats['avg_chunk_size'],
            "by_type": {item['_id']: item['count'] for item in type_stats},
            "sources": stats['sources']
        }
        
    except Exception as e: 
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


@router.delete(
    "/documents",
    response_model=DeleteResponse,
    summary="Delete documents by source URL",
    description="Delete all documents from a specific source URL"
)
async def delete_documents(
    source_url:  str = Query(..., description="Source URL to delete"),
    storage: MongoDBStorage = Depends(get_storage)
):
    """Delete all documents from a specific source URL."""
    try:
        deleted_count = storage.delete_by_source(source_url)
        
        if deleted_count == 0:
            return DeleteResponse(
                success=False,
                deleted_count=0,
                message=f"No documents found for URL: {source_url}"
            )
        
        return DeleteResponse(
            success=True,
            deleted_count=deleted_count,
            message=f"Successfully deleted {deleted_count} documents from {source_url}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )


@router.delete(
    "/documents/all",
    response_model=DeleteResponse,
    summary="Delete all documents",
    description="⚠️ WARNING: Delete ALL documents from the database"
)
async def delete_all_documents(
    confirm: bool = Query(False, description="Must be true to confirm deletion"),
    storage: MongoDBStorage = Depends(get_storage)
):
    """⚠️ WARNING: Delete ALL documents from the database."""
    if not confirm:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "ConfirmationRequired",
                "message": "Set confirm=true to delete all documents"
            }
        )
    
    try:
        # Use storage.documents
        result = storage.documents.delete_many({})
        
        return DeleteResponse(
            success=True,
            deleted_count=result.deleted_count,
            message=f"Deleted all {result.deleted_count} documents"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalError",
                "message": str(e)
            }
        )