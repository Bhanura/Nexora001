"""
MongoDB storage operations for Nexora001. 
Handles connections, document storage, and retrieval.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
import os
from dotenv import load_dotenv

load_dotenv()


class MongoDBStorage:
    """MongoDB storage handler for Nexora001."""
    
    def __init__(self, uri: Optional[str] = None, database: Optional[str] = None):
        """
        Initialize MongoDB connection.
        
        Args:
            uri: MongoDB connection URI (defaults to env var)
            database: Database name (defaults to env var)
        """
        self.uri = uri or os.getenv("MONGODB_URI")
        self.database_name = database or os.getenv("MONGODB_DATABASE", "nexora001")
        
        if not self.uri:
            raise ValueError("MongoDB URI not provided and MONGODB_URI env var not set")
        
        self.client: MongoClient = MongoClient(self.uri)
        self. db: Database = self.client[self.database_name]
        
        # Collections
        self.documents: Collection = self.db["documents"]
        self.crawl_jobs: Collection = self.db["crawl_jobs"]
        
        # Create indexes for better performance
        self._create_indexes()
    
    def _create_indexes(self):
        """Create database indexes for efficient querying."""
        # Index on source URL for quick lookups
        self.documents. create_index([("metadata.source_url", ASCENDING)])
        
        # Index on crawled_at for time-based queries
        self.documents.create_index([("metadata.crawled_at", ASCENDING)])
        
        # Index on source_type
        self.documents.create_index([("metadata.source_type", ASCENDING)])
        
        # Index for crawl jobs
        self.crawl_jobs.create_index([("url", ASCENDING)])
        self.crawl_jobs.create_index([("status", ASCENDING)])
    
    def store_document(
        self,
        content: str,
        source_url: str,
        source_type: str = "web",
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Store a document in MongoDB.
        
        Args:
            content: The text content
            source_url: URL or identifier of the source
            source_type: Type of source ("web", "pdf", "docx")
            title: Document title
            metadata: Additional metadata
            
        Returns:
            Document ID (string)
        """
        doc = {
            "content": content,
            "metadata": {
                "source_url": source_url,
                "source_type": source_type,
                "title": title or source_url,
                "crawled_at": datetime.utcnow(),
                **(metadata or {})
            }
        }
        
        result = self.documents.insert_one(doc)
        return str(result.inserted_id)
    
    def get_document_by_url(self, source_url: str) -> Optional[Dict]:
        """
        Retrieve a document by its source URL. 
        
        Args:
            source_url: The source URL to search for
            
        Returns:
            Document dict or None if not found
        """
        return self.documents.find_one({"metadata.source_url": source_url})
    
    def url_exists(self, source_url: str) -> bool:
        """
        Check if a URL has already been crawled.
        
        Args:
            source_url: The URL to check
            
        Returns:
            True if URL exists in database
        """
        return self.documents.count_documents(
            {"metadata.source_url": source_url}
        ) > 0
    
    def get_all_documents(self, limit: int = 100) -> List[Dict]:
        """
        Get all documents from the database.
        
        Args:
            limit: Maximum number of documents to return
            
        Returns:
            List of document dictionaries
        """
        return list(self.documents.find(). limit(limit))
    
    def count_documents(self, source_type: Optional[str] = None) -> int:
        """
        Count documents in the database.
        
        Args:
            source_type: Optional filter by source type
            
        Returns:
            Number of documents
        """
        query = {"metadata.source_type": source_type} if source_type else {}
        return self.documents.count_documents(query)
    
    def delete_by_url(self, source_url: str) -> int:
        """
        Delete documents by source URL.
        
        Args:
            source_url: The source URL to delete
            
        Returns:
            Number of documents deleted
        """
        result = self. documents.delete_many({"metadata.source_url": source_url})
        return result.deleted_count
    
    def create_crawl_job(self, url: str, options: Optional[Dict] = None) -> str:
        """
        Create a crawl job record.
        
        Args:
            url: URL to crawl
            options: Crawl options (depth, follow_links, etc.)
            
        Returns:
            Job ID
        """
        job = {
            "url": url,
            "status": "pending",
            "pages_crawled": 0,
            "documents_created": 0,
            "started_at": datetime.utcnow(),
            "completed_at": None,
            "error_message": None,
            "options": options or {}
        }
        
        result = self.crawl_jobs. insert_one(job)
        return str(result.inserted_id)
    
    def update_crawl_job(
        self,
        job_id: str,
        status: Optional[str] = None,
        pages_crawled: Optional[int] = None,
        documents_created: Optional[int] = None,
        error_message: Optional[str] = None
    ):
        """Update a crawl job's status."""
        from bson import ObjectId
        
        updates = {}
        if status:
            updates["status"] = status
            if status in ["completed", "failed"]:
                updates["completed_at"] = datetime.utcnow()
        if pages_crawled is not None:
            updates["pages_crawled"] = pages_crawled
        if documents_created is not None:
            updates["documents_created"] = documents_created
        if error_message:
            updates["error_message"] = error_message
        
        if updates:
            self.crawl_jobs.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": updates}
            )
    
    def get_crawl_job(self, job_id: str) -> Optional[Dict]:
        """Get a crawl job by ID."""
        from bson import ObjectId
        return self.crawl_jobs.find_one({"_id": ObjectId(job_id)})
    
    def close(self):
        """Close the MongoDB connection."""
        self.client. close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self. close()


# Convenience function
def get_storage() -> MongoDBStorage:
    """Get a MongoDB storage instance with default configuration."""
    return MongoDBStorage()