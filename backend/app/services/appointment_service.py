from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json

from ..models import (
    Appointment, Service, TimeSlot, User, Department, 
    AppointmentStatus, Document
)
from ..schemas import (
    AppointmentCreate, AppointmentUpdate, AppointmentResponse,
    TimeSlotCreate, TimeSlotUpdate, AppointmentFilter
)
from ..utils import (
    generate_booking_reference, generate_qr_code_data,
    validate_appointment_time, is_business_hours, is_weekday,
    paginate_query
)

class AppointmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_appointment(self, user_id: int, appointment_data: AppointmentCreate) -> Appointment:
        """Create a new appointment."""
        # Validate service exists and is active
        service = self.db.query(Service).filter(
            Service.id == appointment_data.service_id,
            Service.is_active == True
        ).first()
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found or inactive"
            )
        
        # Validate time slot exists and is available
        time_slot = self.db.query(TimeSlot).filter(
            TimeSlot.id == appointment_data.time_slot_id,
            TimeSlot.service_id == appointment_data.service_id,
            TimeSlot.is_available == True
        ).first()
        if not time_slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Time slot not found or unavailable"
            )
        
        # Check if time slot has capacity
        if time_slot.current_bookings >= time_slot.max_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time slot is fully booked"
            )
        
        # Check if user already has an appointment at this time
        existing_appointment = self.db.query(Appointment).filter(
            Appointment.user_id == user_id,
            Appointment.time_slot_id == appointment_data.time_slot_id,
            Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])
        ).first()
        if existing_appointment:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already have an appointment at this time"
            )
        
        # Generate unique booking reference
        booking_reference = generate_booking_reference()
        
        # Create appointment
        db_appointment = Appointment(
            user_id=user_id,
            service_id=appointment_data.service_id,
            time_slot_id=appointment_data.time_slot_id,
            status=AppointmentStatus.PENDING,
            booking_reference=booking_reference,
            notes=appointment_data.notes
        )
        
        try:
            self.db.add(db_appointment)
            self.db.commit()
            self.db.refresh(db_appointment)
            
            # Update time slot booking count
            time_slot.current_bookings += 1
            if time_slot.current_bookings >= time_slot.max_capacity:
                time_slot.is_available = False
            self.db.commit()
            
            # Generate QR code data
            qr_data = generate_qr_code_data(booking_reference, db_appointment.id)
            db_appointment.qr_code = qr_data
            self.db.commit()
            
            return db_appointment
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Appointment creation failed"
            )

    def get_appointment_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Get appointment by ID."""
        return self.db.query(Appointment).filter(Appointment.id == appointment_id).first()

    def get_user_appointments(self, user_id: int, status: Optional[AppointmentStatus] = None) -> List[Appointment]:
        """Get appointments for a specific user."""
        query = self.db.query(Appointment).filter(Appointment.user_id == user_id)
        if status:
            query = query.filter(Appointment.status == status)
        return query.order_by(Appointment.created_at.desc()).all()

    def get_appointments_by_service(self, service_id: int, status: Optional[AppointmentStatus] = None) -> List[Appointment]:
        """Get appointments for a specific service."""
        query = self.db.query(Appointment).filter(Appointment.service_id == service_id)
        if status:
            query = query.filter(Appointment.status == status)
        return query.order_by(Appointment.created_at.desc()).all()

    def get_appointments_by_department(self, department_id: int, status: Optional[AppointmentStatus] = None) -> List[Appointment]:
        """Get appointments for a specific department."""
        query = self.db.query(Appointment).join(Service).filter(Service.department_id == department_id)
        if status:
            query = query.filter(Appointment.status == status)
        return query.order_by(Appointment.created_at.desc()).all()

    def update_appointment_status(self, appointment_id: int, new_status: AppointmentStatus, notes: Optional[str] = None) -> Optional[Appointment]:
        """Update appointment status."""
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return None
        
        old_status = appointment.status
        appointment.status = new_status
        if notes:
            appointment.notes = notes
        appointment.updated_at = datetime.utcnow()
        
        # Handle status-specific logic
        if new_status == AppointmentStatus.CANCELLED or new_status == AppointmentStatus.NO_SHOW:
            # Free up time slot
            time_slot = self.db.query(TimeSlot).filter(TimeSlot.id == appointment.time_slot_id).first()
            if time_slot:
                time_slot.current_bookings = max(0, time_slot.current_bookings - 1)
                if time_slot.current_bookings < time_slot.max_capacity:
                    time_slot.is_available = True
        
        try:
            self.db.commit()
            self.db.refresh(appointment)
            return appointment
        except IntegrityError:
            self.db.rollback()
            return None

    def cancel_appointment(self, appointment_id: int, user_id: int) -> bool:
        """Cancel an appointment (only by the user who booked it)."""
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return False
        
        if appointment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only cancel your own appointments"
            )
        
        if appointment.status not in [AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot cancel appointment in current status"
            )
        
        return self.update_appointment_status(appointment_id, AppointmentStatus.CANCELLED) is not None

    def reschedule_appointment(self, appointment_id: int, new_time_slot_id: int, user_id: int) -> Optional[Appointment]:
        """Reschedule an appointment to a new time slot."""
        appointment = self.get_appointment_by_id(appointment_id)
        if not appointment:
            return None
        
        if appointment.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only reschedule your own appointments"
            )
        
        if appointment.status not in [AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot reschedule appointment in current status"
            )
        
        # Validate new time slot
        new_time_slot = self.db.query(TimeSlot).filter(
            TimeSlot.id == new_time_slot_id,
            TimeSlot.service_id == appointment.service_id,
            TimeSlot.is_available == True
        ).first()
        if not new_time_slot:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="New time slot not found or unavailable"
            )
        
        if new_time_slot.current_bookings >= new_time_slot.max_capacity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New time slot is fully booked"
            )
        
        # Free up old time slot
        old_time_slot = self.db.query(TimeSlot).filter(TimeSlot.id == appointment.time_slot_id).first()
        if old_time_slot:
            old_time_slot.current_bookings = max(0, old_time_slot.current_bookings - 1)
            if old_time_slot.current_bookings < old_time_slot.max_capacity:
                old_time_slot.is_available = True
        
        # Update appointment
        appointment.time_slot_id = new_time_slot_id
        appointment.status = AppointmentStatus.PENDING
        appointment.updated_at = datetime.utcnow()
        
        # Update new time slot
        new_time_slot.current_bookings += 1
        if new_time_slot.current_bookings >= new_time_slot.max_capacity:
            new_time_slot.is_available = False
        
        try:
            self.db.commit()
            self.db.refresh(appointment)
            return appointment
        except IntegrityError:
            self.db.rollback()
            return None

    def get_available_time_slots(self, service_id: int, date: datetime) -> List[TimeSlot]:
        """Get available time slots for a service on a specific date."""
        start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        return self.db.query(TimeSlot).filter(
            TimeSlot.service_id == service_id,
            TimeSlot.start_time >= start_of_day,
            TimeSlot.start_time < end_of_day,
            TimeSlot.is_available == True
        ).order_by(TimeSlot.start_time).all()

    def create_time_slots(self, service_id: int, start_date: datetime, end_date: datetime, 
                         start_time: str, end_time: str, duration_minutes: int) -> List[TimeSlot]:
        """Create time slots for a service over a date range."""
        time_slots = []
        current_date = start_date
        
        while current_date <= end_date:
            if is_weekday(current_date):
                # Parse start and end times
                start_hour, start_minute = map(int, start_time.split(':'))
                end_hour, end_minute = map(int, end_time.split(':'))
                
                current_time = current_date.replace(hour=start_hour, minute=start_minute)
                end_datetime = current_date.replace(hour=end_hour, minute=end_minute)
                
                while current_time < end_datetime:
                    slot_end = current_time + timedelta(minutes=duration_minutes)
                    if slot_end <= end_datetime:
                        time_slot = TimeSlot(
                            service_id=service_id,
                            start_time=current_time,
                            end_time=slot_end,
                            max_capacity=1
                        )
                        time_slots.append(time_slot)
                    current_time = slot_end
            
            current_date += timedelta(days=1)
        
        try:
            self.db.add_all(time_slots)
            self.db.commit()
            return time_slots
        except IntegrityError:
            self.db.rollback()
            return []

    def get_appointment_statistics(self, department_id: Optional[int] = None, 
                                 service_id: Optional[int] = None) -> Dict[str, Any]:
        """Get appointment statistics for dashboard."""
        query = self.db.query(Appointment)
        
        if department_id:
            query = query.join(Service).filter(Service.department_id == department_id)
        if service_id:
            query = query.filter(Appointment.service_id == service_id)
        
        total_appointments = query.count()
        pending_appointments = query.filter(Appointment.status == AppointmentStatus.PENDING).count()
        confirmed_appointments = query.filter(Appointment.status == AppointmentStatus.CONFIRMED).count()
        completed_appointments = query.filter(Appointment.status == AppointmentStatus.COMPLETED).count()
        cancelled_appointments = query.filter(Appointment.status == AppointmentStatus.CANCELLED).count()
        no_show_appointments = query.filter(Appointment.status == AppointmentStatus.NO_SHOW).count()
        
        return {
            "total_appointments": total_appointments,
            "pending_appointments": pending_appointments,
            "confirmed_appointments": confirmed_appointments,
            "completed_appointments": completed_appointments,
            "cancelled_appointments": cancelled_appointments,
            "no_show_appointments": no_show_appointments
        }

    def search_appointments(self, filters: AppointmentFilter, page: int = 1, size: int = 10) -> Dict[str, Any]:
        """Search appointments with filters and pagination."""
        query = self.db.query(Appointment).join(Service).join(TimeSlot)
        
        if filters.status:
            query = query.filter(Appointment.status == filters.status)
        if filters.service_id:
            query = query.filter(Appointment.service_id == filters.service_id)
        if filters.department_id:
            query = query.filter(Service.department_id == filters.department_id)
        if filters.start_date:
            query = query.filter(TimeSlot.start_time >= filters.start_date)
        if filters.end_date:
            query = query.filter(TimeSlot.start_time <= filters.end_date)
        if filters.user_id:
            query = query.filter(Appointment.user_id == filters.user_id)
        
        query = query.order_by(Appointment.created_at.desc())
        
        return paginate_query(query, page, size)

    def get_appointment_by_reference(self, booking_reference: str) -> Optional[Appointment]:
        """Get appointment by booking reference."""
        return self.db.query(Appointment).filter(
            Appointment.booking_reference == booking_reference
        ).first()
