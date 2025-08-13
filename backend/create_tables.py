#!/usr/bin/env python3
"""
Script to create all database tables for the Government Services Portal.
Run this script after setting up your database connection.
"""

import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.db import engine, Base
from app.models import (
    User, Department, Service, TimeSlot, Appointment, 
    Document, GovernmentOfficer, Notification, Feedback, AuditLog
)

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        
        # Print table information
        print("\n📋 Created tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"  - {table_name}")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

def drop_tables():
    """Drop all database tables (use with caution!)."""
    print("⚠️  Dropping all database tables...")
    
    try:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully!")
        
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Database table management for Government Services Portal")
    parser.add_argument("--drop", action="store_true", help="Drop all tables before creating")
    
    args = parser.parse_args()
    
    if args.drop:
        print("🔄 Recreating database schema...")
        drop_tables()
        print()
    
    create_tables()
    
    print("\n🎉 Database setup complete!")
    print("You can now run the application with: uvicorn app.main:app --reload")
