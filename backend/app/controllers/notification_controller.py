from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import User, NotificationType
from ..schemas import (
    NotificationCreate, NotificationUpdate, NotificationResponse
)
from ..services.notification_service import NotificationService
from ..utils import get_current_active_user, require_role

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.post("/", response_model=NotificationResponse, status_code=status.HTTP_201_CREATED)
async def create_notification(
    notification_data: NotificationCreate,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Create a new notification (government officers only)."""
    notification_service = NotificationService(db)
    return notification_service.create_notification(notification_data)

@router.get("/me", response_model=List[NotificationResponse])
async def get_my_notifications(
    unread_only: bool = Query(False, description="Filter unread notifications only"),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's notifications."""
    notification_service = NotificationService(db)
    return notification_service.get_user_notifications(current_user.id, unread_only, limit)

@router.get("/{notification_id}", response_model=NotificationResponse)
async def get_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get notification by ID."""
    notification_service = NotificationService(db)
    notification = notification_service.get_notification_by_id(notification_id)
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    # Check if user can access this notification
    if notification.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return notification

@router.put("/{notification_id}/read")
async def mark_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read."""
    notification_service = NotificationService(db)
    success = notification_service.mark_notification_as_read(notification_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return {"message": "Notification marked as read"}

@router.put("/me/read-all")
async def mark_all_notifications_as_read(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark all notifications as read for the current user."""
    notification_service = NotificationService(db)
    success = notification_service.mark_all_notifications_as_read(current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to mark notifications as read"
        )
    
    return {"message": "All notifications marked as read"}

@router.delete("/{notification_id}")
async def delete_notification(
    notification_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a notification."""
    notification_service = NotificationService(db)
    success = notification_service.delete_notification(notification_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    return {"message": "Notification deleted successfully"}

# Government Officer and Admin endpoints
@router.post("/appointment/{appointment_id}/confirmation")
async def send_appointment_confirmation(
    appointment_id: int,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Send appointment confirmation notification (government officers only)."""
    notification_service = NotificationService(db)
    success = notification_service.send_appointment_confirmation(appointment_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to send appointment confirmation"
        )
    
    return {"message": "Appointment confirmation sent successfully"}

@router.post("/appointment/{appointment_id}/reminder")
async def send_appointment_reminder(
    appointment_id: int,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Send appointment reminder notification (government officers only)."""
    notification_service = NotificationService(db)
    success = notification_service.send_appointment_reminder(appointment_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to send appointment reminder"
        )
    
    return {"message": "Appointment reminder sent successfully"}

@router.post("/appointment/{appointment_id}/status-update")
async def send_status_update(
    appointment_id: int,
    status: str,
    notes: Optional[str] = None,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Send appointment status update notification (government officers only)."""
    notification_service = NotificationService(db)
    success = notification_service.send_status_update(appointment_id, status, notes)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to send status update"
        )
    
    return {"message": "Status update sent successfully"}

@router.post("/user/{user_id}/document-request")
async def send_document_request(
    user_id: int,
    document_type: str,
    notes: Optional[str] = None,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Send document request notification (government officers only)."""
    notification_service = NotificationService(db)
    success = notification_service.send_document_request(user_id, document_type, notes)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to send document request"
        )
    
    return {"message": "Document request sent successfully"}

@router.post("/schedule-reminders")
async def schedule_appointment_reminders(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Schedule reminders for appointments happening tomorrow (admin only)."""
    notification_service = NotificationService(db)
    reminder_count = notification_service.schedule_appointment_reminders()
    
    return {
        "message": f"Successfully scheduled {reminder_count} appointment reminders",
        "reminders_sent": reminder_count
    }

@router.get("/statistics/overview")
async def get_notification_statistics(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get notification statistics (government officers only)."""
    notification_service = NotificationService(db)
    return notification_service.get_notification_statistics(user_id)

@router.get("/type/{notification_type}", response_model=List[NotificationResponse])
async def get_notifications_by_type(
    notification_type: NotificationType,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get notifications of a specific type for the current user."""
    notification_service = NotificationService(db)
    return notification_service.get_notifications_by_type(current_user.id, notification_type)

@router.get("/unread/count")
async def get_unread_notification_count(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications for the current user."""
    notification_service = NotificationService(db)
    count = notification_service.get_unread_notification_count(current_user.id)
    
    return {"unread_count": count}

@router.delete("/cleanup/old")
async def cleanup_old_notifications(
    days_old: int = Query(90, ge=30, le=365, description="Delete notifications older than X days"),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Clean up old notifications (admin only)."""
    notification_service = NotificationService(db)
    deleted_count = notification_service.cleanup_old_notifications(days_old)
    
    return {
        "message": f"Successfully deleted {deleted_count} old notifications",
        "deleted_count": deleted_count
    }
