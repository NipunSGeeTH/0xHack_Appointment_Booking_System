from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..models import Department, Service, GovernmentOfficer
from ..schemas import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from ..utils import paginate_query

class DepartmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_department(self, department_data: DepartmentCreate) -> Department:
        """Create a new department."""
        # Check if department name already exists
        if self.db.query(Department).filter(Department.name == department_data.name).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department name already exists"
            )
        
        # Create department object
        db_department = Department(
            name=department_data.name,
            description=department_data.description,
            location=department_data.location,
            contact_number=department_data.contact_number,
            email=department_data.email,
            operating_hours=department_data.operating_hours
        )
        
        try:
            self.db.add(db_department)
            self.db.commit()
            self.db.refresh(db_department)
            return db_department
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department creation failed"
            )

    def get_department_by_id(self, department_id: int) -> Optional[Department]:
        """Get department by ID."""
        return self.db.query(Department).filter(Department.id == department_id).first()

    def get_department_by_name(self, name: str) -> Optional[Department]:
        """Get department by name."""
        return self.db.query(Department).filter(Department.name == name).first()

    def get_all_departments(self, active_only: bool = True) -> List[Department]:
        """Get all departments, optionally filtered by active status."""
        query = self.db.query(Department)
        if active_only:
            query = query.filter(Department.is_active == True)
        return query.order_by(Department.name).all()

    def update_department(self, department_id: int, department_data: DepartmentUpdate) -> Optional[Department]:
        """Update department information."""
        department = self.get_department_by_id(department_id)
        if not department:
            return None
        
        # Check if new name conflicts with existing department
        if department_data.name and department_data.name != department.name:
            existing_dept = self.db.query(Department).filter(
                Department.name == department_data.name,
                Department.id != department_id
            ).first()
            if existing_dept:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Department name already exists"
                )
        
        # Update fields if provided
        if department_data.name is not None:
            department.name = department_data.name
        if department_data.description is not None:
            department.description = department_data.description
        if department_data.location is not None:
            department.location = department_data.location
        if department_data.contact_number is not None:
            department.contact_number = department_data.contact_number
        if department_data.email is not None:
            department.email = department_data.email
        if department_data.operating_hours is not None:
            department.operating_hours = department_data.operating_hours
        if department_data.is_active is not None:
            department.is_active = department_data.is_active
        
        department.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            self.db.refresh(department)
            return department
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department update failed"
            )

    def deactivate_department(self, department_id: int) -> bool:
        """Deactivate a department."""
        department = self.get_department_by_id(department_id)
        if not department:
            return False
        
        # Check if department has active services
        active_services = self.db.query(Service).filter(
            Service.department_id == department_id,
            Service.is_active == True
        ).count()
        
        if active_services > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate department with active services"
            )
        
        department.is_active = False
        department.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def activate_department(self, department_id: int) -> bool:
        """Activate a department."""
        department = self.get_department_by_id(department_id)
        if not department:
            return False
        
        department.is_active = True
        department.updated_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def get_department_services(self, department_id: int, active_only: bool = True) -> List[Service]:
        """Get all services for a specific department."""
        query = self.db.query(Service).filter(Service.department_id == department_id)
        if active_only:
            query = query.filter(Service.is_active == True)
        return query.order_by(Service.name).all()

    def get_department_officers(self, department_id: int, active_only: bool = True) -> List[GovernmentOfficer]:
        """Get all officers for a specific department."""
        query = self.db.query(GovernmentOfficer).filter(GovernmentOfficer.department_id == department_id)
        if active_only:
            query = query.filter(GovernmentOfficer.is_active == True)
        return query.order_by(GovernmentOfficer.designation).all()

    def search_departments(self, search_term: str, active_only: bool = True) -> List[Department]:
        """Search departments by name, description, or location."""
        search_filter = f"%{search_term}%"
        query = self.db.query(Department).filter(
            (Department.name.ilike(search_filter)) |
            (Department.description.ilike(search_filter)) |
            (Department.location.ilike(search_filter))
        )
        if active_only:
            query = query.filter(Department.is_active == True)
        return query.order_by(Department.name).all()

    def get_department_statistics(self, department_id: int) -> Dict[str, Any]:
        """Get statistics for a specific department."""
        # Count services
        total_services = self.db.query(Service).filter(Service.department_id == department_id).count()
        active_services = self.db.query(Service).filter(
            Service.department_id == department_id,
            Service.is_active == True
        ).count()
        
        # Count officers
        total_officers = self.db.query(GovernmentOfficer).filter(
            GovernmentOfficer.department_id == department_id
        ).count()
        active_officers = self.db.query(GovernmentOfficer).filter(
            GovernmentOfficer.department_id == department_id,
            GovernmentOfficer.is_active == True
        ).count()
        
        return {
            "total_services": total_services,
            "active_services": active_services,
            "total_officers": total_officers,
            "active_officers": active_officers
        }

    def get_all_department_statistics(self) -> Dict[str, Any]:
        """Get statistics for all departments."""
        departments = self.get_all_departments(active_only=True)
        stats = {}
        
        for dept in departments:
            stats[dept.name] = self.get_department_statistics(dept.id)
        
        return stats

    def get_departments_with_pagination(self, page: int = 1, size: int = 10, 
                                      active_only: bool = True) -> Dict[str, Any]:
        """Get departments with pagination."""
        query = self.db.query(Department)
        if active_only:
            query = query.filter(Department.is_active == True)
        
        query = query.order_by(Department.name)
        
        return paginate_query(query, page, size)

    def get_department_by_location(self, location: str) -> List[Department]:
        """Get departments by location."""
        return self.db.query(Department).filter(
            Department.location.ilike(f"%{location}%"),
            Department.is_active == True
        ).order_by(Department.name).all()

    def get_departments_by_operating_hours(self, day_of_week: str) -> List[Department]:
        """Get departments that operate on a specific day of the week."""
        # This is a simplified implementation - you might want to parse operating_hours more carefully
        return self.db.query(Department).filter(
            Department.operating_hours.ilike(f"%{day_of_week}%"),
            Department.is_active == True
        ).order_by(Department.name).all()
