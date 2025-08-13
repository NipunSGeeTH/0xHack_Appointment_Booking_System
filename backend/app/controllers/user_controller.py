from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from ..models import User
from ..schemas import (
    UserCreate, UserUpdate, UserResponse, UserLogin, UserLoginResponse
)
from ..services.user_service import UserService
from ..utils import get_current_active_user, require_role
from app.models import UserRole

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Register a new user."""
    user_service = UserService(db)
    return user_service.create_user(user_data)

@router.post("/login", response_model=UserLoginResponse)
async def login_user(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """Login user and return access token."""
    user_service = UserService(db)
    
    user = user_service.authenticate_user(
        user_credentials.username, 
        user_credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    token_data = user_service.create_user_token(user)
    
    return UserLoginResponse(
        access_token=token_data["access_token"],
        token_type=token_data["token_type"],
        user=user
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information."""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user information."""
    user_service = UserService(db)
    updated_user = user_service.update_user(current_user.id, user_data)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return updated_user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user by ID (admin only or own profile)."""
    if current_user.id != user_id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get all users (admin only)."""
    user_service = UserService(db)
    users = user_service.get_users_by_role(UserRole.CITIZEN, skip, limit)
    return users

@router.get("/officers", response_model=List[UserResponse])
async def get_government_officers(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get all government officers (admin only)."""
    user_service = UserService(db)
    officers = user_service.get_users_by_role(UserRole.GOVERNMENT_OFFICER, skip, limit)
    return officers

@router.put("/{user_id}/activate")
async def activate_user(
    user_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Activate a user account (admin only)."""
    user_service = UserService(db)
    success = user_service.activate_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User activated successfully"}

@router.put("/{user_id}/deactivate")
async def deactivate_user(
    user_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Deactivate a user account (admin only)."""
    user_service = UserService(db)
    success = user_service.deactivate_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deactivated successfully"}

@router.put("/{user_id}/role")
async def change_user_role(
    user_id: int,
    new_role: str,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Change user role (admin only)."""
    user_service = UserService(db)
    success = user_service.change_user_role(user_id, new_role)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": f"User role changed to {new_role}"}

@router.get("/search/{search_term}", response_model=List[UserResponse])
async def search_users(
    search_term: str,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Search users by name, username, email, or national ID (admin only)."""
    user_service = UserService(db)
    users = user_service.search_users(search_term, skip, limit)
    return users

@router.get("/statistics/dashboard")
async def get_user_statistics(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get user statistics for dashboard (admin only)."""
    user_service = UserService(db)
    return user_service.get_user_statistics()

@router.post("/{user_id}/reset-password")
async def reset_user_password(
    user_id: int,
    new_password: str,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Reset user password (admin only)."""
    user_service = UserService(db)
    success = user_service.reset_password(user_id, new_password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "Password reset successfully"}

@router.post("/validate-national-id")
async def validate_national_id(
    national_id: str,
    db: Session = Depends(get_db)
):
    """Validate Sri Lankan National ID format."""
    user_service = UserService(db)
    is_valid = user_service.verify_national_id(national_id)
    
    return {
        "national_id": national_id,
        "is_valid": is_valid
    }
