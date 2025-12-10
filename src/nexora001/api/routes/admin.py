"""
Super Admin endpoints for managing clients, users, and system settings.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from datetime import datetime
import uuid

from nexora001.api.models import (
    ClientInfo,
    ClientCreate,
    ClientListResponse,
    BanRequest,
    BanResponse,
    NotificationRequest,
    NotificationResponse,
    DeleteResponse
)
from nexora001.api.dependencies import get_storage
from nexora001.storage.mongodb import MongoDBStorage

router = APIRouter()

# Dummy data for demonstration purposes
DUMMY_CLIENTS = [
    {
        "id": "client-123",
        "name": "Test Client 1",
        "email": "client1@example.com",
        "api_key": "key-123",
        "is_active": True,
        "created_at": datetime.utcnow()
    },
    {
        "id": "client-456",
        "name": "Test Client 2",
        "email": "client2@example.com",
        "api_key": "key-456",
        "is_active": False,
        "created_at": datetime.utcnow()
    }
]

# ============================================================================
# CLIENT MANAGEMENT
# ============================================================================

@router.get(
    "/clients",
    response_model=ClientListResponse,
    summary="List all clients",
    description="Get a list of all clients in the system."
)
async def list_clients(storage: MongoDBStorage = Depends(get_storage)):
    """List all clients."""
    # In a real application, you would fetch this from the database
    return ClientListResponse(clients=DUMMY_CLIENTS, total=len(DUMMY_CLIENTS))


@router.post(
    "/clients",
    response_model=ClientInfo,
    summary="Create a new client",
    description="Create a new client and return its information."
)
async def create_client(
    client_data: ClientCreate,
    storage: MongoDBStorage = Depends(get_storage)
):
    """Create a new client."""
    new_client = ClientInfo(
        id=f"client-{uuid.uuid4().hex[:6]}",
        name=client_data.name,
        email=client_data.email,
        api_key=f"key-{uuid.uuid4().hex}",
        is_active=True,
        created_at=datetime.utcnow()
    )
    # In a real application, you would save this to the database
    DUMMY_CLIENTS.append(new_client.dict())
    return new_client


@router.delete(
    "/clients/{client_id}",
    response_model=DeleteResponse,
    summary="Delete a client",
    description="Delete a client by its ID."
)
async def delete_client(
    client_id: str,
    storage: MongoDBStorage = Depends(get_storage)
):
    """Delete a client."""
    global DUMMY_CLIENTS
    initial_len = len(DUMMY_CLIENTS)
    DUMMY_CLIENTS = [c for c in DUMMY_CLIENTS if c['id'] != client_id]
    
    if len(DUMMY_CLIENTS) < initial_len:
        return DeleteResponse(success=True, deleted_count=1, message=f"Client '{client_id}' deleted.")
    else:
        raise HTTPException(status_code=404, detail=f"Client '{client_id}' not found.")


# ============================================================================
# USER MANAGEMENT
# ============================================================================

@router.post(
    "/ban",
    response_model=BanResponse,
    summary="Ban a user",
    description="Ban a user by their user ID."
)
async def ban_user(
    ban_request: BanRequest,
    storage: MongoDBStorage = Depends(get_storage)
):
    """Ban a user."""
    # In a real application, you would implement the logic to ban a user
    print(f"Banning user '{ban_request.user_id}' for reason: {ban_request.reason}")
    return BanResponse(success=True, message=f"User '{ban_request.user_id}' has been banned.")


# ============================================================================
# NOTIFICATIONS
# ============================================================================

@router.post(
    "/notify",
    response_model=NotificationResponse,
    summary="Send a notification",
    description="Send a notification to all users or a subset of users."
)
async def send_notification(
    notification_request: NotificationRequest,
    storage: MongoDBStorage = Depends(get_storage)
):
    """Send a notification."""
    # In a real application, you would implement the logic to send notifications
    print(f"Sending notification: {notification_request.message}")
    return NotificationResponse(success=True, message="Notification sent successfully.")
