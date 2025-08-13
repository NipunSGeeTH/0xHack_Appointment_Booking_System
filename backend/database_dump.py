#!/usr/bin/env python3
"""
Database dump script for the Government Services Portal.
This script exports database schema and data for backup and documentation purposes.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from sqlalchemy import text, inspect
from sqlalchemy.orm import Session

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from app.db import SessionLocal, engine
from app.models import (
    User, Department, Service, TimeSlot, Appointment,
    Document, GovernmentOfficer, Notification, Feedback, AuditLog
)

class DatabaseDumper:
    """Handles database dumping operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.inspector = inspect(engine)
    
    def create_database_dump(self, output_dir: str = "database_dumps") -> str:
        """Create a comprehensive database dump."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dump_dir = Path(output_dir) / f"gov_services_dump_{timestamp}"
        dump_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📁 Creating database dump in: {dump_dir}")
        
        try:
            # Dump schema
            self._dump_schema(dump_dir)
            
            # Dump data
            self._dump_data(dump_dir)
            
            # Create summary
            self._create_summary(dump_dir)
            
            # Create SQL scripts
            self._create_sql_scripts(dump_dir)
            
            print(f"✅ Database dump completed successfully!")
            print(f"📁 Location: {dump_dir}")
            
            return str(dump_dir)
            
        except Exception as e:
            print(f"❌ Error creating database dump: {e}")
            raise
    
    def _dump_schema(self, dump_dir: Path):
        """Dump database schema information."""
        print("🏗️  Dumping database schema...")
        
        schema_info = {
            "database_name": engine.url.database,
            "tables": {},
            "created_at": datetime.now().isoformat()
        }
        
        # Get all table names
        table_names = self.inspector.get_table_names()
        
        for table_name in table_names:
            table_info = {
                "columns": [],
                "primary_keys": [],
                "foreign_keys": [],
                "indexes": [],
                "constraints": []
            }
            
            # Get column information
            columns = self.inspector.get_columns(table_name)
            for column in columns:
                col_info = {
                    "name": column["name"],
                    "type": str(column["type"]),
                    "nullable": column["nullable"],
                    "default": str(column["default"]) if column["default"] else None,
                    "autoincrement": column.get("autoincrement", False)
                }
                table_info["columns"].append(col_info)
            
            # Get primary key information
            primary_keys = self.inspector.get_pk_constraint(table_name)
            if primary_keys["constrained_columns"]:
                table_info["primary_keys"] = primary_keys["constrained_columns"]
            
            # Get foreign key information
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            for fk in foreign_keys:
                fk_info = {
                    "constrained_columns": fk["constrained_columns"],
                    "referred_table": fk["referred_table"],
                    "referred_columns": fk["referred_columns"],
                    "ondelete": fk.get("ondelete"),
                    "onupdate": fk.get("onupdate")
                }
                table_info["foreign_keys"].append(fk_info)
            
            # Get index information
            indexes = self.inspector.get_indexes(table_name)
            for index in indexes:
                index_info = {
                    "name": index["name"],
                    "columns": index["column_names"],
                    "unique": index["unique"]
                }
                table_info["indexes"].append(index_info)
            
            schema_info["tables"][table_name] = table_info
        
        # Save schema to file
        schema_file = dump_dir / "schema.json"
        with open(schema_file, 'w') as f:
            json.dump(schema_info, f, indent=2, default=str)
        
        print(f"✅ Schema dumped to: {schema_file}")
    
    def _dump_data(self, dump_dir: Path):
        """Dump database data."""
        print("📊 Dumping database data...")
        
        # Define tables to dump (in order of dependency)
        tables_to_dump = [
            ("departments", Department),
            ("services", Service),
            ("users", User),
            ("government_officers", GovernmentOfficer),
            ("time_slots", TimeSlot),
            ("appointments", Appointment),
            ("documents", Document),
            ("notifications", Notification),
            ("feedback", Feedback),
            ("audit_logs", AuditLog)
        ]
        
        data_dump = {
            "exported_at": datetime.now().isoformat(),
            "tables": {}
        }
        
        for table_name, model in tables_to_dump:
            print(f"  📋 Dumping {table_name}...")
            
            try:
                # Get all records from the table
                records = self.db.query(model).all()
                
                table_data = []
                for record in records:
                    # Convert SQLAlchemy object to dictionary
                    record_dict = {}
                    for column in model.__table__.columns:
                        value = getattr(record, column.name)
                        if hasattr(value, 'isoformat'):  # Handle datetime objects
                            value = value.isoformat()
                        record_dict[column.name] = value
                    table_data.append(record_dict)
                
                data_dump["tables"][table_name] = {
                    "count": len(table_data),
                    "data": table_data
                }
                
                print(f"    ✅ {len(table_data)} records exported")
                
            except Exception as e:
                print(f"    ❌ Error dumping {table_name}: {e}")
                data_dump["tables"][table_name] = {
                    "count": 0,
                    "data": [],
                    "error": str(e)
                }
        
        # Save data to file
        data_file = dump_dir / "data.json"
        with open(data_file, 'w') as f:
            json.dump(data_dump, f, indent=2, default=str)
        
        print(f"✅ Data dumped to: {data_file}")
    
    def _create_summary(self, dump_dir: Path):
        """Create a summary of the database dump."""
        print("📋 Creating dump summary...")
        
        # Count records in each table
        table_counts = {}
        total_records = 0
        
        tables_to_count = [
            ("departments", Department),
            ("services", Service),
            ("users", User),
            ("government_officers", GovernmentOfficer),
            ("time_slots", TimeSlot),
            ("appointments", Appointment),
            ("documents", Document),
            ("notifications", Notification),
            ("feedback", Feedback),
            ("audit_logs", AuditLog)
        ]
        
        for table_name, model in tables_to_count:
            try:
                count = self.db.query(model).count()
                table_counts[table_name] = count
                total_records += count
            except Exception as e:
                table_counts[table_name] = 0
        
        summary = {
            "dump_info": {
                "created_at": datetime.now().isoformat(),
                "database_name": engine.url.database,
                "total_tables": len(table_counts),
                "total_records": total_records
            },
            "table_summary": table_counts,
            "files_created": [
                "schema.json - Database schema information",
                "data.json - Database data export",
                "summary.json - This summary file",
                "create_tables.sql - SQL script to recreate tables",
                "insert_data.sql - SQL script to insert sample data"
            ]
        }
        
        # Save summary to file
        summary_file = dump_dir / "summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"✅ Summary created: {summary_file}")
    
    def _create_sql_scripts(self, dump_dir: Path):
        """Create SQL scripts for recreating the database."""
        print("🔧 Creating SQL scripts...")
        
        # Create table creation script
        create_tables_sql = self._generate_create_tables_sql()
        create_file = dump_dir / "create_tables.sql"
        with open(create_file, 'w') as f:
            f.write(create_tables_sql)
        
        # Create data insertion script
        insert_data_sql = self._generate_insert_data_sql()
        insert_file = dump_dir / "insert_data.sql"
        with open(insert_file, 'w') as f:
            f.write(insert_data_sql)
        
        print(f"✅ SQL scripts created: {create_file}, {insert_file}")
    
    def _generate_create_tables_sql(self) -> str:
        """Generate SQL script to create all tables."""
        sql_lines = [
            "-- Government Services Portal Database Schema",
            "-- Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "",
            "BEGIN;",
            ""
        ]
        
        # Get all table names
        table_names = self.inspector.get_table_names()
        
        for table_name in table_names:
            # Get CREATE TABLE statement
            try:
                result = self.db.execute(text(f"SELECT pg_get_tabledef('{table_name}')"))
                create_statement = result.scalar()
                if create_statement:
                    sql_lines.append(f"-- Table: {table_name}")
                    sql_lines.append(create_statement + ";")
                    sql_lines.append("")
            except Exception as e:
                sql_lines.append(f"-- Error getting table definition for {table_name}: {e}")
                sql_lines.append("")
        
        sql_lines.extend([
            "COMMIT;",
            "",
            "-- End of schema creation script"
        ])
        
        return "\n".join(sql_lines)
    
    def _generate_insert_data_sql(self) -> str:
        """Generate SQL script to insert sample data."""
        sql_lines = [
            "-- Government Services Portal Sample Data",
            "-- Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "",
            "BEGIN;",
            ""
        ]
        
        # Get data from tables and generate INSERT statements
        tables_to_insert = [
            ("departments", Department),
            ("services", Service),
            ("users", User),
            ("government_officers", GovernmentOfficer),
            ("time_slots", TimeSlot),
            ("appointments", Appointment),
            ("documents", Document),
            ("notifications", Notification),
            ("feedback", Feedback),
            ("audit_logs", AuditLog)
        ]
        
        for table_name, model in tables_to_insert:
            try:
                records = self.db.query(model).all()
                if records:
                    sql_lines.append(f"-- Inserting data into {table_name}")
                    
                    # Get column names
                    columns = [column.name for column in model.__table__.columns]
                    columns_str = ", ".join(columns)
                    
                    for record in records:
                        values = []
                        for column in columns:
                            value = getattr(record, column)
                            if value is None:
                                values.append("NULL")
                            elif isinstance(value, str):
                                # Escape single quotes
                                escaped_value = value.replace("'", "''")
                                values.append(f"'{escaped_value}'")
                            elif hasattr(value, 'isoformat'):  # datetime
                                values.append(f"'{value.isoformat()}'")
                            else:
                                values.append(str(value))
                        
                        values_str = ", ".join(values)
                        sql_lines.append(f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});")
                    
                    sql_lines.append("")
            except Exception as e:
                sql_lines.append(f"-- Error inserting data into {table_name}: {e}")
                sql_lines.append("")
        
        sql_lines.extend([
            "COMMIT;",
            "",
            "-- End of data insertion script"
        ])
        
        return "\n".join(sql_lines)

def main():
    """Main function to run the database dump."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database dump utility for Government Services Portal")
    parser.add_argument("--output", "-o", default="database_dumps", 
                       help="Output directory for database dumps (default: database_dumps)")
    parser.add_argument("--format", "-f", choices=["json", "sql", "both"], default="both",
                       help="Output format (default: both)")
    
    args = parser.parse_args()
    
    try:
        db = SessionLocal()
        dumper = DatabaseDumper(db)
        
        output_dir = dumper.create_database_dump(args.output)
        
        print(f"\n🎉 Database dump completed successfully!")
        print(f"📁 Output directory: {output_dir}")
        print(f"📋 Files created:")
        
        # List created files
        dump_path = Path(output_dir)
        for file_path in dump_path.glob("*"):
            if file_path.is_file():
                size = file_path.stat().st_size
                print(f"  - {file_path.name} ({size} bytes)")
        
        print(f"\n💡 You can now use these files for:")
        print(f"  - Database backup and restoration")
        print(f"  - Documentation purposes")
        print(f"  - Setting up development environments")
        print(f"  - Database migration")
        
    except Exception as e:
        print(f"❌ Database dump failed: {e}")
        sys.exit(1)
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    main()
