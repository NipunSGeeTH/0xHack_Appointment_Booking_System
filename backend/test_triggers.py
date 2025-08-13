#!/usr/bin/env python3
"""
Test script to demonstrate and verify database triggers functionality.
This script shows how triggers automatically maintain data consistency.
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.db import SessionLocal
from app.models import User, Department, Service, Appointment, TimeSlot, UserRole, AppointmentStatus
from app.services.user_service import UserService
from app.services.department_service import DepartmentService
from app.services.service_service import ServiceService
from app.services.appointment_service import AppointmentService

def test_triggers():
    """Test various database triggers to ensure they work correctly."""
    print("🧪 Testing Database Triggers...")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        # Test 1: User Deactivation Trigger
        print("\n1️⃣ Testing User Deactivation Trigger")
        test_user_deactivation_trigger(db)
        
        # Test 2: Department Deactivation Trigger
        print("\n2️⃣ Testing Department Deactivation Trigger")
        test_department_deactivation_trigger(db)
        
        # Test 3: Service Deactivation Trigger
        print("\n3️⃣ Testing Service Deactivation Trigger")
        test_service_deactivation_trigger(db)
        
        # Test 4: Appointment Status Change Trigger
        print("\n4️⃣ Testing Appointment Status Change Trigger")
        test_appointment_status_trigger(db)
        
        print("\n✅ All trigger tests completed!")
        
    except Exception as e:
        print(f"❌ Error testing triggers: {e}")
        db.rollback()
    finally:
        db.close()

def test_user_deactivation_trigger(db):
    """Test user deactivation trigger."""
    print("  👤 Testing user deactivation...")
    
    # Find a citizen user
    user = db.query(User).filter(User.role == UserRole.CITIZEN).first()
    if not user:
        print("    ⚠️  No citizen users found for testing")
        return
    
    print(f"    📋 User: {user.username} (ID: {user.id})")
    print(f"    📊 Active appointments before: {db.query(Appointment).filter(Appointment.user_id == user.id, Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])).count()}")
    
    # Deactivate user
    user.is_active = False
    db.commit()
    
    # Check if appointments were cancelled
    cancelled_appointments = db.query(Appointment).filter(
        Appointment.user_id == user.id, 
        Appointment.status == AppointmentStatus.CANCELLED
    ).count()
    
    print(f"    ✅ Appointments cancelled: {cancelled_appointments}")
    
    # Reactivate user
    user.is_active = True
    db.commit()

def test_department_deactivation_trigger(db):
    """Test department deactivation trigger."""
    print("  🏛️  Testing department deactivation...")
    
    # Find a department
    department = db.query(Department).filter(Department.is_active == True).first()
    if not department:
        print("    ⚠️  No active departments found for testing")
        return
    
    print(f"    📋 Department: {department.name} (ID: {department.id})")
    print(f"    📊 Active services before: {db.query(Service).filter(Service.department_id == department.id, Service.is_active == True).count()}")
    
    # Deactivate department
    department.is_active = False
    db.commit()
    
    # Check if services were deactivated
    deactivated_services = db.query(Service).filter(
        Service.department_id == department.id, 
        Service.is_active == False
    ).count()
    
    print(f"    ✅ Services deactivated: {deactivated_services}")
    
    # Reactivate department
    department.is_active = True
    db.commit()

def test_service_deactivation_trigger(db):
    """Test service deactivation trigger."""
    print("  🔧 Testing service deactivation...")
    
    # Find a service
    service = db.query(Service).filter(Service.is_active == True).first()
    if not service:
        print("    ⚠️  No active services found for testing")
        return
    
    print(f"    📋 Service: {service.name} (ID: {service.id})")
    print(f"    📊 Pending appointments before: {db.query(Appointment).filter(Appointment.service_id == service.id, Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])).count()}")
    
    # Deactivate service
    service.is_active = False
    db.commit()
    
    # Check if appointments were cancelled
    cancelled_appointments = db.query(Appointment).filter(
        Appointment.service_id == service.id, 
        Appointment.status == AppointmentStatus.CANCELLED
    ).count()
    
    print(f"    ✅ Appointments cancelled: {cancelled_appointments}")
    
    # Reactivate service
    service.is_active = True
    db.commit()

def test_appointment_status_trigger(db):
    """Test appointment status change trigger."""
    print("  📅 Testing appointment status change...")
    
    # Find a pending appointment
    appointment = db.query(Appointment).filter(Appointment.status == AppointmentStatus.PENDING).first()
    if not appointment:
        print("    ⚠️  No pending appointments found for testing")
        return
    
    print(f"    📋 Appointment: {appointment.booking_reference} (ID: {appointment.id})")
    
    # Get time slot before change
    time_slot = db.query(TimeSlot).filter(TimeSlot.id == appointment.time_slot_id).first()
    if time_slot:
        print(f"    📊 Time slot capacity before: {time_slot.current_bookings}/{time_slot.max_capacity}")
        
        # Change appointment status to confirmed
        appointment.status = AppointmentStatus.CONFIRMED
        db.commit()
        
        # Refresh time slot
        db.refresh(time_slot)
        print(f"    📊 Time slot capacity after: {time_slot.current_bookings}/{time_slot.max_capacity}")
        
        # Change back to pending
        appointment.status = AppointmentStatus.PENDING
        db.commit()

def show_trigger_status():
    """Show the current status of database triggers."""
    print("\n🔍 Database Trigger Status")
    print("=" * 50)
    
    db = SessionLocal()
    try:
        # Check if triggers exist by looking for their effects
        print("\n📊 Current System Status:")
        
        # Count active users
        active_users = db.query(User).filter(User.is_active == True).count()
        inactive_users = db.query(User).filter(User.is_active == False).count()
        print(f"  👥 Users: {active_users} active, {inactive_users} inactive")
        
        # Count active departments
        active_depts = db.query(Department).filter(Department.is_active == True).count()
        inactive_depts = db.query(Department).filter(Department.is_active == False).count()
        print(f"  🏛️  Departments: {active_depts} active, {inactive_depts} inactive")
        
        # Count active services
        active_services = db.query(Service).filter(Service.is_active == True).count()
        inactive_services = db.query(Service).filter(Service.is_active == False).count()
        print(f"  🔧 Services: {active_services} active, {inactive_services} inactive")
        
        # Count appointments by status
        pending_appts = db.query(Appointment).filter(Appointment.status == AppointmentStatus.PENDING).count()
        confirmed_appts = db.query(Appointment).filter(Appointment.status == AppointmentStatus.CONFIRMED).count()
        cancelled_appts = db.query(Appointment).filter(Appointment.status == AppointmentStatus.CANCELLED).count()
        completed_appts = db.query(Appointment).filter(Appointment.status == AppointmentStatus.COMPLETED).count()
        
        print(f"  📅 Appointments: {pending_appts} pending, {confirmed_appts} confirmed, {cancelled_appts} cancelled, {completed_appts} completed")
        
        # Count time slots
        available_slots = db.query(TimeSlot).filter(TimeSlot.is_available == True).count()
        unavailable_slots = db.query(TimeSlot).filter(TimeSlot.is_available == False).count()
        print(f"  ⏰ Time Slots: {available_slots} available, {unavailable_slots} unavailable")
        
    except Exception as e:
        print(f"❌ Error checking trigger status: {e}")
    finally:
        db.close()

def main():
    """Main function to run trigger tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test database triggers for Government Services Portal")
    parser.add_argument("--status", action="store_true", help="Show current trigger status only")
    parser.add_argument("--test", action="store_true", help="Run trigger tests")
    
    args = parser.parse_args()
    
    if args.status:
        show_trigger_status()
    elif args.test:
        test_triggers()
    else:
        # Default: show status and run tests
        show_trigger_status()
        test_triggers()

if __name__ == "__main__":
    main()
