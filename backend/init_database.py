#!/usr/bin/env python3
"""
Database initialization script for the Government Services Portal.
This script creates sample data for testing and demonstration purposes.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.db import SessionLocal
from app.models import (
    User, Department, Service, TimeSlot, Appointment,
    Document, GovernmentOfficer, Notification, Feedback, AuditLog,
    UserRole, AppointmentStatus, NotificationType
)
from app.services.user_service import UserService
from app.services.department_service import DepartmentService
from app.services.service_service import ServiceService
from app.services.appointment_service import AppointmentService
from app.services.document_service import DocumentService
from app.services.notification_service import NotificationService
from app.services.feedback_service import FeedbackService
from app.utils import get_password_hash

def init_database():
    """Initialize database with sample data."""
    print("🚀 Initializing database with sample data...")
    
    db = SessionLocal()
    try:
        # Create sample departments
        departments = create_sample_departments(db)
        
        # Create sample services
        services = create_sample_services(db, departments)
        
        # Create sample users
        users = create_sample_users(db)
        
        # Create sample government officers
        officers = create_sample_officers(db, users, departments)
        
        # Create sample time slots
        time_slots = create_sample_time_slots(db, services)
        
        # Create sample appointments
        appointments = create_sample_appointments(db, users, services, time_slots)
        
        # Create sample documents
        create_sample_documents(db, users, appointments)
        
        # Create sample notifications
        create_sample_notifications(db, users, appointments)
        
        # Create sample feedback
        create_sample_feedback(db, users, appointments)
        
        print("✅ Database initialization completed successfully!")
        print(f"📊 Created: {len(departments)} departments, {len(services)} services, {len(users)} users")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def create_sample_departments(db):
    """Create sample government departments."""
    print("🏛️  Creating sample departments...")
    
    departments_data = [
        {
            "name": "Department of Motor Traffic",
            "description": "Handles vehicle registration, driving licenses, and traffic management",
            "location": "Colombo 10",
            "contact_number": "+94-11-269-4444",
            "email": "info@dmt.gov.lk",
            "operating_hours": "Monday-Friday: 8:30 AM - 4:30 PM"
        },
        {
            "name": "Department of Immigration & Emigration",
            "description": "Manages passports, visas, and immigration services",
            "location": "Colombo 1",
            "contact_number": "+94-11-532-9000",
            "email": "info@immigration.gov.lk",
            "operating_hours": "Monday-Friday: 8:00 AM - 4:00 PM"
        },
        {
            "name": "Department of Registration of Persons",
            "description": "Handles national ID cards and personal registration",
            "location": "Colombo 2",
            "contact_number": "+94-11-234-5678",
            "email": "info@drp.gov.lk",
            "operating_hours": "Monday-Friday: 8:30 AM - 4:00 PM"
        },
        {
            "name": "Department of Inland Revenue",
            "description": "Manages tax collection and revenue services",
            "location": "Colombo 3",
            "contact_number": "+94-11-218-7000",
            "email": "info@ird.gov.lk",
            "operating_hours": "Monday-Friday: 8:00 AM - 4:30 PM"
        },
        {
            "name": "Department of Labor",
            "description": "Handles employment services and labor regulations",
            "location": "Colombo 5",
            "contact_number": "+94-11-258-7000",
            "email": "info@labor.gov.lk",
            "operating_hours": "Monday-Friday: 8:30 AM - 4:00 PM"
        }
    ]
    
    departments = []
    for dept_data in departments_data:
        dept = Department(**dept_data)
        db.add(dept)
        db.flush()  # Get the ID
        departments.append(dept)
    
    db.commit()
    return departments

def create_sample_services(db, departments):
    """Create sample government services."""
    print("🔧 Creating sample services...")
    
    services_data = [
        # Motor Traffic Department
        {
            "name": "Vehicle Registration",
            "description": "New vehicle registration and transfer of ownership",
            "department_id": departments[0].id,
            "duration_minutes": 45,
            "max_daily_appointments": 20,
            "required_documents": "Vehicle documents, ID copy, proof of address"
        },
        {
            "name": "Driving License Renewal",
            "description": "Renewal of driving license",
            "department_id": departments[0].id,
            "duration_minutes": 30,
            "max_daily_appointments": 30,
            "required_documents": "Old license, ID copy, medical certificate"
        },
        {
            "name": "Learner's Permit",
            "description": "Application for learner's driving permit",
            "department_id": departments[0].id,
            "duration_minutes": 60,
            "max_daily_appointments": 15,
            "required_documents": "ID copy, medical certificate, passport photos"
        },
        
        # Immigration Department
        {
            "name": "Passport Application",
            "description": "New passport application",
            "department_id": departments[1].id,
            "duration_minutes": 90,
            "max_daily_appointments": 25,
            "required_documents": "Birth certificate, ID copy, passport photos, application form"
        },
        {
            "name": "Visa Extension",
            "description": "Extension of tourist/business visa",
            "department_id": departments[1].id,
            "duration_minutes": 60,
            "max_daily_appointments": 20,
            "required_documents": "Current visa, passport, application form, supporting documents"
        },
        
        # Registration Department
        {
            "name": "National ID Application",
            "description": "Application for national identity card",
            "department_id": departments[2].id,
            "duration_minutes": 45,
            "max_daily_appointments": 40,
            "required_documents": "Birth certificate, application form, passport photos"
        },
        {
            "name": "ID Card Renewal",
            "description": "Renewal of expired national ID card",
            "department_id": departments[2].id,
            "duration_minutes": 30,
            "max_daily_appointments": 35,
            "required_documents": "Old ID card, application form, passport photos"
        },
        
        # Inland Revenue Department
        {
            "name": "Tax Registration",
            "description": "Business tax registration",
            "department_id": departments[3].id,
            "duration_minutes": 75,
            "max_daily_appointments": 15,
            "required_documents": "Business registration, ID copy, proof of address, financial statements"
        },
        {
            "name": "Tax Clearance Certificate",
            "description": "Obtain tax clearance certificate",
            "department_id": departments[3].id,
            "duration_minutes": 45,
            "max_daily_appointments": 25,
            "required_documents": "ID copy, tax returns, payment receipts"
        },
        
        # Labor Department
        {
            "name": "Employment Registration",
            "description": "Register for employment services",
            "department_id": departments[4].id,
            "duration_minutes": 30,
            "max_daily_appointments": 30,
            "required_documents": "ID copy, educational certificates, CV"
        },
        {
            "name": "Work Permit Application",
            "description": "Application for work permit",
            "department_id": departments[4].id,
            "duration_minutes": 60,
            "max_daily_appointments": 20,
            "required_documents": "ID copy, job offer letter, employer details, application form"
        }
    ]
    
    services = []
    for service_data in services_data:
        service = Service(**service_data)
        db.add(service)
        db.flush()  # Get the ID
        services.append(service)
    
    db.commit()
    return services

def create_sample_users(db):
    """Create sample users (citizens and officers)."""
    print("👥 Creating sample users...")
    
    # Create admin user
    admin_user = User(
        username="admin",
        email="admin@gov.lk",
        hashed_password=get_password_hash("admin123"),
        first_name="System",
        last_name="Administrator",
        phone_number="+94-11-123-4567",
        national_id="ADMIN001",
        address="Government Complex, Colombo",
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(admin_user)
    
    # Create government officers
    officers_data = [
        {
            "username": "officer1",
            "email": "officer1@dmt.gov.lk",
            "first_name": "Kamal",
            "last_name": "Perera",
            "phone_number": "+94-11-234-5678",
            "national_id": "OFF001",
            "address": "Motor Traffic Department, Colombo 10",
            "role": UserRole.GOVERNMENT_OFFICER
        },
        {
            "username": "officer2",
            "email": "officer2@immigration.gov.lk",
            "first_name": "Nimali",
            "last_name": "Fernando",
            "phone_number": "+94-11-345-6789",
            "national_id": "OFF002",
            "address": "Immigration Department, Colombo 1",
            "role": UserRole.GOVERNMENT_OFFICER
        },
        {
            "username": "officer3",
            "email": "officer3@drp.gov.lk",
            "first_name": "Sunil",
            "last_name": "Silva",
            "phone_number": "+94-11-456-7890",
            "national_id": "OFF003",
            "address": "Registration Department, Colombo 2",
            "role": UserRole.GOVERNMENT_OFFICER
        }
    ]
    
    officers = []
    for officer_data in officers_data:
        officer = User(
            **officer_data,
            hashed_password=get_password_hash("officer123"),
            is_active=True
        )
        db.add(officer)
        officers.append(officer)
    
    # Create citizen users
    citizens_data = [
        {
            "username": "citizen1",
            "email": "citizen1@example.com",
            "first_name": "Anura",
            "last_name": "Bandara",
            "phone_number": "+94-71-123-4567",
            "national_id": "CIT001",
            "address": "123 Main Street, Colombo 4",
            "role": UserRole.CITIZEN
        },
        {
            "username": "citizen2",
            "email": "citizen2@example.com",
            "first_name": "Malini",
            "last_name": "Jayawardena",
            "phone_number": "+94-71-234-5678",
            "national_id": "CIT002",
            "address": "456 Lake Road, Colombo 6",
            "role": UserRole.CITIZEN
        },
        {
            "username": "citizen3",
            "email": "citizen3@example.com",
            "first_name": "Dinesh",
            "last_name": "Wijesinghe",
            "phone_number": "+94-71-345-6789",
            "national_id": "CIT003",
            "address": "789 Hill Street, Colombo 8",
            "role": UserRole.CITIZEN
        },
        {
            "username": "citizen4",
            "email": "citizen4@example.com",
            "first_name": "Priyanka",
            "last_name": "Rajapaksa",
            "phone_number": "+94-71-456-7890",
            "national_id": "CIT004",
            "address": "321 Temple Road, Colombo 10",
            "role": UserRole.CITIZEN
        },
        {
            "username": "citizen5",
            "email": "citizen5@example.com",
            "first_name": "Ranjith",
            "last_name": "Kumarasiri",
            "phone_number": "+94-71-567-8901",
            "national_id": "CIT005",
            "address": "654 Beach Road, Colombo 3",
            "role": UserRole.CITIZEN
        }
    ]
    
    citizens = []
    for citizen_data in citizens_data:
        citizen = User(
            **citizen_data,
            hashed_password=get_password_hash("citizen123"),
            is_active=True
        )
        db.add(citizen)
        citizens.append(citizen)
    
    db.commit()
    return officers + citizens

def create_sample_officers(db, users, departments):
    """Create sample government officer records."""
    print("👨‍💼 Creating sample government officers...")
    
    # Find users with GOVERNMENT_OFFICER role
    officer_users = [u for u in users if u.role == UserRole.GOVERNMENT_OFFICER]
    
    officers_data = [
        {
            "user_id": officer_users[0].id,
            "department_id": departments[0].id,  # Motor Traffic
            "officer_id": "DMT001",
            "designation": "Senior Vehicle Inspector",
            "is_active": True
        },
        {
            "user_id": officer_users[1].id,
            "department_id": departments[1].id,  # Immigration
            "officer_id": "DIE001",
            "designation": "Passport Officer",
            "is_active": True
        },
        {
            "user_id": officer_users[2].id,
            "department_id": departments[2].id,  # Registration
            "officer_id": "DRP001",
            "designation": "Registration Officer",
            "is_active": True
        }
    ]
    
    officers = []
    for officer_data in officers_data:
        officer = GovernmentOfficer(**officer_data)
        db.add(officer)
        officers.append(officer)
    
    db.commit()
    return officers

def create_sample_time_slots(db, services):
    """Create sample time slots for services."""
    print("⏰ Creating sample time slots...")
    
    time_slots = []
    
    # Create time slots for the next 30 days
    start_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    
    for service in services:
        # Create slots for each service
        for day in range(30):
            current_date = start_date + timedelta(days=day)
            
            # Skip weekends
            if current_date.weekday() >= 5:
                continue
            
            # Create morning slots (8:00 AM - 12:00 PM)
            for hour in range(8, 12):
                for minute in [0, 30]:
                    slot = TimeSlot(
                        service_id=service.id,
                        start_time=current_date.replace(hour=hour, minute=minute),
                        end_time=current_date.replace(hour=hour, minute=minute) + timedelta(minutes=service.duration_minutes),
                        is_available=True,
                        max_capacity=3,
                        current_bookings=0
                    )
                    db.add(slot)
                    time_slots.append(slot)
            
            # Create afternoon slots (1:00 PM - 4:00 PM)
            for hour in range(13, 16):
                for minute in [0, 30]:
                    slot = TimeSlot(
                        service_id=service.id,
                        start_time=current_date.replace(hour=hour, minute=minute),
                        end_time=current_date.replace(hour=hour, minute=minute) + timedelta(minutes=service.duration_minutes),
                        is_available=True,
                        max_capacity=3,
                        current_bookings=0
                    )
                    db.add(slot)
                    time_slots.append(slot)
    
    db.commit()
    return time_slots

def create_sample_appointments(db, users, services, time_slots):
    """Create sample appointments."""
    print("📅 Creating sample appointments...")
    
    # Get citizen users
    citizens = [u for u in users if u.role == UserRole.CITIZEN]
    
    appointments = []
    
    # Create some past appointments (completed)
    for i, citizen in enumerate(citizens[:3]):
        service = services[i % len(services)]
        # Find available time slots for this service
        service_slots = [ts for ts in time_slots if ts.service_id == service.id and ts.is_available]
        
        if service_slots:
            slot = service_slots[0]
            appointment = Appointment(
                user_id=citizen.id,
                service_id=service.id,
                time_slot_id=slot.id,
                status=AppointmentStatus.COMPLETED,
                booking_reference=f"REF{i+1:03d}",
                qr_code=f"QR{i+1:03d}",
                notes="Sample completed appointment"
            )
            db.add(appointment)
            appointments.append(appointment)
            
            # Update time slot
            slot.current_bookings += 1
            slot.is_available = slot.current_bookings < slot.max_capacity
    
    # Create some current appointments (pending/confirmed)
    for i, citizen in enumerate(citizens[3:]):
        service = services[(i+3) % len(services)]
        # Find available time slots for this service
        service_slots = [ts for ts in time_slots if ts.service_id == service.id and ts.is_available]
        
        if service_slots:
            slot = service_slots[0]
            status = AppointmentStatus.PENDING if i % 2 == 0 else AppointmentStatus.CONFIRMED
            appointment = Appointment(
                user_id=citizen.id,
                service_id=service.id,
                time_slot_id=slot.id,
                status=status,
                booking_reference=f"REF{i+4:03d}",
                qr_code=f"QR{i+4:03d}",
                notes="Sample current appointment"
            )
            db.add(appointment)
            appointments.append(appointment)
            
            # Update time slot
            slot.current_bookings += 1
            slot.is_available = slot.current_bookings < slot.max_capacity
    
    db.commit()
    return appointments

def create_sample_documents(db, users, appointments):
    """Create sample documents."""
    print("📄 Creating sample documents...")
    
    # Get citizens
    citizens = [u for u in users if u.role == UserRole.CITIZEN]
    
    document_types = ["ID_CARD", "PASSPORT", "BIRTH_CERTIFICATE", "MEDICAL_CERTIFICATE", "APPLICATION_FORM"]
    
    for i, citizen in enumerate(citizens):
        # Create some documents for each citizen
        for j, doc_type in enumerate(document_types[:3]):  # Create 3 documents per citizen
            document = Document(
                user_id=citizen.id,
                appointment_id=appointments[i].id if i < len(appointments) else None,
                document_type=doc_type,
                file_path=f"/uploads/documents/{citizen.id}_{doc_type.lower()}.pdf",
                file_name=f"{doc_type.lower()}_{citizen.username}.pdf",
                file_size=random.randint(100000, 500000),  # 100KB - 500KB
                mime_type="application/pdf",
                is_verified=random.choice([True, False]),
                verification_notes="Sample document for testing" if random.choice([True, False]) else None
            )
            db.add(document)
    
    db.commit()

def create_sample_notifications(db, users, appointments):
    """Create sample notifications."""
    print("🔔 Creating sample notifications...")
    
    # Get citizens
    citizens = [u for u in users if u.role == UserRole.CITIZEN]
    
    notification_types = [NotificationType.APPOINTMENT_CONFIRMATION, NotificationType.REMINDER, NotificationType.STATUS_UPDATE]
    
    for i, citizen in enumerate(citizens):
        # Create some notifications for each citizen
        for j, notif_type in enumerate(notification_types):
            notification = Notification(
                user_id=citizen.id,
                type=notif_type,
                title=f"Sample {notif_type.value}",
                message=f"This is a sample {notif_type.value} notification for {citizen.first_name}",
                is_read=random.choice([True, False]),
                sent_via_email=True,
                sent_via_sms=random.choice([True, False])
            )
            db.add(notification)
    
    db.commit()

def create_sample_feedback(db, users, appointments):
    """Create sample feedback."""
    print("⭐ Creating sample feedback...")
    
    # Get completed appointments
    completed_appointments = [a for a in appointments if a.status == AppointmentStatus.COMPLETED]
    
    for appointment in completed_appointments:
        feedback = Feedback(
            user_id=appointment.user_id,
            appointment_id=appointment.id,
            rating=random.randint(3, 5),  # Good to excellent ratings
            comment=f"Sample feedback for appointment {appointment.booking_reference}. Service was efficient and staff were helpful."
        )
        db.add(feedback)
    
    db.commit()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database initialization for Government Services Portal")
    parser.add_argument("--force", action="store_true", help="Force initialization even if data exists")
    
    args = parser.parse_args()
    
    try:
        init_database()
        print("\n🎉 Database initialization completed successfully!")
        print("\n📋 Sample data created:")
        print("  - 5 Government Departments")
        print("  - 12 Government Services")
        print("  - 9 Users (1 Admin, 3 Officers, 5 Citizens)")
        print("  - Multiple Time Slots")
        print("  - Sample Appointments")
        print("  - Sample Documents")
        print("  - Sample Notifications")
        print("  - Sample Feedback")
        print("\n🔑 Default login credentials:")
        print("  - Admin: admin / admin123")
        print("  - Officers: officer1, officer2, officer3 / officer123")
        print("  - Citizens: citizen1, citizen2, citizen3, citizen4, citizen5 / citizen123")
        
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        sys.exit(1)
