from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from nexora001.api.security import create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from nexora001.api.dependencies import get_storage
from nexora001.storage.mongodb import MongoDBStorage

router = APIRouter()

@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    storage: MongoDBStorage = Depends(get_storage)
):
    """
    OAuth2 compatible token login. 
    Use this to get a 'Bearer' token for all other endpoints.
    """
    # 1. Find User
    # Note: Using your existing password hashing method (SHA256)
    user = storage.users.find_one({"email": form_data.username})
    
    # 2. Verify Password
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # 3. Check Status
    if user.get("status") == "banned":
        raise HTTPException(status_code=400, detail="Account is banned")

    # 4. Generate Token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user.get("role", "client")},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "role": user.get("role", "client"),
        "name": user.get("name")
    }