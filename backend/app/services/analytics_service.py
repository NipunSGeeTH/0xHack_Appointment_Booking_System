from sqlalchemy.orm import Session
from sqlalchemy import func, case, extract
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from ..models import (
    User, Appointment, Service, Department, TimeSlot, 
    Document, Feedback, Notification, AppointmentStatus, UserRole
)

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_dashboard_overview(self) -> Dict[str, Any]:
        """Get comprehensive dashboard overview statistics."""
        # User statistics
        total_users = self.db.query(User).count()
        active_users = self.db.query(User).filter(User.is_active == True).count()
        citizens = self.db.query(User).filter(User.role == UserRole.CITIZEN).count()
        officers = self.db.query(User).filter(User.role == UserRole.GOVERNMENT_OFFICER).count()
        
        # Appointment statistics
        total_appointments = self.db.query(Appointment).count()
        pending_appointments = self.db.query(Appointment).filter(
            Appointment.status == AppointmentStatus.PENDING
        ).count()
        completed_appointments = self.db.query(Appointment).filter(
            Appointment.status == AppointmentStatus.COMPLETED
        ).count()
        
        # Service and department statistics
        total_services = self.db.query(Service).filter(Service.is_active == True).count()
        total_departments = self.db.query(Department).filter(Department.is_active == True).count()
        
        # Document statistics
        total_documents = self.db.query(Document).count()
        verified_documents = self.db.query(Document).filter(Document.is_verified == True).count()
        
        # Feedback statistics
        total_feedback = self.db.query(Feedback).count()
        avg_rating = self.db.query(func.avg(Feedback.rating)).scalar() or 0
        
        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "citizens": citizens,
                "officers": officers
            },
            "appointments": {
                "total": total_appointments,
                "pending": pending_appointments,
                "completed": completed_appointments
            },
            "services": {
                "total": total_services,
                "departments": total_departments
            },
            "documents": {
                "total": total_documents,
                "verified": verified_documents,
                "verification_rate": round((verified_documents / total_documents * 100), 2) if total_documents > 0 else 0
            },
            "feedback": {
                "total": total_feedback,
                "average_rating": round(avg_rating, 2)
            }
        }

    def get_appointment_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get appointment analytics over a specified period."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Daily appointment counts
        daily_stats = self.db.query(
            func.date(Appointment.created_at).label('date'),
            func.count(Appointment.id).label('total'),
            func.sum(case((Appointment.status == AppointmentStatus.COMPLETED, 1), else_=0)).label('completed')
        ).filter(
            Appointment.created_at >= start_date
        ).group_by(
            func.date(Appointment.created_at)
        ).order_by(func.date(Appointment.created_at)).all()
        
        # Service popularity
        service_popularity = self.db.query(
            Service.name,
            func.count(Appointment.id).label('appointment_count')
        ).join(Appointment).filter(
            Appointment.created_at >= start_date
        ).group_by(Service.name).order_by(
            func.count(Appointment.id).desc()
        ).limit(10).all()
        
        return {
            "daily_stats": [
                {
                    "date": stat.date.strftime('%Y-%m-%d'),
                    "total": stat.total,
                    "completed": stat.completed or 0
                }
                for stat in daily_stats
            ],
            "service_popularity": [
                {
                    "service": stat.name,
                    "appointment_count": stat.appointment_count
                }
                for stat in service_popularity
            ]
        }

    def get_department_performance(self) -> List[Dict[str, Any]]:
        """Get performance metrics for each department."""
        dept_performance = []
        
        departments = self.db.query(Department).filter(Department.is_active == True).all()
        
        for dept in departments:
            # Appointment statistics
            appointments = self.db.query(Appointment).join(Service).filter(
                Service.department_id == dept.id
            ).all()
            
            total_appointments = len(appointments)
            if total_appointments == 0:
                dept_performance.append({
                    "department_id": dept.id,
                    "department_name": dept.name,
                    "total_appointments": 0,
                    "completion_rate": 0,
                    "satisfaction_score": 0
                })
                continue
            
            completed_appointments = len([a for a in appointments if a.status == AppointmentStatus.COMPLETED])
            completion_rate = (completed_appointments / total_appointments) * 100
            
            # Get satisfaction score from feedback
            feedback_stats = self.db.query(
                func.avg(Feedback.rating).label('avg_rating')
            ).join(Appointment).join(Service).filter(
                Service.department_id == dept.id
            ).scalar()
            
            satisfaction_score = round(feedback_stats or 0, 2)
            
            dept_performance.append({
                "department_id": dept.id,
                "department_name": dept.name,
                "total_appointments": total_appointments,
                "completion_rate": round(completion_rate, 2),
                "satisfaction_score": satisfaction_score
            })
        
        return sorted(dept_performance, key=lambda x: x['completion_rate'], reverse=True)

    def get_user_engagement_metrics(self, days: int = 30) -> Dict[str, Any]:
        """Get user engagement metrics."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # New user registrations
        new_users = self.db.query(User).filter(
            User.created_at >= start_date
        ).count()
        
        # Active users (users with appointments in the period)
        active_users = self.db.query(
            func.count(func.distinct(Appointment.user_id))
        ).filter(Appointment.created_at >= start_date).scalar()
        
        return {
            "new_users": new_users,
            "active_users": active_users
        }

    def get_capacity_utilization(self, service_id: Optional[int] = None) -> Dict[str, Any]:
        """Get capacity utilization analytics."""
        query = self.db.query(TimeSlot)
        if service_id:
            query = query.filter(TimeSlot.service_id == service_id)
        
        # Get time slots for the last 30 days
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=30)
        
        time_slots = query.filter(
            TimeSlot.start_time >= start_date
        ).all()
        
        if not time_slots:
            return {
                "total_capacity": 0,
                "total_bookings": 0,
                "utilization_rate": 0
            }
        
        total_capacity = sum(slot.max_capacity for slot in time_slots)
        total_bookings = sum(slot.current_bookings for slot in time_slots)
        utilization_rate = (total_bookings / total_capacity * 100) if total_capacity > 0 else 0
        
        return {
            "total_capacity": total_capacity,
            "total_bookings": total_bookings,
            "utilization_rate": round(utilization_rate, 2)
        }

    def get_document_analytics(self) -> Dict[str, Any]:
        """Get document upload and verification analytics."""
        # Document type distribution
        type_distribution = self.db.query(
            Document.document_type,
            func.count(Document.id).label('count')
        ).group_by(Document.document_type).all()
        
        # Verification statistics
        total_documents = self.db.query(Document).count()
        verified_documents = self.db.query(Document).filter(Document.is_verified == True).count()
        
        return {
            "type_distribution": [
                {
                    "type": stat.document_type,
                    "count": stat.count
                }
                for stat in type_distribution
            ],
            "verification_stats": {
                "total": total_documents,
                "verified": verified_documents,
                "verification_rate": round((verified_documents / total_documents * 100), 2) if total_documents > 0 else 0
            }
        }

    def get_feedback_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get feedback and satisfaction analytics."""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        # Rating distribution
        rating_distribution = self.db.query(
            Feedback.rating,
            func.count(Feedback.id).label('count')
        ).group_by(Feedback.rating).order_by(Feedback.rating).all()
        
        # Service satisfaction comparison
        service_satisfaction = self.db.query(
            Service.name,
            func.avg(Feedback.rating).label('avg_rating'),
            func.count(Feedback.id).label('feedback_count')
        ).join(Appointment).join(Feedback).group_by(
            Service.name
        ).having(
            func.count(Feedback.id) >= 3
        ).order_by(
            func.avg(Feedback.rating).desc()
        ).limit(10).all()
        
        return {
            "rating_distribution": [
                {
                    "rating": stat.rating,
                    "count": stat.count
                }
                for stat in rating_distribution
            ],
            "service_satisfaction": [
                {
                    "service": stat.name,
                    "average_rating": round(stat.avg_rating, 2),
                    "feedback_count": stat.count
                }
                for stat in service_satisfaction
            ]
        }
