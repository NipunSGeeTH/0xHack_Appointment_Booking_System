from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

from ..models import Notification, User, Appointment, NotificationType
from ..schemas import NotificationCreate, NotificationUpdate, NotificationResponse

class NotificationService:
    def __init__(self, db: Session):
        self.db = db
        
        # Email configuration
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@gov.lk")
        
        # SMS configuration (placeholder for SMS service integration)
        self.sms_api_key = os.getenv("SMS_API_KEY", "")
        self.sms_api_url = os.getenv("SMS_API_URL", "")

    def create_notification(self, notification_data: NotificationCreate) -> Notification:
        """Create a new notification."""
        # Validate user exists
        user = self.db.query(User).filter(User.id == notification_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Create notification object
        db_notification = Notification(
            user_id=notification_data.user_id,
            type=notification_data.type,
            title=notification_data.title,
            message=notification_data.message
        )
        
        try:
            self.db.add(db_notification)
            self.db.commit()
            self.db.refresh(db_notification)
            
            # Send notifications based on type
            self._send_notifications(db_notification, user)
            
            return db_notification
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification creation failed"
            )

    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """Get notification by ID."""
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def get_user_notifications(self, user_id: int, unread_only: bool = False, 
                             limit: int = 100) -> List[Notification]:
        """Get notifications for a specific user."""
        query = self.db.query(Notification).filter(Notification.user_id == user_id)
        if unread_only:
            query = query.filter(Notification.is_read == False)
        return query.order_by(Notification.created_at.desc()).limit(limit).all()

    def mark_notification_as_read(self, notification_id: int, user_id: int) -> bool:
        """Mark a notification as read."""
        notification = self.get_notification_by_id(notification_id)
        if not notification or notification.user_id != user_id:
            return False
        
        notification.is_read = True
        notification.read_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def mark_all_notifications_as_read(self, user_id: int) -> bool:
        """Mark all notifications as read for a user."""
        try:
            self.db.query(Notification).filter(
                Notification.user_id == user_id,
                Notification.is_read == False
            ).update({
                "is_read": True,
                "read_at": datetime.utcnow()
            })
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def delete_notification(self, notification_id: int, user_id: int) -> bool:
        """Delete a notification."""
        notification = self.get_notification_by_id(notification_id)
        if not notification or notification.user_id != user_id:
            return False
        
        try:
            self.db.delete(notification)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def send_appointment_confirmation(self, appointment_id: int) -> bool:
        """Send appointment confirmation notification."""
        appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appointment:
            return False
        
        user = self.db.query(User).filter(User.id == appointment.user_id).first()
        if not user:
            return False
        
        notification_data = NotificationCreate(
            user_id=user.id,
            type=NotificationType.APPOINTMENT_CONFIRMATION,
            title="Appointment Confirmed",
            message=f"Your appointment for {appointment.service.name} has been confirmed. "
                   f"Booking Reference: {appointment.booking_reference}. "
                   f"Date: {appointment.time_slot.start_time.strftime('%Y-%m-%d %H:%M')}"
        )
        
        try:
            self.create_notification(notification_data)
            return True
        except Exception:
            return False

    def send_appointment_reminder(self, appointment_id: int) -> bool:
        """Send appointment reminder notification (24 hours before)."""
        appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appointment:
            return False
        
        user = self.db.query(User).filter(User.id == appointment.user_id).first()
        if not user:
            return False
        
        # Get required documents
        required_docs = self._get_required_documents_for_service(appointment.service_id)
        docs_list = ", ".join(required_docs) if required_docs else "None specified"
        
        notification_data = NotificationCreate(
            user_id=user.id,
            type=NotificationType.REMINDER,
            title="Appointment Reminder",
            message=f"Reminder: You have an appointment tomorrow for {appointment.service.name}. "
                   f"Time: {appointment.time_slot.start_time.strftime('%Y-%m-%d %H:%M')}. "
                   f"Please bring: {docs_list}"
        )
        
        try:
            self.create_notification(notification_data)
            return True
        except Exception:
            return False

    def send_status_update(self, appointment_id: int, status: str, notes: str = None) -> bool:
        """Send appointment status update notification."""
        appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appointment:
            return False
        
        user = self.db.query(User).filter(User.id == appointment.user_id).first()
        if not user:
            return False
        
        message = f"Your appointment status has been updated to: {status}"
        if notes:
            message += f". Notes: {notes}"
        
        notification_data = NotificationCreate(
            user_id=user.id,
            type=NotificationType.STATUS_UPDATE,
            title="Appointment Status Update",
            message=message
        )
        
        try:
            self.create_notification(notification_data)
            return True
        except Exception:
            return False

    def send_document_request(self, user_id: int, document_type: str, notes: str = None) -> bool:
        """Send document request notification."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        message = f"Please upload your {document_type} document"
        if notes:
            message += f". {notes}"
        
        notification_data = NotificationCreate(
            user_id=user.id,
            type=NotificationType.DOCUMENT_REQUEST,
            title="Document Required",
            message=message
        )
        
        try:
            self.create_notification(notification_data)
            return True
        except Exception:
            return False

    def schedule_appointment_reminders(self) -> int:
        """Schedule reminders for appointments happening tomorrow."""
        tomorrow = datetime.now() + timedelta(days=1)
        start_of_day = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        # Get appointments for tomorrow
        appointments = self.db.query(Appointment).join(TimeSlot).filter(
            TimeSlot.start_time >= start_of_day,
            TimeSlot.start_time < end_of_day,
            Appointment.status.in_(['pending', 'confirmed'])
        ).all()
        
        reminder_count = 0
        for appointment in appointments:
            if self.send_appointment_reminder(appointment.id):
                reminder_count += 1
        
        return reminder_count

    def get_notification_statistics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get notification statistics."""
        query = self.db.query(Notification)
        if user_id:
            query = query.filter(Notification.user_id == user_id)
        
        total_notifications = query.count()
        unread_notifications = query.filter(Notification.is_read == False).count()
        read_notifications = query.filter(Notification.is_read == True).count()
        
        # Get type distribution
        type_distribution = {}
        for notification_type in NotificationType:
            count = query.filter(Notification.type == notification_type).count()
            type_distribution[notification_type.value] = count
        
        return {
            "total_notifications": total_notifications,
            "unread_notifications": unread_notifications,
            "read_notifications": read_notifications,
            "type_distribution": type_distribution
        }

    def _send_notifications(self, notification: Notification, user: User):
        """Send notifications via email and/or SMS."""
        try:
            # Send email notification
            if user.email:
                self._send_email_notification(notification, user)
                notification.sent_via_email = True
            
            # Send SMS notification (placeholder)
            if user.phone_number:
                # self._send_sms_notification(notification, user)
                notification.sent_via_sms = True
            
            self.db.commit()
        except Exception as e:
            # Log error but don't fail the notification creation
            print(f"Failed to send notification: {str(e)}")

    def _send_email_notification(self, notification: Notification, user: User):
        """Send email notification."""
        if not self.smtp_username or not self.smtp_password:
            return  # Email not configured
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = user.email
            msg['Subject'] = notification.title
            
            body = f"""
            Dear {user.first_name} {user.last_name},
            
            {notification.message}
            
            Best regards,
            Sri Lankan Government Services Portal
            
            ---
            This is an automated message. Please do not reply.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
            server.quit()
            
        except Exception as e:
            print(f"Failed to send email: {str(e)}")

    def _send_sms_notification(self, notification: Notification, user: User):
        """Send SMS notification (placeholder for SMS service integration)."""
        # This would integrate with an SMS service provider
        # For now, just log the attempt
        print(f"SMS notification would be sent to {user.phone_number}: {notification.message}")

    def _get_required_documents_for_service(self, service_id: int) -> List[str]:
        """Get required documents for a service."""
        # This would typically come from the service configuration
        # For now, return common document types
        return [
            "National ID",
            "Passport (if applicable)",
            "Relevant certificates"
        ]

    def cleanup_old_notifications(self, days_old: int = 90) -> int:
        """Clean up old notifications."""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        try:
            deleted_count = self.db.query(Notification).filter(
                Notification.created_at < cutoff_date,
                Notification.is_read == True
            ).delete()
            self.db.commit()
            return deleted_count
        except IntegrityError:
            self.db.rollback()
            return 0

    def get_notifications_by_type(self, user_id: int, notification_type: NotificationType) -> List[Notification]:
        """Get notifications of a specific type for a user."""
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.type == notification_type
        ).order_by(Notification.created_at.desc()).all()

    def get_unread_notification_count(self, user_id: int) -> int:
        """Get count of unread notifications for a user."""
        return self.db.query(Notification).filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        ).count()
