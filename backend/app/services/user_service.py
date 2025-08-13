from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List
from datetime import datetime, timedelta  # Add timedelta here

from ..models import User, UserRole
from ..schemas import UserCreate, UserUpdate, UserResponse
from ..utils import get_password_hash, verify_password, create_access_token, format_phone_number

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user."""
        # Check if username already exists
        if self.db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        
        # Check if email already exists
        if self.db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Check if national ID already exists
        if self.db.query(User).filter(User.national_id == user_data.national_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="National ID already registered"
            )
        
        # Format phone number if provided
        phone_number = None
        if user_data.phone_number:
            phone_number = format_phone_number(user_data.phone_number)
        
        # Create user object
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            phone_number=phone_number,
            national_id=user_data.national_id,
            address=user_data.address,
            role=user_data.role
        )
        
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed"
            )

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password."""
        user = self.db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def create_user_token(self, user: User) -> dict:
        """Create access token for user."""
        access_token_expires_delta = timedelta(minutes=30)  # This is a timedelta object
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires_delta
        )
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_national_id(self, national_id: str) -> Optional[User]:
        """Get user by national ID."""
        return self.db.query(User).filter(User.national_id == national_id).first()

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Update user information."""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # Update fields if provided
        if user_data.first_name is not None:
            user.first_name = user_data.first_name
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
        if user_data.phone_number is not None:
            user.phone_number = format_phone_number(user_data.phone_number)
        if user_data.address is not None:
            user.address = user_data.address
        
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User update failed"
            )

    def deactivate_user(self, user_id: int) -> bool:
        """Deactivate a user."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def activate_user(self, user_id: int) -> bool:
        """Activate a user."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def change_user_role(self, user_id: int, new_role: UserRole) -> bool:
        """Change user role."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.role = new_role
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def get_users_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role with pagination."""
        return self.db.query(User).filter(
            User.role == role,
            User.is_active == True
        ).offset(skip).limit(limit).all()

    def search_users(self, search_term: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Search users by name, username, email, or national ID."""
        search_filter = f"%{search_term}%"
        return self.db.query(User).filter(
            (User.first_name.ilike(search_filter)) |
            (User.last_name.ilike(search_filter)) |
            (User.username.ilike(search_filter)) |
            (User.email.ilike(search_filter)) |
            (User.national_id.ilike(search_filter))
        ).offset(skip).limit(limit).all()

    def get_user_statistics(self) -> dict:
        """Get user statistics for dashboard."""
        total_users = self.db.query(User).count()
        active_users = self.db.query(User).filter(User.is_active == True).count()
        citizens = self.db.query(User).filter(User.role == UserRole.CITIZEN).count()
        officers = self.db.query(User).filter(User.role == UserRole.GOVERNMENT_OFFICER).count()
        admins = self.db.query(User).filter(User.role == UserRole.ADMIN).count()
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "citizens": citizens,
            "officers": officers,
            "admins": admins
        }

    def reset_password(self, user_id: int, new_password: str) -> bool:
        """Reset user password."""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.hashed_password = get_password_hash(new_password)
        user.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def verify_national_id(self, national_id: str) -> bool:
        """Verify if national ID format is valid (Sri Lankan format)."""
        # Basic validation for Sri Lankan National ID
        if not national_id or len(national_id) != 10:
            return False
        
        # Check if it's numeric
        if not national_id.isdigit():
            return False
        
        # Check if it starts with valid year (19xx or 20xx)
        year = int(national_id[:4])
        if year < 1900 or year > 2025:
            return False
        
        return True
