import os
import secrets
import string
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from .db import get_db
from .models import User

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user

def require_role(required_role: str):
    """Decorator to require specific user role."""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role.value != required_role and current_user.role.value != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return role_checker

def generate_booking_reference() -> str:
    """Generate unique booking reference."""
    prefix = "SL"
    timestamp = datetime.now().strftime("%Y%m%d")
    random_chars = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    return f"{prefix}{timestamp}{random_chars}"

def generate_qr_code_data(booking_reference: str, appointment_id: int) -> str:
    """Generate QR code data for appointment."""
    return f"SL-GOV-{booking_reference}-{appointment_id}"

def validate_appointment_time(start_time: datetime, end_time: datetime, duration_minutes: int) -> bool:
    """Validate appointment time slot."""
    if start_time >= end_time:
        return False
    
    calculated_duration = (end_time - start_time).total_seconds() / 60
    if abs(calculated_duration - duration_minutes) > 5:  # Allow 5 minutes tolerance
        return False
    
    return True

def is_business_hours(time: datetime) -> bool:
    """Check if time is within business hours (8 AM to 5 PM)."""
    hour = time.hour
    return 8 <= hour < 17

def is_weekday(time: datetime) -> bool:
    """Check if time is on a weekday."""
    return time.weekday() < 5  # Monday = 0, Friday = 4

def format_phone_number(phone: str) -> str:
    """Format phone number to standard format."""
    # Remove all non-digit characters
    digits = ''.join(filter(str.isdigit, phone))
    
    # Handle Sri Lankan phone numbers
    if len(digits) == 10 and digits.startswith('0'):
        return f"+94{digits[1:]}"
    elif len(digits) == 9 and digits.startswith('7'):
        return f"+94{digits}"
    elif len(digits) == 12 and digits.startswith('94'):
        return f"+{digits}"
    
    return phone

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:250] + '.' + ext
    
    return filename

def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def is_allowed_file_type(filename: str, allowed_extensions: list) -> bool:
    """Check if file type is allowed."""
    ext = get_file_extension(filename)
    return ext.lower() in [ext.lower() for ext in allowed_extensions]

def calculate_file_size_mb(file_size_bytes: int) -> float:
    """Calculate file size in MB."""
    return round(file_size_bytes / (1024 * 1024), 2)

def generate_audit_log_data(action: str, table_name: str, record_id: int = None, 
                           old_values: dict = None, new_values: dict = None) -> dict:
    """Generate audit log data."""
    return {
        "action": action,
        "table_name": table_name,
        "record_id": record_id,
        "old_values": str(old_values) if old_values else None,
        "new_values": str(new_values) if new_values else None
    }

def paginate_query(query, page: int, size: int):
    """Apply pagination to SQLAlchemy query."""
    total = query.count()
    items = query.offset((page - 1) * size).limit(size).all()
    
    pages = (total + size - 1) // size
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "pages": pages
    }
