from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, case

from ..models import Feedback, User, Appointment, Service, Department
from ..schemas import FeedbackCreate, FeedbackResponse

class FeedbackService:
    def __init__(self, db: Session):
        self.db = db

    def create_feedback(self, user_id: int, feedback_data: FeedbackCreate) -> Feedback:
        """Create a new feedback entry."""
        # Validate appointment exists and belongs to user
        appointment = self.db.query(Appointment).filter(
            Appointment.id == feedback_data.appointment_id,
            Appointment.user_id == user_id
        ).first()
        if not appointment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Appointment not found or access denied"
            )
        
        # Check if appointment is completed
        if appointment.status != 'completed':
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback can only be submitted for completed appointments"
            )
        
        # Check if feedback already exists for this appointment
        existing_feedback = self.db.query(Feedback).filter(
            Feedback.appointment_id == feedback_data.appointment_id
        ).first()
        if existing_feedback:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback already exists for this appointment"
            )
        
        # Validate rating
        if not 1 <= feedback_data.rating <= 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be between 1 and 5"
            )
        
        # Create feedback object
        db_feedback = Feedback(
            user_id=user_id,
            appointment_id=feedback_data.appointment_id,
            rating=feedback_data.rating,
            comment=feedback_data.comment
        )
        
        try:
            self.db.add(db_feedback)
            self.db.commit()
            self.db.refresh(db_feedback)
            return db_feedback
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback creation failed"
            )

    def get_feedback_by_id(self, feedback_id: int) -> Optional[Feedback]:
        """Get feedback by ID."""
        return self.db.query(Feedback).filter(Feedback.id == feedback_id).first()

    def get_user_feedback(self, user_id: int, limit: int = 100) -> List[Feedback]:
        """Get all feedback submitted by a specific user."""
        return self.db.query(Feedback).filter(
            Feedback.user_id == user_id
        ).order_by(Feedback.created_at.desc()).limit(limit).all()

    def get_appointment_feedback(self, appointment_id: int) -> Optional[Feedback]:
        """Get feedback for a specific appointment."""
        return self.db.query(Feedback).filter(
            Feedback.appointment_id == appointment_id
        ).first()

    def get_service_feedback(self, service_id: int, limit: int = 100) -> List[Feedback]:
        """Get all feedback for a specific service."""
        return self.db.query(Feedback).join(Appointment).filter(
            Appointment.service_id == service_id
        ).order_by(Feedback.created_at.desc()).limit(limit).all()

    def get_department_feedback(self, department_id: int, limit: int = 100) -> List[Feedback]:
        """Get all feedback for services in a specific department."""
        return self.db.query(Feedback).join(Appointment).join(Service).filter(
            Service.department_id == department_id
        ).order_by(Feedback.created_at.desc()).limit(limit).all()

    def update_feedback(self, feedback_id: int, user_id: int, 
                       new_rating: Optional[int] = None, new_comment: Optional[str] = None) -> Optional[Feedback]:
        """Update feedback (only by the user who submitted it)."""
        feedback = self.get_feedback_by_id(feedback_id)
        if not feedback:
            return None
        
        if feedback.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own feedback"
            )
        
        # Check if feedback is within editable timeframe (e.g., 24 hours)
        if feedback.created_at < datetime.utcnow() - timedelta(hours=24):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Feedback can only be updated within 24 hours of submission"
            )
        
        # Update fields if provided
        if new_rating is not None:
            if not 1 <= new_rating <= 5:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Rating must be between 1 and 5"
                )
            feedback.rating = new_rating
        
        if new_comment is not None:
            feedback.comment = new_comment
        
        try:
            self.db.commit()
            self.db.refresh(feedback)
            return feedback
        except IntegrityError:
            self.db.rollback()
            return None

    def delete_feedback(self, feedback_id: int, user_id: int) -> bool:
        """Delete feedback (only by the user who submitted it)."""
        feedback = self.get_feedback_by_id(feedback_id)
        if not feedback:
            return False
        
        if feedback.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own feedback"
            )
        
        try:
            self.db.delete(feedback)
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def get_service_rating_statistics(self, service_id: int) -> Dict[str, Any]:
        """Get rating statistics for a specific service."""
        feedback_stats = self.db.query(
            func.avg(Feedback.rating).label('average_rating'),
            func.count(Feedback.id).label('total_feedback'),
            func.sum(case((Feedback.rating == 5, 1), else_=0)).label('five_star'),
            func.sum(case((Feedback.rating == 4, 1), else_=0)).label('four_star'),
            func.sum(case((Feedback.rating == 3, 1), else_=0)).label('three_star'),
            func.sum(case((Feedback.rating == 2, 1), else_=0)).label('two_star'),
            func.sum(case((Feedback.rating == 1, 1), else_=0)).label('one_star')
        ).join(Appointment).filter(Appointment.service_id == service_id).first()
        
        if not feedback_stats or feedback_stats.total_feedback == 0:
            return {
                "average_rating": 0,
                "total_feedback": 0,
                "rating_distribution": {},
                "satisfaction_percentage": 0
            }
        
        # Calculate rating distribution
        rating_distribution = {
            "5 stars": feedback_stats.five_star or 0,
            "4 stars": feedback_stats.four_star or 0,
            "3 stars": feedback_stats.three_star or 0,
            "2 stars": feedback_stats.two_star or 0,
            "1 star": feedback_stats.one_star or 0
        }
        
        # Calculate satisfaction percentage (4+ stars)
        satisfaction_count = (feedback_stats.four_star or 0) + (feedback_stats.five_star or 0)
        satisfaction_percentage = (satisfaction_count / feedback_stats.total_feedback) * 100
        
        return {
            "average_rating": round(feedback_stats.average_rating, 2),
            "total_feedback": feedback_stats.total_feedback,
            "rating_distribution": rating_distribution,
            "satisfaction_percentage": round(satisfaction_percentage, 2)
        }

    def get_department_rating_statistics(self, department_id: int) -> Dict[str, Any]:
        """Get rating statistics for all services in a department."""
        feedback_stats = self.db.query(
            func.avg(Feedback.rating).label('average_rating'),
            func.count(Feedback.id).label('total_feedback')
        ).join(Appointment).join(Service).filter(Service.department_id == department_id).first()
        
        if not feedback_stats or feedback_stats.total_feedback == 0:
            return {
                "average_rating": 0,
                "total_feedback": 0
            }
        
        return {
            "average_rating": round(feedback_stats.average_rating, 2),
            "total_feedback": feedback_stats.total_feedback
        }

    def get_overall_rating_statistics(self) -> Dict[str, Any]:
        """Get overall rating statistics across all services."""
        feedback_stats = self.db.query(
            func.avg(Feedback.rating).label('average_rating'),
            func.count(Feedback.id).label('total_feedback'),
            func.sum(case((Feedback.rating >= 4, 1), else_=0)).label('satisfied_customers'),
            func.sum(case((Feedback.rating <= 2, 1), else_=0)).label('dissatisfied_customers')
        ).first()
        
        if not feedback_stats or feedback_stats.total_feedback == 0:
            return {
                "average_rating": 0,
                "total_feedback": 0,
                "satisfaction_percentage": 0,
                "dissatisfaction_percentage": 0
            }
        
        satisfaction_percentage = (feedback_stats.satisfied_customers / feedback_stats.total_feedback) * 100
        dissatisfaction_percentage = (feedback_stats.dissatisfied_customers / feedback_stats.total_feedback) * 100
        
        return {
            "average_rating": round(feedback_stats.average_rating, 2),
            "total_feedback": feedback_stats.total_feedback,
            "satisfaction_percentage": round(satisfaction_percentage, 2),
            "dissatisfaction_percentage": round(dissatisfaction_percentage, 2)
        }

    def get_top_rated_services(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top-rated services based on average rating."""
        top_services = self.db.query(
            Service.id,
            Service.name,
            Department.name.label('department_name'),
            func.avg(Feedback.rating).label('average_rating'),
            func.count(Feedback.id).label('feedback_count')
        ).join(Appointment).join(Department).join(Feedback).group_by(
            Service.id, Service.name, Department.name
        ).having(func.count(Feedback.id) >= 3).order_by(
            func.avg(Feedback.rating).desc()
        ).limit(limit).all()
        
        return [
            {
                "service_id": service.id,
                "service_name": service.name,
                "department_name": service.department_name,
                "average_rating": round(service.average_rating, 2),
                "feedback_count": service.feedback_count
            }
            for service in top_services
        ]

    def get_feedback_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get feedback trends over a specified number of days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        
        daily_stats = self.db.query(
            func.date(Feedback.created_at).label('date'),
            func.avg(Feedback.rating).label('average_rating'),
            func.count(Feedback.id).label('feedback_count')
        ).filter(Feedback.created_at >= start_date).group_by(
            func.date(Feedback.created_at)
        ).order_by(func.date(Feedback.created_at)).all()
        
        return [
            {
                "date": stat.date.strftime('%Y-%m-%d'),
                "average_rating": round(stat.average_rating, 2),
                "feedback_count": stat.feedback_count
            }
            for stat in daily_stats
        ]

    def search_feedback(self, search_term: str = None, min_rating: int = None, 
                       max_rating: int = None, service_id: int = None) -> List[Feedback]:
        """Search feedback with various filters."""
        query = self.db.query(Feedback).join(Appointment).join(Service)
        
        if search_term:
            search_filter = f"%{search_term}%"
            query = query.filter(Feedback.comment.ilike(search_filter))
        
        if min_rating is not None:
            query = query.filter(Feedback.rating >= min_rating)
        
        if max_rating is not None:
            query = query.filter(Feedback.rating <= max_rating)
        
        if service_id:
            query = query.filter(Appointment.service_id == service_id)
        
        return query.order_by(Feedback.created_at.desc()).all()

    def get_feedback_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Feedback]:
        """Get feedback submitted within a date range."""
        return self.db.query(Feedback).filter(
            Feedback.created_at >= start_date,
            Feedback.created_at <= end_date
        ).order_by(Feedback.created_at.desc()).all()

    def get_recent_feedback(self, limit: int = 20) -> List[Feedback]:
        """Get most recent feedback submissions."""
        return self.db.query(Feedback).order_by(
            Feedback.created_at.desc()
        ).limit(limit).all()

    def get_feedback_statistics_summary(self) -> Dict[str, Any]:
        """Get a comprehensive summary of feedback statistics."""
        overall_stats = self.get_overall_rating_statistics()
        
        # Get top and bottom rated services
        top_services = self.get_top_rated_services(5)
        bottom_services = self.get_top_rated_services(5)  # This will need modification for bottom-rated
        
        # Get recent feedback count
        recent_feedback = self.db.query(Feedback).filter(
            Feedback.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()
        
        return {
            "overall": overall_stats,
            "top_services": top_services,
            "recent_feedback_count": recent_feedback,
            "total_services_with_feedback": self.db.query(Service).join(Appointment).join(Feedback).distinct().count()
        }
