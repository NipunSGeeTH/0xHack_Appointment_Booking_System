from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from ..models import Service, Department, Appointment, TimeSlot
from ..schemas import ServiceCreate, ServiceUpdate, ServiceResponse, ServiceFilter
from ..utils import paginate_query

class ServiceService:
    def __init__(self, db: Session):
        self.db = db

    def create_service(self, service_data: ServiceCreate) -> Service:
        """Create a new service."""
        # Validate department exists and is active
        department = self.db.query(Department).filter(
            Department.id == service_data.department_id,
            Department.is_active == True
        ).first()
        if not department:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found or inactive"
            )
        
        # Check if service name already exists in the same department
        existing_service = self.db.query(Service).filter(
            Service.name == service_data.name,
            Service.department_id == service_data.department_id
        ).first()
        if existing_service:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service name already exists in this department"
            )
        
        # Create service object
        db_service = Service(
            name=service_data.name,
            description=service_data.description,
            department_id=service_data.department_id,
            duration_minutes=service_data.duration_minutes,
            max_daily_appointments=service_data.max_daily_appointments,
            required_documents=service_data.required_documents
        )
        
        try:
            self.db.add(db_service)
            self.db.commit()
            self.db.refresh(db_service)
            return db_service
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service creation failed"
            )

    def get_service_by_id(self, service_id: int) -> Optional[Service]:
        """Get service by ID."""
        return self.db.query(Service).filter(Service.id == service_id).first()

    def get_service_by_name(self, name: str, department_id: Optional[int] = None) -> Optional[Service]:
        """Get service by name, optionally filtered by department."""
        query = self.db.query(Service).filter(Service.name == name)
        if department_id:
            query = query.filter(Service.department_id == department_id)
        return query.first()

    def get_services_by_department(self, department_id: int, active_only: bool = True) -> List[Service]:
        """Get all services for a specific department."""
        query = self.db.query(Service).filter(Service.department_id == department_id)
        if active_only:
            query = query.filter(Service.is_active == True)
        return query.order_by(Service.name).all()

    def get_all_services(self, active_only: bool = True) -> List[Service]:
        """Get all services, optionally filtered by active status."""
        query = self.db.query(Service)
        if active_only:
            query = query.filter(Service.is_active == True)
        return query.order_by(Service.name).all()

    def update_service(self, service_id: int, service_data: ServiceUpdate) -> Optional[Service]:
        """Update service information."""
        service = self.get_service_by_id(service_id)
        if not service:
            return None
        
        # Check if new name conflicts with existing service in the same department
        if service_data.name and service_data.name != service.name:
            existing_service = self.db.query(Service).filter(
                Service.name == service_data.name,
                Service.department_id == service.department_id,
                Service.id != service_id
            ).first()
            if existing_service:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Service name already exists in this department"
                )
        
        # Update fields if provided
        if service_data.name is not None:
            service.name = service_data.name
        if service_data.description is not None:
            service.description = service_data.description
        if service_data.duration_minutes is not None:
            service.duration_minutes = service_data.duration_minutes
        if service_data.max_daily_appointments is not None:
            service.max_daily_appointments = service_data.max_daily_appointments
        if service_data.required_documents is not None:
            service.required_documents = service_data.required_documents
        if service_data.is_active is not None:
            service.is_active = service_data.is_active
        
        service.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            self.db.refresh(service)
            return service
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Service update failed"
            )

    def deactivate_service(self, service_id: int) -> bool:
        """Deactivate a service."""
        service = self.get_service_by_id(service_id)
        if not service:
            return False
        
        # Check if service has pending or confirmed appointments
        active_appointments = self.db.query(Appointment).filter(
            Appointment.service_id == service_id,
            Appointment.status.in_(['pending', 'confirmed'])
        ).count()
        
        if active_appointments > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate service with active appointments"
            )
        
        service.is_active = False
        service.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def activate_service(self, service_id: int) -> bool:
        """Activate a service."""
        service = self.get_service_by_id(service_id)
        if not service:
            return False
        
        service.is_active = True
        service.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def search_services(self, filters: ServiceFilter, page: int = 1, size: int = 10) -> Dict[str, Any]:
        """Search services with filters and pagination."""
        query = self.db.query(Service).join(Department)
        
        if filters.department_id:
            query = query.filter(Service.department_id == filters.department_id)
        if filters.is_active is not None:
            query = query.filter(Service.is_active == filters.is_active)
        if filters.search:
            search_filter = f"%{filters.search}%"
            query = query.filter(
                (Service.name.ilike(search_filter)) |
                (Service.description.ilike(search_filter))
            )
        
        query = query.order_by(Service.name)
        
        return paginate_query(query, page, size)

    def get_service_statistics(self, service_id: int) -> Dict[str, Any]:
        """Get statistics for a specific service."""
        # Count appointments by status
        total_appointments = self.db.query(Appointment).filter(Appointment.service_id == service_id).count()
        pending_appointments = self.db.query(Appointment).filter(
            Appointment.service_id == service_id,
            Appointment.status == 'pending'
        ).count()
        confirmed_appointments = self.db.query(Appointment).filter(
            Appointment.service_id == service_id,
            Appointment.status == 'confirmed'
        ).count()
        completed_appointments = self.db.query(Appointment).filter(
            Appointment.service_id == service_id,
            Appointment.status == 'completed'
        ).count()
        cancelled_appointments = self.db.query(Appointment).filter(
            Appointment.service_id == service_id,
            Appointment.status == 'cancelled'
        ).count()
        
        # Count time slots
        total_time_slots = self.db.query(TimeSlot).filter(TimeSlot.service_id == service_id).count()
        available_time_slots = self.db.query(TimeSlot).filter(
            TimeSlot.service_id == service_id,
            TimeSlot.is_available == True
        ).count()
        
        return {
            "total_appointments": total_appointments,
            "pending_appointments": pending_appointments,
            "confirmed_appointments": confirmed_appointments,
            "completed_appointments": completed_appointments,
            "cancelled_appointments": cancelled_appointments,
            "total_time_slots": total_time_slots,
            "available_time_slots": available_time_slots
        }

    def get_popular_services(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular services based on appointment count."""
        services = self.db.query(
            Service.id,
            Service.name,
            Service.department_id,
            Department.name.label('department_name')
        ).join(Department).filter(Service.is_active == True).all()
        
        service_stats = []
        for service in services:
            appointment_count = self.db.query(Appointment).filter(
                Appointment.service_id == service.id
            ).count()
            
            service_stats.append({
                "id": service.id,
                "name": service.name,
                "department_id": service.department_id,
                "department_name": service.department_name,
                "appointment_count": appointment_count
            })
        
        # Sort by appointment count and return top services
        service_stats.sort(key=lambda x: x['appointment_count'], reverse=True)
        return service_stats[:limit]

    def get_services_by_duration(self, min_duration: int, max_duration: int) -> List[Service]:
        """Get services within a specific duration range."""
        return self.db.query(Service).filter(
            Service.duration_minutes >= min_duration,
            Service.duration_minutes <= max_duration,
            Service.is_active == True
        ).order_by(Service.duration_minutes).all()

    def get_services_with_required_documents(self, document_type: str) -> List[Service]:
        """Get services that require a specific document type."""
        return self.db.query(Service).filter(
            Service.required_documents.ilike(f"%{document_type}%"),
            Service.is_active == True
        ).order_by(Service.name).all()

    def get_service_capacity_utilization(self, service_id: int) -> Dict[str, Any]:
        """Get capacity utilization for a service."""
        service = self.get_service_by_id(service_id)
        if not service:
            return {}
        
        # Get total time slots for today
        today = datetime.now().date()
        today_slots = self.db.query(TimeSlot).filter(
            TimeSlot.service_id == service_id,
            TimeSlot.start_time >= today,
            TimeSlot.start_time < today + timedelta(days=1)
        ).all()
        
        total_capacity = sum(slot.max_capacity for slot in today_slots)
        total_bookings = sum(slot.current_bookings for slot in today_slots)
        
        utilization_percentage = (total_bookings / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            "service_id": service_id,
            "service_name": service.name,
            "total_capacity": total_capacity,
            "total_bookings": total_bookings,
            "utilization_percentage": round(utilization_percentage, 2),
            "available_capacity": total_capacity - total_bookings
        }

    def get_services_with_pagination(self, page: int = 1, size: int = 10, 
                                   active_only: bool = True) -> Dict[str, Any]:
        """Get services with pagination."""
        query = self.db.query(Service).join(Department)
        if active_only:
            query = query.filter(Service.is_active == True)
        
        query = query.order_by(Service.name)
        
        return paginate_query(query, page, size)
