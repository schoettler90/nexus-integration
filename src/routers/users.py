from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

from src.models import User, UserPublic
from src.routers.deps import get_db
from src.security import hash_password, is_bcrypt_hash, verify_password

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    """Create a new user (the password is stored as a bcrypt hash)."""
    try:
        user.password = hash_password(user.password)
        user_id = get_db().create_user(user)
        return {"message": "User created successfully", "id": user_id}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login", response_model=dict)
async def login(login_request: LoginRequest):
    """Authenticate a user."""
    user = get_db().get_user_by_email(login_request.email)
    if not user or not verify_password(login_request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
        )

    return {"message": "Login successful", "user_id": user.id, "name": user.name}


@router.get("/users/{user_id}", response_model=UserPublic)
async def get_user(user_id: str):
    """Get a user by ID."""
    user = get_db().get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.put("/users/{user_id}", response_model=dict)
async def update_user(user_id: str, user: User):
    """Update an existing user; a new plaintext password is hashed before storage."""
    if not is_bcrypt_hash(user.password):
        user.password = hash_password(user.password)
    success = get_db().update_user(user_id, user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or no changes made",
        )
    return {"message": "User updated successfully"}


@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    """Delete a user by ID."""
    success = get_db().delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"message": "User deleted successfully"}


@router.get("/users", response_model=List[UserPublic])
async def list_users():
    """Get all users."""
    try:
        return get_db().list_users()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
