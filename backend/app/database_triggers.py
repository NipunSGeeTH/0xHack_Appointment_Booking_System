#!/usr/bin/env python3
"""
Database triggers for maintaining data consistency and referential integrity.
These triggers automatically update related tables when primary tables are modified.
"""

from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class DatabaseTriggers:
    """Manages database triggers for data consistency."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_all_triggers(self) -> bool:
        """Create all database triggers."""
        try:
            # Create triggers in order of dependency
            self._create_user_triggers()
            self._create_department_triggers()
            self._create_service_triggers()
            self._create_appointment_triggers()
            self._create_document_triggers()
            self._create_notification_triggers()
            self._create_feedback_triggers()
            self._create_audit_triggers()
            
            logger.info("✅ All database triggers created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error creating triggers: {e}")
            return False
    
    def drop_all_triggers(self) -> bool:
        """Drop all database triggers."""
        try:
            # Drop triggers in reverse order
            self._drop_audit_triggers()
            self._drop_feedback_triggers()
            self._drop_notification_triggers()
            self._drop_document_triggers()
            self._drop_appointment_triggers()
            self._drop_service_triggers()
            self._drop_department_triggers()
            self._drop_user_triggers()
            
            logger.info("✅ All database triggers dropped successfully!")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error dropping triggers: {e}")
            return False
    
    def _create_user_triggers(self):
        """Create triggers for user table updates."""
        
        # Trigger to update related tables when user is deactivated
        user_deactivation_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_user_deactivation()
            RETURNS TRIGGER AS $$
            BEGIN
                -- If user is deactivated, update related records
                IF NEW.is_active = FALSE AND OLD.is_active = TRUE THEN
                    -- Deactivate government officer role
                    UPDATE government_officers 
                    SET is_active = FALSE, updated_at = NOW()
                    WHERE user_id = NEW.id;
                    
                    -- Cancel all pending appointments
                    UPDATE appointments 
                    SET status = 'CANCELLED', updated_at = NOW()
                    WHERE user_id = NEW.id AND status IN ('PENDING', 'CONFIRMED');
                    
                    -- Mark all notifications as read
                    UPDATE notifications 
                    SET is_read = TRUE, updated_at = NOW()
                    WHERE user_id = NEW.id AND is_read = FALSE;
                    
                    -- Log the deactivation
                    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, created_at)
                    VALUES (NEW.id, 'USER_DEACTIVATED', 'users', NEW.id, 
                           jsonb_build_object('is_active', OLD.is_active), 
                           jsonb_build_object('is_active', NEW.is_active), NOW());
                END IF;
                
                -- If user is reactivated
                IF NEW.is_active = TRUE AND OLD.is_active = FALSE THEN
                    -- Reactivate government officer role if exists
                    UPDATE government_officers 
                    SET is_active = TRUE, updated_at = NOW()
                    WHERE user_id = NEW.id;
                    
                    -- Log the reactivation
                    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, created_at)
                    VALUES (NEW.id, 'USER_REACTIVATED', 'users', NEW.id, 
                           jsonb_build_object('is_active', OLD.is_active), 
                           jsonb_build_object('is_active', NEW.is_active), NOW());
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the trigger
        user_trigger = text("""
            DROP TRIGGER IF EXISTS user_deactivation_trigger ON users;
            CREATE TRIGGER user_deactivation_trigger
                AFTER UPDATE ON users
                FOR EACH ROW
                EXECUTE FUNCTION handle_user_deactivation();
        """)
        
        self.db.execute(user_deactivation_trigger)
        self.db.execute(user_trigger)
        self.db.commit()
        
        logger.info("✅ User triggers created")
    
    def _create_department_triggers(self):
        """Create triggers for department table updates."""
        
        # Trigger to handle department deactivation
        department_deactivation_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_department_deactivation()
            RETURNS TRIGGER AS $$
            BEGIN
                -- If department is deactivated
                IF NEW.is_active = FALSE AND OLD.is_active = TRUE THEN
                    -- Deactivate all services in the department
                    UPDATE services 
                    SET is_active = FALSE, updated_at = NOW()
                    WHERE department_id = NEW.id;
                    
                    -- Deactivate all government officers in the department
                    UPDATE government_officers 
                    SET is_active = FALSE, updated_at = NOW()
                    WHERE department_id = NEW.id;
                    
                    -- Cancel all pending appointments for services in this department
                    UPDATE appointments 
                    SET status = 'CANCELLED', updated_at = NOW()
                    WHERE service_id IN (
                        SELECT id FROM services WHERE department_id = NEW.id
                    ) AND status IN ('PENDING', 'CONFIRMED');
                    
                    -- Log the deactivation
                    INSERT INTO audit_logs (action, table_name, record_id, old_values, new_values, created_at)
                    VALUES ('DEPARTMENT_DEACTIVATED', 'departments', NEW.id, 
                           jsonb_build_object('is_active', OLD.is_active), 
                           jsonb_build_object('is_active', NEW.is_active), NOW());
                END IF;
                
                -- If department is reactivated
                IF NEW.is_active = TRUE AND OLD.is_active = FALSE THEN
                    -- Reactivate all services in the department
                    UPDATE services 
                    SET is_active = TRUE, updated_at = NOW()
                    WHERE department_id = NEW.id;
                    
                    -- Reactivate all government officers in the department
                    UPDATE government_officers 
                    SET is_active = TRUE, updated_at = NOW()
                    WHERE department_id = NEW.id;
                    
                    -- Log the reactivation
                    INSERT INTO audit_logs (action, table_name, record_id, old_values, new_values, created_at)
                    VALUES ('DEPARTMENT_REACTIVATED', 'departments', NEW.id, 
                           jsonb_build_object('is_active', OLD.is_active), 
                           jsonb_build_object('is_active', NEW.is_active), NOW());
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the trigger
        department_trigger = text("""
            DROP TRIGGER IF EXISTS department_deactivation_trigger ON departments;
            CREATE TRIGGER department_deactivation_trigger
                AFTER UPDATE ON departments
                FOR EACH ROW
                EXECUTE FUNCTION handle_department_deactivation();
        """)
        
        self.db.execute(department_deactivation_trigger)
        self.db.execute(department_trigger)
        self.db.commit()
        
        logger.info("✅ Department triggers created")
    
    def _create_service_triggers(self):
        """Create triggers for service table updates."""
        
        # Trigger to handle service deactivation
        service_deactivation_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_service_deactivation()
            RETURNS TRIGGER AS $$
            BEGIN
                -- If service is deactivated
                IF NEW.is_active = FALSE AND OLD.is_active = TRUE THEN
                    -- Cancel all pending appointments for this service
                    UPDATE appointments 
                    SET status = 'CANCELLED', updated_at = NOW()
                    WHERE service_id = NEW.id AND status IN ('PENDING', 'CONFIRMED');
                    
                    -- Free up all time slots for this service
                    UPDATE time_slots 
                    SET is_available = TRUE, current_bookings = 0, updated_at = NOW()
                    WHERE service_id = NEW.id;
                    
                    -- Log the deactivation
                    INSERT INTO audit_logs (action, table_name, record_id, old_values, new_values, created_at)
                    VALUES ('SERVICE_DEACTIVATED', 'services', NEW.id, 
                           jsonb_build_object('is_active', OLD.is_active), 
                           jsonb_build_object('is_active', NEW.is_active), NOW());
                END IF;
                
                -- If service is reactivated
                IF NEW.is_active = TRUE AND OLD.is_active = FALSE THEN
                    -- Log the reactivation
                    INSERT INTO audit_logs (action, table_name, record_id, old_values, new_values, created_at)
                    VALUES ('SERVICE_REACTIVATED', 'services', NEW.id, 
                           jsonb_build_object('is_active', OLD.is_active), 
                           jsonb_build_object('is_active', NEW.is_active), NOW());
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the trigger
        service_trigger = text("""
            DROP TRIGGER IF EXISTS service_deactivation_trigger ON services;
            CREATE TRIGGER service_deactivation_trigger
                AFTER UPDATE ON services
                FOR EACH ROW
                EXECUTE FUNCTION handle_service_deactivation();
        """)
        
        self.db.execute(service_deactivation_trigger)
        self.db.execute(service_trigger)
        self.db.commit()
        
        logger.info("✅ Service triggers created")
    
    def _create_appointment_triggers(self):
        """Create triggers for appointment table updates."""
        
        # Trigger to handle appointment status changes
        appointment_status_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_appointment_status_change()
            RETURNS TRIGGER AS $$
            BEGIN
                -- If appointment status changes
                IF NEW.status != OLD.status THEN
                    -- Update time slot capacity based on status
                    IF NEW.status = 'CANCELLED' OR NEW.status = 'NO_SHOW' THEN
                        -- Free up the time slot
                        UPDATE time_slots 
                        SET current_bookings = GREATEST(0, current_bookings - 1),
                            is_available = CASE 
                                WHEN current_bookings - 1 <= max_capacity THEN TRUE 
                                ELSE FALSE 
                            END,
                            updated_at = NOW()
                        WHERE id = NEW.time_slot_id;
                        
                    ELSIF NEW.status = 'CONFIRMED' AND OLD.status = 'PENDING' THEN
                        -- Reduce time slot capacity
                        UPDATE time_slots 
                        SET current_bookings = current_bookings + 1,
                            is_available = CASE 
                                WHEN current_bookings + 1 >= max_capacity THEN FALSE 
                                ELSE TRUE 
                            END,
                            updated_at = NOW()
                        WHERE id = NEW.time_slot_id;
                    END IF;
                    
                    -- Log the status change
                    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, created_at)
                    VALUES (NEW.user_id, 'APPOINTMENT_STATUS_CHANGED', 'appointments', NEW.id, 
                           jsonb_build_object('status', OLD.status), 
                           jsonb_build_object('status', NEW.status), NOW());
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Trigger to handle appointment creation
        appointment_creation_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_appointment_creation()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Update time slot capacity when appointment is created
                UPDATE time_slots 
                SET current_bookings = current_bookings + 1,
                    is_available = CASE 
                        WHEN current_bookings + 1 >= max_capacity THEN FALSE 
                        ELSE TRUE 
                    END,
                    updated_at = NOW()
                WHERE id = NEW.time_slot_id;
                
                -- Log the appointment creation
                INSERT INTO audit_logs (user_id, action, table_name, record_id, new_values, created_at)
                VALUES (NEW.user_id, 'APPOINTMENT_CREATED', 'appointments', NEW.id, 
                       jsonb_build_object('service_id', NEW.service_id, 'status', NEW.status), NOW());
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the triggers
        appointment_status_trigger_func = text("""
            DROP TRIGGER IF EXISTS appointment_status_change_trigger ON appointments;
            CREATE TRIGGER appointment_status_change_trigger
                AFTER UPDATE ON appointments
                FOR EACH ROW
                EXECUTE FUNCTION handle_appointment_status_change();
        """)
        
        appointment_creation_trigger_func = text("""
            DROP TRIGGER IF EXISTS appointment_creation_trigger ON appointments;
            CREATE TRIGGER appointment_creation_trigger
                AFTER INSERT ON appointments
                FOR EACH ROW
                EXECUTE FUNCTION handle_appointment_creation();
        """)
        
        self.db.execute(appointment_status_trigger)
        self.db.execute(appointment_creation_trigger)
        self.db.execute(appointment_status_trigger_func)
        self.db.execute(appointment_creation_trigger_func)
        self.db.commit()
        
        logger.info("✅ Appointment triggers created")
    
    def _create_document_triggers(self):
        """Create triggers for document table updates."""
        
        # Trigger to handle document verification
        document_verification_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_document_verification()
            RETURNS TRIGGER AS $$
            BEGIN
                -- If document verification status changes
                IF NEW.is_verified != OLD.is_verified THEN
                    -- Log the verification change
                    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, created_at)
                    VALUES (NEW.user_id, 'DOCUMENT_VERIFICATION_CHANGED', 'documents', NEW.id, 
                           jsonb_build_object('is_verified', OLD.is_verified), 
                           jsonb_build_object('is_verified', NEW.is_verified), NOW());
                    
                    -- If document is verified, check if all required documents for appointment are verified
                    IF NEW.is_verified = TRUE AND NEW.appointment_id IS NOT NULL THEN
                        -- Check if all required documents for this appointment are verified
                        IF NOT EXISTS (
                            SELECT 1 FROM documents d
                            JOIN appointments a ON d.appointment_id = a.id
                            JOIN services s ON a.service_id = s.id
                            WHERE a.id = NEW.appointment_id 
                            AND d.is_verified = FALSE
                        ) THEN
                            -- All documents verified, update appointment status if needed
                            UPDATE appointments 
                            SET status = 'CONFIRMED', updated_at = NOW()
                            WHERE id = NEW.appointment_id AND status = 'PENDING';
                        END IF;
                    END IF;
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the trigger
        document_trigger = text("""
            DROP TRIGGER IF EXISTS document_verification_trigger ON documents;
            CREATE TRIGGER document_verification_trigger
                AFTER UPDATE ON documents
                FOR EACH ROW
                EXECUTE FUNCTION handle_document_verification();
        """)
        
        self.db.execute(document_verification_trigger)
        self.db.execute(document_trigger)
        self.db.commit()
        
        logger.info("✅ Document triggers created")
    
    def _create_notification_triggers(self):
        """Create triggers for notification table updates."""
        
        # Trigger to handle notification read status
        notification_read_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_notification_read()
            RETURNS TRIGGER AS $$
            BEGIN
                -- If notification is marked as read
                IF NEW.is_read = TRUE AND OLD.is_read = FALSE THEN
                    -- Log the read action
                    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, created_at)
                    VALUES (NEW.user_id, 'NOTIFICATION_READ', 'notifications', NEW.id, 
                           jsonb_build_object('is_read', OLD.is_read), 
                           jsonb_build_object('is_read', NEW.is_read), NOW());
                END IF;
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the trigger
        notification_trigger = text("""
            DROP TRIGGER IF EXISTS notification_read_trigger ON notifications;
            CREATE TRIGGER notification_read_trigger
                AFTER UPDATE ON notifications
                FOR EACH ROW
                EXECUTE FUNCTION handle_notification_read();
        """)
        
        self.db.execute(notification_read_trigger)
        self.db.execute(notification_trigger)
        self.db.commit()
        
        logger.info("✅ Notification triggers created")
    
    def _create_feedback_triggers(self):
        """Create triggers for feedback table updates."""
        
        # Trigger to handle feedback creation
        feedback_creation_trigger = text("""
            CREATE OR REPLACE FUNCTION handle_feedback_creation()
            RETURNS TRIGGER AS $$
            BEGIN
                -- Log the feedback creation
                INSERT INTO audit_logs (user_id, action, table_name, record_id, new_values, created_at)
                VALUES (NEW.user_id, 'FEEDBACK_CREATED', 'feedback', NEW.id, 
                       jsonb_build_object('rating', NEW.rating, 'appointment_id', NEW.appointment_id), NOW());
                
                RETURN NEW;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the trigger
        feedback_trigger = text("""
            DROP TRIGGER IF EXISTS feedback_creation_trigger ON feedback;
            CREATE TRIGGER feedback_creation_trigger
                AFTER INSERT ON feedback
                FOR EACH ROW
                EXECUTE FUNCTION handle_feedback_creation();
        """)
        
        self.db.execute(feedback_creation_trigger)
        self.db.execute(feedback_trigger)
        self.db.commit()
        
        logger.info("✅ Feedback triggers created")
    
    def _create_audit_triggers(self):
        """Create triggers for audit logging."""
        
        # Trigger to automatically log user table changes
        user_audit_trigger = text("""
            CREATE OR REPLACE FUNCTION log_user_changes()
            RETURNS TRIGGER AS $$
            BEGIN
                IF TG_OP = 'INSERT' THEN
                    INSERT INTO audit_logs (user_id, action, table_name, record_id, new_values, created_at)
                    VALUES (NEW.id, 'USER_CREATED', TG_TABLE_NAME, NEW.id, to_jsonb(NEW), NOW());
                    RETURN NEW;
                ELSIF TG_OP = 'UPDATE' THEN
                    INSERT INTO audit_logs (user_id, action, table_name, record_id, old_values, new_values, created_at)
                    VALUES (NEW.id, 'USER_UPDATED', TG_TABLE_NAME, NEW.id, to_jsonb(OLD), to_jsonb(NEW), NOW());
                    RETURN NEW;
                ELSIF TG_OP = 'DELETE' THEN
                    INSERT INTO audit_logs (action, table_name, record_id, old_values, created_at)
                    VALUES ('USER_DELETED', TG_TABLE_NAME, OLD.id, to_jsonb(OLD), NOW());
                    RETURN OLD;
                END IF;
                RETURN NULL;
            END;
            $$ LANGUAGE plpgsql;
        """)
        
        # Create the trigger
        user_audit_trigger_func = text("""
            DROP TRIGGER IF EXISTS user_audit_trigger ON users;
            CREATE TRIGGER user_audit_trigger
                AFTER INSERT OR UPDATE OR DELETE ON users
                FOR EACH ROW
                EXECUTE FUNCTION log_user_changes();
        """)
        
        self.db.execute(user_audit_trigger)
        self.db.execute(user_audit_trigger_func)
        self.db.commit()
        
        logger.info("✅ Audit triggers created")
    
    def _drop_user_triggers(self):
        """Drop user-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS user_deactivation_trigger ON users;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_user_deactivation();"))
        self.db.commit()
    
    def _drop_department_triggers(self):
        """Drop department-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS department_deactivation_trigger ON departments;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_department_deactivation();"))
        self.db.commit()
    
    def _drop_service_triggers(self):
        """Drop service-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS service_deactivation_trigger ON services;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_service_deactivation();"))
        self.db.commit()
    
    def _drop_appointment_triggers(self):
        """Drop appointment-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS appointment_status_change_trigger ON appointments;"))
        self.db.execute(text("DROP TRIGGER IF EXISTS appointment_creation_trigger ON appointments;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_appointment_status_change();"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_appointment_creation();"))
        self.db.commit()
    
    def _drop_document_triggers(self):
        """Drop document-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS document_verification_trigger ON documents;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_document_verification();"))
        self.db.commit()
    
    def _drop_notification_triggers(self):
        """Drop notification-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS notification_read_trigger ON notifications;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_notification_read();"))
        self.db.commit()
    
    def _drop_feedback_triggers(self):
        """Drop feedback-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS feedback_creation_trigger ON feedback;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS handle_feedback_creation();"))
        self.db.commit()
    
    def _drop_audit_triggers(self):
        """Drop audit-related triggers."""
        self.db.execute(text("DROP TRIGGER IF EXISTS user_audit_trigger ON users;"))
        self.db.execute(text("DROP FUNCTION IF EXISTS log_user_changes();"))
        self.db.commit()
