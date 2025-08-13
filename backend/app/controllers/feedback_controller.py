from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import User
from ..schemas import (
    FeedbackCreate, FeedbackResponse
)
from ..services.feedback_service import FeedbackService
from ..utils import get_current_active_user, require_role

router = APIRouter(prefix="/feedback", tags=["feedback"])

@router.post("/", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
async def create_feedback(
    feedback_data: FeedbackCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new feedback entry."""
    feedback_service = FeedbackService(db)
    return feedback_service.create_feedback(current_user.id, feedback_data)

@router.get("/me", response_model=List[FeedbackResponse])
async def get_my_feedback(
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's feedback."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_user_feedback(current_user.id, limit)

@router.get("/{feedback_id}", response_model=FeedbackResponse)
async def get_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get feedback by ID."""
    feedback_service = FeedbackService(db)
    feedback = feedback_service.get_feedback_by_id(feedback_id)
    
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    # Check if user can access this feedback
    if feedback.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return feedback

@router.put("/{feedback_id}", response_model=FeedbackResponse)
async def update_feedback(
    feedback_id: int,
    new_rating: Optional[int] = Query(None, ge=1, le=5, description="New rating (1-5)"),
    new_comment: Optional[str] = Query(None, description="New comment"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update feedback (only by the user who submitted it)."""
    feedback_service = FeedbackService(db)
    updated_feedback = feedback_service.update_feedback(
        feedback_id, current_user.id, new_rating, new_comment
    )
    
    if not updated_feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found or cannot be updated"
        )
    
    return updated_feedback

@router.delete("/{feedback_id}")
async def delete_feedback(
    feedback_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete feedback (only by the user who submitted it)."""
    feedback_service = FeedbackService(db)
    success = feedback_service.delete_feedback(feedback_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback not found"
        )
    
    return {"message": "Feedback deleted successfully"}

@router.get("/appointment/{appointment_id}", response_model=Optional[FeedbackResponse])
async def get_appointment_feedback(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get feedback for a specific appointment."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_appointment_feedback(appointment_id)

# Government Officer and Admin endpoints
@router.get("/service/{service_id}", response_model=List[FeedbackResponse])
async def get_service_feedback(
    service_id: int,
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get all feedback for a specific service (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_service_feedback(service_id, limit)

@router.get("/department/{department_id}", response_model=List[FeedbackResponse])
async def get_department_feedback(
    department_id: int,
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get all feedback for services in a specific department (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_department_feedback(department_id, limit)

@router.get("/statistics/service/{service_id}")
async def get_service_rating_statistics(
    service_id: int,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get rating statistics for a specific service (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_service_rating_statistics(service_id)

@router.get("/statistics/department/{department_id}")
async def get_department_rating_statistics(
    department_id: int,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get rating statistics for all services in a department (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_department_rating_statistics(department_id)

@router.get("/statistics/overview")
async def get_overall_rating_statistics(
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get overall rating statistics across all services (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_overall_rating_statistics()

@router.get("/popular/top-rated")
async def get_top_rated_services(
    limit: int = Query(10, ge=1, le=50),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get top-rated services based on average rating."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_top_rated_services(limit)

@router.get("/trends/analysis")
async def get_feedback_trends(
    days: int = Query(30, ge=7, le=365, description="Number of days to analyze"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get feedback trends over a specified number of days (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_feedback_trends(days)

@router.get("/search/advanced")
async def search_feedback(
    search_term: Optional[str] = Query(None, description="Search term for comments"),
    min_rating: Optional[int] = Query(None, ge=1, le=5, description="Minimum rating"),
    max_rating: Optional[int] = Query(None, ge=1, le=5, description="Maximum rating"),
    service_id: Optional[int] = Query(None, description="Filter by service ID"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Search feedback with various filters (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.search_feedback(search_term, min_rating, max_rating, service_id)

@router.get("/recent/submissions")
async def get_recent_feedback(
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get most recent feedback submissions (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_recent_feedback(limit)

@router.get("/summary/comprehensive")
async def get_feedback_statistics_summary(
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get a comprehensive summary of feedback statistics (government officers only)."""
    feedback_service = FeedbackService(db)
    return feedback_service.get_feedback_statistics_summary()
