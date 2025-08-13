from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import User
from ..schemas import (
    ServiceCreate, ServiceUpdate, ServiceResponse, ServiceFilter
)
from ..services.service_service import ServiceService
from ..utils import get_current_active_user, require_role

router = APIRouter(prefix="/services", tags=["services"])

@router.post("/", response_model=ServiceResponse, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_data: ServiceCreate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Create a new service (admin only)."""
    service_service = ServiceService(db)
    return service_service.create_service(service_data)

@router.get("/", response_model=List[ServiceResponse])
async def get_services(
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all services."""
    service_service = ServiceService(db)
    return service_service.get_all_services(active_only)

@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get service by ID."""
    service_service = ServiceService(db)
    service = service_service.get_service_by_id(service_id)
    
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return service

@router.put("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_id: int,
    service_data: ServiceUpdate,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Update service (admin only)."""
    service_service = ServiceService(db)
    updated_service = service_service.update_service(service_id, service_data)
    
    if not updated_service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return updated_service

@router.put("/{service_id}/activate")
async def activate_service(
    service_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Activate a service (admin only)."""
    service_service = ServiceService(db)
    success = service_service.activate_service(service_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return {"message": "Service activated successfully"}

@router.put("/{service_id}/deactivate")
async def deactivate_service(
    service_id: int,
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Deactivate a service (admin only)."""
    service_service = ServiceService(db)
    success = service_service.deactivate_service(service_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    return {"message": "Service deactivated successfully"}

@router.get("/department/{department_id}", response_model=List[ServiceResponse])
async def get_services_by_department(
    department_id: int,
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all services for a specific department."""
    service_service = ServiceService(db)
    return service_service.get_services_by_department(department_id, active_only)

@router.post("/search")
async def search_services(
    filters: ServiceFilter,
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search services with filters and pagination."""
    service_service = ServiceService(db)
    return service_service.search_services(filters, page, size)

@router.get("/{service_id}/statistics")
async def get_service_statistics(
    service_id: int,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get statistics for a specific service (government officers only)."""
    service_service = ServiceService(db)
    return service_service.get_service_statistics(service_id)

@router.get("/popular/top-rated")
async def get_popular_services(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get most popular services based on appointment count."""
    service_service = ServiceService(db)
    return service_service.get_popular_services(limit)

@router.get("/duration/range")
async def get_services_by_duration(
    min_duration: int = Query(..., ge=15, le=480, description="Minimum duration in minutes"),
    max_duration: int = Query(..., ge=15, le=480, description="Maximum duration in minutes"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get services within a specific duration range."""
    service_service = ServiceService(db)
    services = service_service.get_services_by_duration(min_duration, max_duration)
    
    return [
        {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "duration_minutes": service.duration_minutes,
            "department_id": service.department_id
        }
        for service in services
    ]

@router.get("/documents/{document_type}")
async def get_services_with_required_documents(
    document_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get services that require a specific document type."""
    service_service = ServiceService(db)
    services = service_service.get_services_with_required_documents(document_type)
    
    return [
        {
            "id": service.id,
            "name": service.name,
            "description": service.description,
            "department_id": service.department_id
        }
        for service in services
    ]

@router.get("/{service_id}/capacity-utilization")
async def get_service_capacity_utilization(
    service_id: int,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get capacity utilization for a service (government officers only)."""
    service_service = ServiceService(db)
    return service_service.get_service_capacity_utilization(service_id)

@router.get("/pagination/list")
async def get_services_with_pagination(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    active_only: bool = Query(True, description="Filter by active status"),
    current_user: User = Depends(require_role("admin")),
    db: Session = Depends(get_db)
):
    """Get services with pagination (admin only)."""
    service_service = ServiceService(db)
    return service_service.get_services_with_pagination(page, size, active_only)
