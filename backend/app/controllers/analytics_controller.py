from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..db import get_db
from ..models import User
from ..services.analytics_service import AnalyticsService
from ..utils import get_current_active_user, require_role

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/dashboard/overview")
async def get_dashboard_overview(
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard overview statistics (government officers only)."""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_dashboard_overview()

@router.get("/appointments/trends")
async def get_appointment_analytics(
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get appointment analytics over a specified period (government officers only)."""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_appointment_analytics(days)

@router.get("/departments/performance")
async def get_department_performance(
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get performance metrics for each department (government officers only)."""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_department_performance()

@router.get("/users/engagement")
async def get_user_engagement_metrics(
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get user engagement metrics (government officers only)."""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_user_engagement_metrics(days)

@router.get("/capacity/utilization")
async def get_capacity_utilization(
    service_id: Optional[int] = Query(None, description="Filter by service ID"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get capacity utilization analytics (government officers only)."""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_capacity_utilization(service_id)

@router.get("/documents/overview")
async def get_document_analytics(
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get document upload and verification analytics (government officers only)."""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_document_analytics()

@router.get("/feedback/satisfaction")
async def get_feedback_analytics(
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get feedback and satisfaction analytics (government officers only)."""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_feedback_analytics(days)
