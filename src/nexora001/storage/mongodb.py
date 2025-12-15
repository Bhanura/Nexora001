"""
MongoDB storage operations for Nexora001 - Multi-Tenant Edition.
"""

from typing import List, Dict, Optional, Any
from datetime import datetime
from pymongo import MongoClient, ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database
from bson import ObjectId
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

class MongoDBStorage:
    def __init__(self, uri: Optional[str] = None, database: Optional[str] = None):
        self.uri = uri or os.getenv("MONGODB_URI")
        self.database_name = database or os.getenv("MONGODB_DATABASE", "nexora001")
        
        if not self.uri:
            raise ValueError("MongoDB URI not provided")
        
        self.client: MongoClient = MongoClient(self.uri)
        self.db: Database = self.client[self.database_name]
        
        # --- UPDATED COLLECTIONS ---
        self.users: Collection = self.db["users"]            # NEW: Stores user creds
        self.documents: Collection = self.db["documents"]
        self.crawl_jobs: Collection = self.db["crawl_jobs"]
        self.api_keys: Collection = self.db["api_keys"]      # NEW: Stores widget keys
        self.chat_sessions: Collection = self.db["chat_sessions"]  # NEW: Stores chat history
        
        self._create_indexes()
    
    def _create_indexes(self):
        """Create indexes safely, handling conflicts."""
        try:
            # NEW: Filter by client_id first, then source_url
            self.documents.create_index([("client_id", ASCENDING), ("metadata.source_url", ASCENDING)])
        except Exception:
            pass  # Index already exists
        
        try:
            self.users.create_index("email", unique=True)
        except Exception:
            pass
        
        try:
            self.api_keys.create_index("key", unique=True)
        except Exception:
            pass
        
        try:
            self.crawl_jobs.create_index([("client_id", ASCENDING)])
        except Exception:
            pass
        
        try:
            self.chat_sessions.create_index("session_id", unique=True)
        except Exception:
            pass
        
        # For last_active, keep the existing index with TTL if it exists
        # Don't try to recreate it
        try:
            existing_indexes = self.chat_sessions.index_information()
            if "last_active_1" not in existing_indexes:
                # Only create if it doesn't exist at all
                self.chat_sessions.create_index("last_active", expireAfterSeconds=86400)
        except Exception:
            pass  # Index exists or cannot be created

    # ==========================================
    # 1. AUTH & USER MANAGEMENT
    # ==========================================
    def create_user(self, email: str, password_hash: str, name: str) -> str:
        user = {
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "role": "client_admin",
            "created_at": datetime.utcnow(),
            "status": "active"
        }
        return str(self.users.insert_one(user).inserted_id)

    def update_user_profile(self, user_id: str, updates: Dict) -> bool:
            """Update user details (name, email, etc)."""
            # Protect against changing role/id/password via this simple method
            safe_updates = {k: v for k, v in updates.items() if k in ['name', 'email']}
            if not safe_updates: return False
            
            result = self.users.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": safe_updates}
            )
            return result.modified_count > 0

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        return self.users.find_one({"_id": ObjectId(user_id)})

    # ==========================================
    # 2. API KEY
    # ==========================================

    def get_or_create_api_key(self, client_id: str) -> str:
        """Return existing key if found, otherwise create new one."""
        existing = self.api_keys.find_one({"client_id": client_id})
        if existing:
            return existing["key"]
            
        key = f"nx_{secrets.token_urlsafe(24)}"
        self.api_keys.insert_one({
            "key": key,
            "client_id": client_id,
            "created_at": datetime.utcnow()
        })
        return key

    def validate_api_key(self, key: str) -> Optional[str]:
        doc = self.api_keys.find_one({"key": key})
        if doc:
            user = self.users.find_one({"_id": ObjectId(doc['client_id'])})
            if user and user.get('status') == 'banned':
                return None
            return doc['client_id']
        return None

    # ==========================================
    # 3. SUPER ADMIN ACTIONS
    # ==========================================

    def get_all_users(self) -> List[Dict]:
        users = list(self.users.find({}, {"password_hash": 0}))
        for user in users:
            uid = str(user["_id"])
            user["doc_count"] = self.documents.count_documents({"client_id": uid})
            user["api_keys"] = self.api_keys.count_documents({"client_id": uid})
        return users

    def set_user_status(self, email: str, status: str) -> bool:
        """Ban or Unban a user (status: 'active' or 'banned')."""
        result = self.users.update_one(
            {"email": email},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0

    def delete_user_full(self, email: str) -> int:
        """
        Hard Delete: Removes User + Documents + Keys + Jobs + Chats.
        Returns total deleted count.
        """
        user = self.users.find_one({"email": email})
        if not user: return 0
        
        uid = str(user["_id"])
        
        # Cascade delete
        d1 = self.documents.delete_many({"client_id": uid}).deleted_count
        d2 = self.api_keys.delete_many({"client_id": uid}).deleted_count
        d3 = self.crawl_jobs.delete_many({"client_id": uid}).deleted_count
        d4 = self.users.delete_one({"_id": user["_id"]}).deleted_count
        
        return d1 + d2 + d3 + d4

    # ==========================================
    # 4. DOCUMENT MANAGEMENT
    # ==========================================
    def store_document(self, client_id: str, content: str, source_url: str, source_type: str = "web", title: str = None, metadata: Dict = None) -> str:
        # NOTICE: client_id is now the FIRST required argument
        doc = {
            "client_id": client_id,  # <--- DATA ISOLATION
            "content": content,
            "metadata": {
                "source_url": source_url,
                "source_type": source_type,
                "title": title or source_url,
                "crawled_at": datetime.utcnow(),
                **(metadata or {})
            }
        }
        return str(self.documents.insert_one(doc).inserted_id)

    def store_document_with_embedding(self, client_id: str, content: str, embedding: List[float], source_url: str, source_type: str = "web", title: str = None, chunk_index: int = 0, total_chunks: int = 1, metadata: Dict = None) -> str:
        doc = {
            "client_id": client_id,  # <--- DATA ISOLATION
            "content": content,
            "embedding": embedding,
            "metadata": {
                "source_url": source_url,
                "source_type": source_type,
                "title": title or source_url,
                "crawled_at": datetime.utcnow(),
                "chunk_index": chunk_index,
                "total_chunks": total_chunks,
                **(metadata or {})
            }
        }
        return str(self.documents.insert_one(doc).inserted_id)

    # --- UPDATED SEARCH METHODS ---
    def vector_search(self, client_id: str, query_embedding: List[float], limit: int = 5, min_score: float = 0.0) -> List[Dict]:
        # 1. Fetch only documents belonging to this client
        # In production, use Atlas Search pipeline: {"$search": { ..., "filter": {"client_id": client_id} }}
        # For now (simple python implementation):
        
        candidates = list(self.documents.find(
            {"client_id": client_id, "embedding": {"$exists": True}}, 
            {"content": 1, "embedding": 1, "metadata": 1}
        ))
        
        results = []
        for doc in candidates:
            score = self._cosine_similarity(query_embedding, doc['embedding'])
            if score >= min_score:
                doc['similarity_score'] = score
                del doc['embedding'] # Save bandwidth
                results.append(doc)
        
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results[:limit]
    
    def close(self):
        self.client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def url_exists(self, client_id: str, source_url: str) -> bool:
        """Check if a URL has already been crawled by THIS client."""
        return self.documents.count_documents(
            {"client_id": client_id, "metadata.source_url": source_url}
        ) > 0

    def count_documents(self, client_id: str) -> int:
        """Count total documents for a specific client."""
        return self.documents.count_documents({"client_id": client_id})

    def delete_document_by_id(self, client_id: str, doc_id: str) -> bool:
        """Delete a single document chunk by its MongoDB _id."""
        try:
            # We must convert the string ID to a MongoDB ObjectId
            from bson import ObjectId
            result = self.documents.delete_one(
                {"_id": ObjectId(doc_id), "client_id": client_id}
            )
            return result.deleted_count > 0
        except Exception:
            return False

    def delete_by_url(self, client_id: str, source_url: str) -> int:
        """Delete a client's documents for a specific URL."""
        result = self.documents.delete_many(
            {"client_id": client_id, "metadata.source_url": source_url}
        )
        return result.deleted_count
    
    @staticmethod
    def _cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if len(vec1) != len(vec2): 
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        magnitude1 = sum(a * a for a in vec1) ** 0.5
        magnitude2 = sum(b * b for b in vec2) ** 0.5
        
        if magnitude1 == 0 or magnitude2 == 0: 
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def add_chat_message(self, session_id: str, role: str, content: str):
        """Add a message to a chat session."""
        self.chat_sessions.update_one(
            {"session_id": session_id},
            {
                "$push": {"messages": {"role": role, "content": content, "timestamp": datetime.utcnow()}},
                "$set": {"last_active": datetime.utcnow()}
            },
            upsert=True
        )

    # ==========================================
    # 6. CRAWL JOB MANAGEMENT
    # ==========================================

    def create_crawl_job(self, client_id: str, url: str, options: Dict = None) -> str:
        """Create a new crawl job record."""
        job = {
            "client_id": client_id,
            "url": url,
            "status": "running",
            "pages_crawled": 0,
            "documents_created": 0,
            "started_at": datetime.utcnow(),
            "completed_at": None,
            "error_message": None,
            "options": options or {}
        }
        result = self.crawl_jobs.insert_one(job)
        return str(result.inserted_id)

    def update_crawl_job(self, job_id: str, status: str = None, pages_crawled: int = None, documents_created: int = None, error_message: str = None):
        """Update an existing crawl job."""
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
            
    # ==========================================
    # 7. SUPER ADMIN METHODS
    # ==========================================
    
    def get_all_users(self) -> List[Dict]:
        """Super Admin: Get list of all clients with usage stats."""
        users = list(self.users.find({}, {"password_hash": 0})) # Hide passwords
        
        # Attach usage stats to each user
        for user in users:
            user_id = str(user["_id"])
            user["doc_count"] = self.documents.count_documents({"client_id": user_id})
            user["api_keys"] = self.api_keys.count_documents({"client_id": user_id})
            
        return users

    def ban_user(self, email: str) -> bool:
        """Super Admin: Ban a client."""
        result = self.users.update_one(
            {"email": email},
            {"$set": {"status": "banned"}}
        )
        return result.modified_count > 0

    def unban_user(self, email: str) -> bool:
        """Super Admin: Activate a client."""
        result = self.users.update_one(
            {"email": email},
            {"$set": {"status": "active"}}
        )
        return result.modified_count > 0
        
    def validate_api_key(self, key: str) -> Optional[str]:
        """Widget: Get client_id from API key."""
        doc = self.api_keys.find_one({"key": key})
        if doc:
            # Check if the OWNER is banned
            user = self.users.find_one({"_id": ObjectId(doc['client_id'])})
            if user and user.get('status') == 'banned':
                return None
            return doc['client_id']
        return None
    
    def get_stats(self, client_id: Optional[str] = None) -> Dict[str, Any]:
        """Get statistics about documents in the database."""
        try:
            # Build filter
            filter_query = {}
            if client_id:
                filter_query["client_id"] = client_id
            
            # Total documents
            total_documents = self.documents.count_documents(filter_query)
            
            # Get unique sources
            sources_pipeline = [
                {"$match": filter_query} if filter_query else {"$match": {}},
                {"$group": {"_id": "$metadata.source_url"}},
                {"$count": "total"}
            ]
            sources_result = list(self.documents.aggregate(sources_pipeline))
            unique_sources = sources_result[0]["total"] if sources_result else 0
            
            # Calculate average chunk size
            avg_pipeline = [
                {"$match": filter_query} if filter_query else {"$match": {}},
                {"$group": {"_id": None, "avg_size": {"$avg": {"$strLenCP": "$content"}}}}
            ]
            avg_result = list(self.documents.aggregate(avg_pipeline))
            avg_chunk_size = int(avg_result[0]["avg_size"]) if avg_result else 0
            
            # Get list of sources
            sources_list_pipeline = [
                {"$match": filter_query} if filter_query else {"$match": {}},
                {"$group": {
                    "_id": "$metadata.source_url",
                    "count": {"$sum": 1},
                    "type": {"$first": "$metadata.source_type"}
                }},
                {"$limit": 100}  # Limit to avoid huge result sets
            ]
            sources_data = list(self.documents.aggregate(sources_list_pipeline))
            sources = [
                {
                    "url": item["_id"],
                    "count": item["count"],
                    "type": item.get("type", "unknown")
                }
                for item in sources_data
            ]
            
            return {
                "total_documents": total_documents,
                "unique_sources": unique_sources,
                "avg_chunk_size": avg_chunk_size,
                "sources": sources
            }
        except Exception as e:
            # Return empty stats on error
            return {
                "total_documents": 0,
                "unique_sources": 0,
                "avg_chunk_size": 0,
                "sources": []
            }

def get_storage():
    return MongoDBStorage()