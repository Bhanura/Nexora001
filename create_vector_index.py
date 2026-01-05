"""
Script to create MongoDB Atlas Vector Search Index
Run this once to set up vector search capability
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def create_vector_search_index():
    """Create vector search index in MongoDB Atlas."""
    
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DATABASE", "nexora001")
    
    if not uri:
        print("❌ Error: MONGODB_URI not found in .env")
        return
    
    print(f"Connecting to MongoDB Atlas...")
    client = MongoClient(uri)
    db = client[db_name]
    collection = db["documents"]
    
    # Check if index already exists
    try:
        indexes = list(collection.list_search_indexes())
        if any(idx.get('name') == 'vector_index' for idx in indexes):
            print("✓ Vector index 'vector_index' already exists!")
            return
    except Exception as e:
        print(f"Note: {e}")
    
    # Create vector search index
    print("Creating vector search index...")
    print("⚠️  This requires MongoDB Atlas (not local MongoDB)")
    print("⚠️  Index creation may take 2-5 minutes")
    
    try:
        # Note: This requires MongoDB Atlas M10+ cluster or free tier with Search enabled
        result = collection.create_search_index(
            {
                "name": "vector_index",
                "type": "vectorSearch",
                "definition": {
                    "fields": [
                        {
                            "type": "vector",
                            "path": "embedding",
                            "numDimensions": 384,  # for all-MiniLM-L6-v2
                            "similarity": "cosine"
                        },
                        {
                            "type": "filter",
                            "path": "client_id"
                        }
                    ]
                }
            }
        )
        
        print(f"✅ Vector search index created successfully!")
        print(f"   Index name: vector_index")
        print(f"   Dimensions: 384")
        print(f"   Similarity: cosine")
        print(f"\n⏳ Wait 2-5 minutes for index to finish building")
        print(f"   Then restart your API server")
        
    except Exception as e:
        print(f"\n❌ Error creating index: {e}")
        print(f"\n💡 If you see 'command not found' or 'unsupported' error:")
        print(f"   1. Make sure you're using MongoDB Atlas (not local)")
        print(f"   2. Use the Atlas UI method instead (easier):")
        print(f"      - Go to https://cloud.mongodb.com")
        print(f"      - Select your cluster")
        print(f"      - Click 'Atlas Search' tab")
        print(f"      - Create search index with the JSON config shown above")
        
    finally:
        client.close()

if __name__ == "__main__":
    create_vector_search_index()
