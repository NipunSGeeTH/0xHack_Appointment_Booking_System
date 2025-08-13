from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from ..db import get_db
from ..models import User, AppointmentStatus
from ..schemas import (
    AppointmentCreate, AppointmentUpdate, AppointmentResponse,
    TimeSlotCreate, TimeSlotUpdate, AppointmentFilter, TimeSlotRecurringCreate
)
from ..services.appointment_service import AppointmentService
from ..utils import get_current_active_user, require_role

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment_data: AppointmentCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new appointment."""
    appointment_service = AppointmentService(db)
    return appointment_service.create_appointment(current_user.id, appointment_data)

@router.get("/me", response_model=List[AppointmentResponse])
async def get_my_appointments(
    status: Optional[AppointmentStatus] = Query(None, description="Filter by appointment status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's appointments."""
    appointment_service = AppointmentService(db)
    return appointment_service.get_user_appointments(current_user.id, status)

@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get appointment by ID."""
    appointment_service = AppointmentService(db)
    appointment = appointment_service.get_appointment_by_id(appointment_id)
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user can access this appointment
    if appointment.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return appointment

@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update appointment (admin or government officer only)."""
    appointment_service = AppointmentService(db)
    appointment = appointment_service.get_appointment_by_id(appointment_id)
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Only admins, government officers, or the appointment owner can update
    if (appointment.user_id != current_user.id and 
        current_user.role.value not in ["admin", "government_officer"]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Update appointment status
    if appointment_data.status:
        updated_appointment = appointment_service.update_appointment_status(
            appointment_id, appointment_data.status, appointment_data.notes
        )
    else:
        # Update other fields
        updated_appointment = appointment_service.update_appointment_status(
            appointment_id, appointment.status, appointment_data.notes
        )
    
    if not updated_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update appointment"
        )
    
    return updated_appointment

@router.delete("/{appointment_id}")
async def cancel_appointment(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Cancel an appointment."""
    appointment_service = AppointmentService(db)
    success = appointment_service.cancel_appointment(appointment_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to cancel appointment"
        )
    
    return {"message": "Appointment cancelled successfully"}

@router.put("/{appointment_id}/reschedule")
async def reschedule_appointment(
    appointment_id: int,
    new_time_slot_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Reschedule an appointment to a new time slot."""
    appointment_service = AppointmentService(db)
    updated_appointment = appointment_service.reschedule_appointment(
        appointment_id, new_time_slot_id, current_user.id
    )
    
    if not updated_appointment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to reschedule appointment"
        )
    
    return {"message": "Appointment rescheduled successfully"}

@router.get("/{appointment_id}/qr-code")
async def get_appointment_qr_code(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get QR code data for an appointment."""
    appointment_service = AppointmentService(db)
    appointment = appointment_service.get_appointment_by_id(appointment_id)
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    if appointment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return {
        "appointment_id": appointment_id,
        "qr_code_data": appointment.qr_code,
        "booking_reference": appointment.booking_reference
    }

@router.get("/reference/{booking_reference}", response_model=AppointmentResponse)
async def get_appointment_by_reference(
    booking_reference: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get appointment by booking reference."""
    appointment_service = AppointmentService(db)
    appointment = appointment_service.get_appointment_by_reference(booking_reference)
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    # Check if user can access this appointment
    if appointment.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return appointment

# Government Officer and Admin endpoints
@router.get("/service/{service_id}", response_model=List[AppointmentResponse])
async def get_appointments_by_service(
    service_id: int,
    status: Optional[AppointmentStatus] = Query(None, description="Filter by appointment status"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get appointments for a specific service (government officers only)."""
    appointment_service = AppointmentService(db)
    return appointment_service.get_appointments_by_service(service_id, status)

@router.get("/department/{department_id}", response_model=List[AppointmentResponse])
async def get_appointments_by_department(
    department_id: int,
    status: Optional[AppointmentStatus] = Query(None, description="Filter by appointment status"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get appointments for a specific department (government officers only)."""
    appointment_service = AppointmentService(db)
    return appointment_service.get_appointments_by_department(department_id, status)

@router.put("/{appointment_id}/status")
async def update_appointment_status(
    appointment_id: int,
    new_status: AppointmentStatus,
    notes: Optional[str] = None,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Update appointment status (government officers only)."""
    appointment_service = AppointmentService(db)
    updated_appointment = appointment_service.update_appointment_status(
        appointment_id, new_status, notes
    )
    
    if not updated_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    
    return {"message": f"Appointment status updated to {new_status.value}"}

@router.get("/analytics/statistics")
async def get_appointment_statistics(
    department_id: Optional[int] = Query(None, description="Filter by department ID"),
    service_id: Optional[int] = Query(None, description="Filter by service ID"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get appointment statistics (government officers only)."""
    appointment_service = AppointmentService(db)
    return appointment_service.get_appointment_statistics(department_id, service_id)

@router.post("/search")
async def search_appointments(
    filters: AppointmentFilter,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Search appointments with filters (government officers only)."""
    appointment_service = AppointmentService(db)
    return appointment_service.search_appointments(filters, page, size)

# Time Slot Management (Admin only)
@router.post("/time-slots", response_model=List[dict])
async def create_time_slots(
    service_id: int,
    start_date: datetime,
    end_date: datetime,
    start_time: str = Query(..., description="Start time in HH:MM format"),
    end_time: str = Query(..., description="End time in HH:MM format"),
    duration_minutes: int = Query(30, ge=15, le=480),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Create time slots for a service (admin only)."""
    appointment_service = AppointmentService(db)
    time_slots = appointment_service.create_time_slots(
        service_id, start_date, end_date, start_time, end_time, duration_minutes
    )
    
    return [{"id": slot.id, "start_time": slot.start_time, "end_time": slot.end_time} for slot in time_slots]

@router.post("/time-slots/single")
async def create_single_time_slot(
    payload: TimeSlotCreate,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Create a single time slot (government officers and admins)."""
    svc = AppointmentService(db)
    slot = svc.create_single_time_slot(payload)
    return {
        "id": slot.id,
        "start_time": slot.start_time,
        "end_time": slot.end_time,
        "max_capacity": slot.max_capacity,
        "current_bookings": slot.current_bookings
    }

@router.post("/time-slots/recurring")
async def create_recurring_time_slots(
    payload: TimeSlotRecurringCreate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Create recurring time slots for a service over a date range (admin)."""
    svc = AppointmentService(db)
    # If weekdays provided, filter days accordingly
    start_date = payload.start_date
    end_date = payload.end_date
    created = []
    current = start_date
    while current <= end_date:
        if payload.weekdays is None:
            allowed = current.weekday() < 5
        else:
            allowed = current.weekday() in payload.weekdays
        if allowed:
            created.extend(
                svc.create_time_slots(
                    service_id=payload.service_id,
                    start_date=current,
                    end_date=current,
                    start_time=payload.start_time,
                    end_time=payload.end_time,
                    duration_minutes=payload.duration_minutes
                )
            )
        current = current + timedelta(days=1)
    return [{"id": s.id, "start_time": s.start_time, "end_time": s.end_time} for s in created]

@router.get("/time-slots/{service_id}/available")
async def get_available_time_slots(
    service_id: int,
    date: datetime,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get available time slots for a service on a specific date."""
    appointment_service = AppointmentService(db)
    time_slots = appointment_service.get_available_time_slots(service_id, date)
    
    return [
        {
            "id": slot.id,
            "start_time": slot.start_time,
            "end_time": slot.end_time,
            "max_capacity": slot.max_capacity,
            "current_bookings": slot.current_bookings
        }
        for slot in time_slots
    ]
