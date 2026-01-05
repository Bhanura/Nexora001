"""
Migration script: MongoDB Atlas → Self-hosted MongoDB + Qdrant
Migrates documents and creates vector embeddings in Qdrant
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv
from nexora001.storage.qdrant_storage import get_qdrant
from nexora001.processors.embeddings import get_embedding_generator
from tqdm import tqdm

load_dotenv()

def migrate_to_self_hosted():
    """Migrate from Atlas to self-hosted MongoDB + Qdrant."""
    
    print("=" * 60)
    print("MIGRATION: Atlas → Self-Hosted MongoDB + Qdrant")
    print("=" * 60)
    
    # Source: MongoDB Atlas
    atlas_uri = input("Enter MongoDB Atlas URI: ")
    atlas_client = MongoClient(atlas_uri)
    atlas_db = atlas_client["nexora001"]
    
    # Destination: Local MongoDB
    local_uri = os.getenv("MONGODB_URI", "mongodb://admin:changeme123@localhost:27017")
    local_client = MongoClient(local_uri)
    local_db = local_client["nexora001"]
    
    # Qdrant for vectors
    qdrant = get_qdrant()
    
    print("\n1️⃣ Migrating Users...")
    users = list(atlas_db.users.find())
    if users:
        local_db.users.insert_many(users)
        print(f"   ✓ Migrated {len(users)} users")
    
    print("\n2️⃣ Migrating Documents to MongoDB...")
    documents = list(atlas_db.documents.find())
    print(f"   Found {len(documents)} documents")
    
    if not documents:
        print("   ⚠️  No documents to migrate")
        return
    
    # Remove old _id for clean insert
    for doc in documents:
        doc.pop('_id', None)
    
    result = local_db.documents.insert_many(documents)
    print(f"   ✓ Migrated {len(result.inserted_ids)} documents")
    
    print("\n3️⃣ Creating Vector Embeddings in Qdrant...")
    embedding_gen = get_embedding_generator()
    
    for i, doc in enumerate(tqdm(documents, desc="Processing")):
        try:
            # Check if has embedding
            if 'embedding' not in doc:
                # Generate embedding
                content = doc.get('content', '')
                if len(content) < 10:
                    continue
                embedding = embedding_gen.generate_embedding(content)
            else:
                embedding = doc['embedding']
            
            # Store in Qdrant
            qdrant.store_embedding(
                doc_id=str(result.inserted_ids[i]),
                embedding=embedding,
                client_id=doc.get('client_id', ''),
                content=doc.get('content', ''),
                metadata=doc.get('metadata', {})
            )
            
        except Exception as e:
            print(f"   ⚠️  Error processing doc {i}: {e}")
            continue
    
    print("\n4️⃣ Migrating API Keys...")
    api_keys = list(atlas_db.api_keys.find())
    if api_keys:
        local_db.api_keys.insert_many(api_keys)
        print(f"   ✓ Migrated {len(api_keys)} API keys")
    
    print("\n" + "=" * 60)
    print("✅ Migration Complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update .env to use local MongoDB")
    print("2. Set USE_QDRANT=true in .env")
    print("3. Restart your application")
    print("4. Test that everything works")
    print("5. Once confirmed, you can stop using Atlas")
    
    atlas_client.close()
    local_client.close()

if __name__ == "__main__":
    migrate_to_self_hosted()
