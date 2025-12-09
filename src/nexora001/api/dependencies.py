"""
Shared dependencies for FastAPI routes. 
"""

import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from nexora001.rag.pipeline import RAGPipeline
from nexora001.storage.mongodb import MongoDBStorage


# ============================================================================
# GLOBAL INSTANCES (Singletons)
# ============================================================================

_rag_pipeline: Optional[RAGPipeline] = None
_storage: Optional[MongoDBStorage] = None


def get_rag_pipeline() -> RAGPipeline:
    """Get or create RAG pipeline instance (singleton)."""
    global _rag_pipeline
    
    if _rag_pipeline is None:
        from nexora001.rag.pipeline import create_rag_pipeline
        _rag_pipeline = create_rag_pipeline(
            embedding_provider="sentence_transformers",
            model_name="gemini-2.5-flash",
            top_k=5,
            min_similarity=0.3
        )
    
    return _rag_pipeline


def get_storage() -> MongoDBStorage:
    """Get or create storage instance (singleton)."""
    global _storage
    
    if _storage is None:
        _storage = MongoDBStorage()
    
    return _storage


def reset_dependencies():
    """Reset all singletons (useful for testing)."""
    global _rag_pipeline, _storage
    _rag_pipeline = None
    _storage = None