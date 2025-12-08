"""
Complete RAG pipeline that combines retrieval and generation.
"""

from typing import Dict, List, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from nexora001.rag.retriever import DocumentRetriever
from nexora001.rag.generator import AnswerGenerator


class RAGPipeline:
    """
    Complete RAG pipeline: Retrieve → Augment → Generate
    """
    
    def __init__(
        self,
        embedding_provider: str = "sentence_transformers",
        model_name: str = "gemini-2.5-flash",
        top_k: int = 5,
        min_similarity: float = 0.3,
        temperature: float = 0.7
    ):
        """
        Initialize the RAG pipeline.
        
        Args:
            embedding_provider: Embedding provider for retrieval
            model_name: Gemini model for generation
            top_k: Number of documents to retrieve
            min_similarity: Minimum similarity threshold
            temperature: LLM temperature
        """
        self.retriever = DocumentRetriever(
            embedding_provider=embedding_provider,
            top_k=top_k,
            min_similarity=min_similarity
        )
        
        self.generator = AnswerGenerator(
            model_name=model_name,
            temperature=temperature
        )
        
        self.conversation_history: List[Dict] = []
    
    def ask(
        self,
        query: str,
        use_history: bool = True,
        stream: bool = False
    ) -> Dict:
        """
        Ask a question and get an answer.
        
        Args:
            query: User's question
            use_history: Whether to use conversation history
            stream: Whether to stream the response
            
        Returns:
            Dictionary with answer, sources, and metadata
        """
        # Step 1: Retrieve relevant documents
        retrieval_result = self.retriever.retrieve_with_context(query)
        
        context = retrieval_result['context']
        sources = retrieval_result['sources']
        found_documents = retrieval_result['found_documents']
        
        # Step 2: Generate answer
        conversation = self.conversation_history if use_history else None
        
        if stream:
            # Return generator for streaming
            answer_generator = self.generator.generate_streaming_answer(
                query, context, conversation
            )
            
            return {
                'answer': answer_generator,  # Generator object
                'sources': sources,
                'found_documents': found_documents,
                'streaming': True
            }
        else:
            answer = self.generator.generate_answer(query, context, conversation)
            
            # Add to conversation history
            self.conversation_history.append({
                'role': 'user',
                'content': query
            })
            self.conversation_history.append({
                'role': 'assistant',
                'content': answer
            })
            
            return {
                'answer': answer,
                'sources': sources,
                'found_documents': found_documents,
                'streaming': False
            }
    
    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict]:
        """Get conversation history."""
        return self.conversation_history. copy()


# Convenience function
def create_rag_pipeline(**kwargs) -> RAGPipeline:
    """Create a RAG pipeline with custom settings."""
    return RAGPipeline(**kwargs)