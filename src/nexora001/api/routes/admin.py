from fastapi import APIRouter, HTTPException, Depends
from typing import List
from nexora001.api.dependencies import get_current_active_superuser, get_storage
from nexora001.storage.mongodb import MongoDBStorage
from pydantic import BaseModel

router = APIRouter()

# --- Admin Models ---
class AdminUserList(BaseModel):
    id: str
    email: str
    name: str
    role: str
    status: str
    doc_count: int
    api_keys: int

class UserAction(BaseModel):
    email: str

# --- Endpoints ---

@router.get("/users", response_model=List[AdminUserList])
async def list_all_users(
    storage: MongoDBStorage = Depends(get_storage),
    admin: dict = Depends(get_current_active_superuser)
):
    """Super Admin: List all registered clients with statistics."""
    users = storage.get_all_users()
    
    # Format for response
    result = []
    for u in users:
        result.append(AdminUserList(
            id=str(u["_id"]),
            email=u["email"],
            name=u.get("name", ""),
            role=u.get("role", "client"),
            status=u.get("status", "active"),
            doc_count=u.get("doc_count", 0),
            api_keys=u.get("api_keys", 0)
        ))
    return result

@router.post("/ban")
async def ban_user(
    action: UserAction,
    storage: MongoDBStorage = Depends(get_storage),
    admin: dict = Depends(get_current_active_superuser)
):
    """Super Admin: Ban a client account."""
    if storage.set_user_status(action.email, "banned"):
        return {"message": f"User {action.email} has been BANNED"}
    raise HTTPException(status_code=404, detail="User not found")

@router.post("/unban")
async def unban_user(
    action: UserAction,
    storage: MongoDBStorage = Depends(get_storage),
    admin: dict = Depends(get_current_active_superuser)
):
    """Super Admin: Unban a client account."""
    if storage.set_user_status(action.email, "active"):
        return {"message": f"User {action.email} has been ACTIVATED"}
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/client")
async def delete_client(
    email: str,
    storage: MongoDBStorage = Depends(get_storage),
    admin: dict = Depends(get_current_active_superuser)
):
    """Super Admin: Permanently delete a client and ALL their data."""
    count = storage.delete_user_full(email)
    if count > 0:
        return {"message": f"Permanently deleted user and {count} related records"}
    raise HTTPException(status_code=404, detail="User not found")