"""
Check if MongoDB Atlas Vector Search index is ready
"""

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def check_vector_index_status():
    uri = os.getenv("MONGODB_URI")
    db_name = os.getenv("MONGODB_DATABASE", "nexora001")
    
    client = MongoClient(uri)
    db = client[db_name]
    collection = db["documents"]
    
    try:
        print("Checking vector search indexes...")
        indexes = list(collection.list_search_indexes())
        
        if not indexes:
            print("❌ No search indexes found")
            print("   Run create_vector_index.py first")
            return
        
        print(f"\n📊 Found {len(indexes)} search index(es):\n")
        
        for idx in indexes:
            name = idx.get('name', 'Unknown')
            status = idx.get('status', 'Unknown')
            type_ = idx.get('type', 'Unknown')
            
            status_icon = "✅" if status == "READY" else "⏳" if status == "BUILDING" else "❌"
            
            print(f"{status_icon} Index: {name}")
            print(f"   Status: {status}")
            print(f"   Type: {type_}")
            
            if status == "READY":
                print(f"   🎉 Index is ready! Your API should be fast now.")
            elif status == "BUILDING":
                print(f"   ⏳ Index is still building. Wait 2-5 minutes.")
            else:
                print(f"   ⚠️  Unexpected status. Check Atlas console.")
            print()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"\n💡 Make sure:")
        print(f"   1. You're using MongoDB Atlas (not local)")
        print(f"   2. The index was created successfully")
    finally:
        client.close()

if __name__ == "__main__":
    check_vector_index_status()
