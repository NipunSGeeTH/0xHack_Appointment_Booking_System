from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from .models import UserRole, AppointmentStatus, NotificationType

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    national_id: str = Field(..., min_length=10, max_length=20)
    address: Optional[str] = None
   # role: UserRole = UserRole.CITIZEN

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserUpdate(BaseSchema):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = None

class UserResponse(UserBase):
    id: int
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserLogin(BaseSchema):
    username: str
    password: str

class UserLoginResponse(BaseSchema):
    access_token: str
    token_type: str
    user: UserResponse

# Department schemas
class DepartmentBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=200)
    contact_number: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    operating_hours: Optional[str] = Field(None, max_length=100)

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    is_active: Optional[bool] = None

class DepartmentResponse(DepartmentBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

# Service schemas
class ServiceBase(BaseSchema):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    department_id: int
    duration_minutes: int = Field(30, ge=15, le=480)  # 15 min to 8 hours
    max_daily_appointments: int = Field(50, ge=1, le=1000)
    required_documents: Optional[str] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseSchema):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    duration_minutes: Optional[int] = Field(None, ge=15, le=480)
    max_daily_appointments: Optional[int] = Field(None, ge=1, le=1000)
    required_documents: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceResponse(ServiceBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    department: DepartmentResponse

# TimeSlot schemas
class TimeSlotBase(BaseSchema):
    service_id: int
    start_time: datetime
    end_time: datetime
    max_capacity: int = Field(1, ge=1, le=10)

class TimeSlotCreate(TimeSlotBase):
    pass

class TimeSlotUpdate(BaseSchema):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    max_capacity: Optional[int] = Field(None, ge=1, le=10)
    is_available: Optional[bool] = None

class TimeSlotResponse(TimeSlotBase):
    id: int
    is_available: bool
    current_bookings: int
    created_at: datetime

class TimeSlotRecurringCreate(BaseSchema):
    service_id: int
    start_date: datetime
    end_date: datetime
    start_time: str  # HH:MM
    end_time: str    # HH:MM
    duration_minutes: int = Field(30, ge=15, le=480)
    max_capacity: int = Field(1, ge=1, le=10)
    weekdays: Optional[list[int]] = Field(default=None, description="0=Mon .. 6=Sun; None means weekdays only")

# Appointment schemas
class AppointmentBase(BaseSchema):
    service_id: int
    time_slot_id: int
    notes: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(BaseSchema):
    notes: Optional[str] = None
    status: Optional[AppointmentStatus] = None

class AppointmentResponse(BaseSchema):
    id: int
    user_id: int
    service_id: int
    time_slot_id: int
    status: AppointmentStatus
    booking_reference: str
    qr_code: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    service: ServiceResponse
    time_slot: TimeSlotResponse

# Document schemas
class DocumentBase(BaseSchema):
    document_type: str = Field(..., min_length=1, max_length=100)
    file_name: str = Field(..., min_length=1, max_length=255)

class DocumentCreate(DocumentBase):
    appointment_id: Optional[int] = None

class DocumentUpdate(BaseSchema):
    is_verified: Optional[bool] = None
    verification_notes: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: int
    user_id: int
    appointment_id: Optional[int] = None
    file_path: str
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    is_verified: bool
    verification_notes: Optional[str] = None
    uploaded_at: datetime
    verified_at: Optional[datetime] = None

# Government Officer schemas
class GovernmentOfficerBase(BaseSchema):
    department_id: int
    officer_id: str = Field(..., min_length=1, max_length=50)
    designation: str = Field(..., min_length=1, max_length=100)

class GovernmentOfficerCreate(GovernmentOfficerBase):
    user_id: int

class GovernmentOfficerUpdate(BaseSchema):
    designation: Optional[str] = Field(None, min_length=1, max_length=100)
    is_active: Optional[bool] = None

class GovernmentOfficerResponse(GovernmentOfficerBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    department: DepartmentResponse

# Notification schemas
class NotificationBase(BaseSchema):
    type: NotificationType
    title: str = Field(..., min_length=1, max_length=200)
    message: str

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationUpdate(BaseSchema):
    is_read: Optional[bool] = None

class NotificationResponse(NotificationBase):
    id: int
    user_id: int
    is_read: bool
    sent_via_email: bool
    sent_via_sms: bool
    created_at: datetime
    read_at: Optional[datetime] = None

# Feedback schemas
class FeedbackBase(BaseSchema):
    appointment_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackResponse(FeedbackBase):
    id: int
    user_id: int
    created_at: datetime

# Audit Log schemas
class AuditLogResponse(BaseSchema):
    id: int
    user_id: Optional[int] = None
    action: str
    table_name: str
    record_id: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    created_at: datetime

# Dashboard and Analytics schemas
class DashboardStats(BaseSchema):
    total_appointments: int
    pending_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    total_users: int
    total_services: int
    total_departments: int

class AppointmentAnalytics(BaseSchema):
    date: str
    total_bookings: int
    completed: int
    cancelled: int
    no_show: int

class ServiceAnalytics(BaseSchema):
    service_id: int
    service_name: str
    total_bookings: int
    average_rating: float
    completion_rate: float

# Search and Filter schemas
class AppointmentFilter(BaseSchema):
    status: Optional[AppointmentStatus] = None
    service_id: Optional[int] = None
    department_id: Optional[int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_id: Optional[int] = None

class ServiceFilter(BaseSchema):
    department_id: Optional[int] = None
    is_active: Optional[bool] = None
    search: Optional[str] = None

# Pagination schemas
class PaginationParams(BaseSchema):
    page: int = Field(1, ge=1)
    size: int = Field(10, ge=1, le=100)

class PaginatedResponse(BaseSchema):
    items: List[dict]
    total: int
    page: int
    size: int
    pages: int
