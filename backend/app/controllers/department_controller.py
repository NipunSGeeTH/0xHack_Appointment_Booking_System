from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import User
from ..schemas import (
    DepartmentCreate, DepartmentUpdate, DepartmentResponse
)
from ..services.department_service import DepartmentService
from ..utils import get_current_active_user, require_role

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED)
async def create_department(
    department_data: DepartmentCreate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Create a new department (admin only)."""
    department_service = DepartmentService(db)
    return department_service.create_department(department_data)

@router.get("/", response_model=List[DepartmentResponse])
async def get_departments(
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all departments."""
    department_service = DepartmentService(db)
    return department_service.get_all_departments(active_only)

@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get department by ID."""
    department_service = DepartmentService(db)
    department = department_service.get_department_by_id(department_id)
    
    if not department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    return department

@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: int,
    department_data: DepartmentUpdate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Update department (admin only)."""
    department_service = DepartmentService(db)
    updated_department = department_service.update_department(department_id, department_data)
    
    if not updated_department:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    return updated_department

@router.put("/{department_id}/activate")
async def activate_department(
    department_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Activate a department (admin only)."""
    department_service = DepartmentService(db)
    success = department_service.activate_department(department_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    return {"message": "Department activated successfully"}

@router.put("/{department_id}/deactivate")
async def deactivate_department(
    department_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Deactivate a department (admin only)."""
    department_service = DepartmentService(db)
    success = department_service.deactivate_department(department_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Department not found"
        )
    
    return {"message": "Department deactivated successfully"}

@router.get("/{department_id}/services")
async def get_department_services(
    department_id: int,
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all services for a specific department."""
    department_service = DepartmentService(db)
    services = department_service.get_department_services(department_id, active_only)
    
    return [
        {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "duration_minutes": service.duration_minutes,
            "max_daily_appointments": service.max_daily_appointments,
            "is_active": service.is_active
        }
        for service in services
    ]

@router.get("/{department_id}/officers")
async def get_department_officers(
    department_id: int,
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get all officers for a specific department (government officers only)."""
    department_service = DepartmentService(db)
    officers = department_service.get_department_officers(department_id, active_only)
    
    return [
        {
            "id": officer.id,
            "officer_id": officer.officer_id,
            "designation": officer.designation,
            "user": {
                "id": officer.user.id,
                "first_name": officer.user.first_name,
                "last_name": officer.user.last_name,
                "email": officer.user.email
            },
            "is_active": officer.is_active
        }
        for officer in officers
    ]

@router.get("/search/{search_term}", response_model=List[DepartmentResponse])
async def search_departments(
    search_term: str,
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search departments by name, description, or location."""
    department_service = DepartmentService(db)
    departments = department_service.search_departments(search_term, active_only)
    return departments

@router.get("/{department_id}/statistics")
async def get_department_statistics(
    department_id: int,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific department (government officers only)."""
    department_service = DepartmentService(db)
    return department_service.get_department_statistics(department_id)

@router.get("/statistics/overview")
async def get_all_department_statistics(
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get statistics for all departments (admin only)."""
    department_service = DepartmentService(db)
    return department_service.get_all_department_statistics()

@router.get("/pagination/list")
async def get_departments_with_pagination(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get departments with pagination (admin only)."""
    department_service = DepartmentService(db)
    return department_service.get_departments_with_pagination(page, size, active_only)

@router.get("/location/{location}")
async def get_departments_by_location(
    location: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get departments by location."""
    department_service = DepartmentService(db)
    departments = department_service.get_department_by_location(location)
    
    return [
        {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description,
            "location": dept.location,
            "contact_number": dept.contact_number,
            "email": dept.email,
            "operating_hours": dept.operating_hours
        }
        for dept in departments
    ]

@router.get("/operating-hours/{day_of_week}")
async def get_departments_by_operating_hours(
    day_of_week: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get departments that operate on a specific day of the week."""
    department_service = DepartmentService(db)
    departments = department_service.get_departments_by_operating_hours(day_of_week)
    
    return [
        {
            "id": dept.id,
            "name": dept.name,
            "description": dept.description,
            "location": dept.location,
            "operating_hours": dept.operating_hours
        }
        for dept in departments
    ]
