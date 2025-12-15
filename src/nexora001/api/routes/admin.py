from fastapi import APIRouter, HTTPException, Depends
from typing import List
from nexora001.api.dependencies import get_current_active_superuser, get_storage
from nexora001.storage.mongodb import MongoDBStorage
from pydantic import BaseModel
import secrets
from nexora001.api.security import get_password_hash

router = APIRouter()

# --- Admin Models ---

class AdminCreateUser(BaseModel):
    email: str
    name: str

class AdminNotification(BaseModel):
    email: str # Send to specific user by email
    message: str
    type: str = "info"

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

@router.post("/client", response_model=dict)
async def create_client_manually(
    user_in: AdminCreateUser,
    storage: MongoDBStorage = Depends(get_storage),
    admin: dict = Depends(get_current_active_superuser)
):
    """Super Admin: Create a client manually and generate a temp password."""
    if storage.users.find_one({"email": user_in.email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Generate random 12-char password
    temp_password = secrets.token_urlsafe(12)
    hashed_pw = get_password_hash(temp_password) # Make sure get_password_hash is imported from security
    
    user_id = storage.create_user(user_in.email, hashed_pw, user_in.name)
    
    # Return the password so Admin can copy it
    return {
        "message": "User created",
        "user_id": user_id,
        "email": user_in.email,
        "temporary_password": temp_password 
    }

@router.post("/notify")
async def send_notification(
    note: AdminNotification,
    storage: MongoDBStorage = Depends(get_storage),
    admin: dict = Depends(get_current_active_superuser)
):
    """Super Admin: Send an internal message to a client."""
    target_user = storage.users.find_one({"email": note.email})
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    storage.create_notification(str(target_user["_id"]), note.message, note.type)
    return {"message": "Notification sent"}