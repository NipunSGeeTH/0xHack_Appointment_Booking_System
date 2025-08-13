# Database Triggers Summary

## Overview

The Government Services Portal uses comprehensive database triggers to maintain data consistency, referential integrity, and automatic updates across all related tables. These triggers ensure that when one table is updated, all related tables are automatically updated to maintain system consistency.

## 🔧 Trigger Categories

### 1. User Management Triggers

#### `handle_user_deactivation()`
**Triggered by**: `UPDATE` on `users` table
**Purpose**: Maintains data consistency when users are deactivated/reactivated

**Actions**:
- **User Deactivation** (`is_active = FALSE`):
  - Deactivates government officer role
  - Cancels all pending/confirmed appointments
  - Marks all notifications as read
  - Logs the deactivation in audit logs

- **User Reactivation** (`is_active = TRUE`):
  - Reactivates government officer role (if exists)
  - Logs the reactivation in audit logs

**Example**:
```sql
-- When a user is deactivated
UPDATE users SET is_active = FALSE WHERE id = 123;

-- Trigger automatically:
-- 1. Cancels appointments
-- 2. Deactivates officer role
-- 3. Marks notifications as read
-- 4. Logs the action
```

### 2. Department Management Triggers

#### `handle_department_deactivation()`
**Triggered by**: `UPDATE` on `departments` table
**Purpose**: Cascades department status changes to related entities

**Actions**:
- **Department Deactivation** (`is_active = FALSE`):
  - Deactivates all services in the department
  - Deactivates all government officers in the department
  - Cancels all pending/confirmed appointments for services in the department
  - Logs the deactivation

- **Department Reactivation** (`is_active = TRUE`):
  - Reactivates all services in the department
  - Reactivates all government officers in the department
  - Logs the reactivation

**Example**:
```sql
-- When a department is deactivated
UPDATE departments SET is_active = FALSE WHERE id = 456;

-- Trigger automatically:
-- 1. Deactivates all services in department
-- 2. Deactivates all officers in department
-- 3. Cancels related appointments
-- 4. Logs the action
```

### 3. Service Management Triggers

#### `handle_service_deactivation()`
**Triggered by**: `UPDATE` on `services` table
**Purpose**: Manages service deactivation and related cleanup

**Actions**:
- **Service Deactivation** (`is_active = FALSE`):
  - Cancels all pending/confirmed appointments for the service
  - Frees up all time slots for the service
  - Logs the deactivation

- **Service Reactivation** (`is_active = TRUE`):
  - Logs the reactivation

**Example**:
```sql
-- When a service is deactivated
UPDATE services SET is_active = FALSE WHERE id = 789;

-- Trigger automatically:
-- 1. Cancels related appointments
-- 2. Frees up time slots
-- 3. Logs the action
```

### 4. Appointment Management Triggers

#### `handle_appointment_status_change()`
**Triggered by**: `UPDATE` on `appointments` table
**Purpose**: Manages time slot capacity based on appointment status changes

**Actions**:
- **Appointment Cancellation/No-Show**:
  - Decreases time slot current bookings
  - Updates time slot availability
  - Logs the status change

- **Appointment Confirmation**:
  - Increases time slot current bookings
  - Updates time slot availability
  - Logs the status change

**Example**:
```sql
-- When appointment status changes
UPDATE appointments SET status = 'CANCELLED' WHERE id = 101;

-- Trigger automatically:
-- 1. Updates time slot capacity
-- 2. Adjusts availability
-- 3. Logs the change
```

#### `handle_appointment_creation()`
**Triggered by**: `INSERT` on `appointments` table
**Purpose**: Manages time slot capacity when new appointments are created

**Actions**:
- Updates time slot current bookings
- Updates time slot availability
- Logs the appointment creation

**Example**:
```sql
-- When a new appointment is created
INSERT INTO appointments (user_id, service_id, time_slot_id, status) 
VALUES (123, 456, 789, 'PENDING');

-- Trigger automatically:
-- 1. Updates time slot capacity
-- 2. Logs the creation
```

### 5. Document Management Triggers

#### `handle_document_verification()`
**Triggered by**: `UPDATE` on `documents` table
**Purpose**: Manages document verification and appointment status updates

**Actions**:
- **Document Verification**:
  - Logs the verification change
  - Checks if all required documents for an appointment are verified
  - Updates appointment status to 'DOCUMENTS_VERIFIED' if all documents are verified

**Example**:
```sql
-- When a document is verified
UPDATE documents SET is_verified = TRUE WHERE id = 202;

-- Trigger automatically:
-- 1. Logs the verification
-- 2. Checks appointment document status
-- 3. Updates appointment if all documents verified
```

### 6. Notification Management Triggers

#### `handle_notification_read()`
**Triggered by**: `UPDATE` on `notifications` table
**Purpose**: Logs when notifications are marked as read

**Actions**:
- Logs the read action in audit logs when `is_read` changes from `FALSE` to `TRUE`

**Example**:
```sql
-- When a notification is marked as read
UPDATE notifications SET is_read = TRUE WHERE id = 303;

-- Trigger automatically:
-- 1. Logs the read action
```

### 7. Feedback Management Triggers

#### `handle_feedback_creation()`
**Triggered by**: `INSERT` on `feedback` table
**Purpose**: Logs feedback creation for audit purposes

**Actions**:
- Logs the feedback creation in audit logs

**Example**:
```sql
-- When feedback is created
INSERT INTO feedback (user_id, appointment_id, rating, comment) 
VALUES (123, 456, 5, 'Great service!');

-- Trigger automatically:
-- 1. Logs the feedback creation
```

### 8. Audit Logging Triggers

#### `log_user_changes()`
**Triggered by**: `INSERT`, `UPDATE`, `DELETE` on `users` table
**Purpose**: Comprehensive audit logging of all user-related changes

**Actions**:
- **INSERT**: Logs user creation
- **UPDATE**: Logs user modifications
- **DELETE**: Logs user deletion

**Example**:
```sql
-- Any user table change is automatically logged
UPDATE users SET email = 'newemail@example.com' WHERE id = 123;

-- Trigger automatically:
-- 1. Logs the change with old and new values
```

## 🚀 Benefits of These Triggers

### 1. **Data Consistency**
- Ensures related data remains synchronized
- Prevents orphaned records
- Maintains referential integrity

### 2. **Automatic Updates**
- No manual intervention required
- Reduces human error
- Ensures business rules are always enforced

### 3. **Audit Trail**
- Complete history of all changes
- Compliance with government regulations
- Troubleshooting and debugging support

### 4. **Business Logic Enforcement**
- Automatic appointment cancellation when services are deactivated
- Time slot capacity management
- Document verification workflow

### 5. **Performance Optimization**
- Reduces need for complex JOIN queries
- Maintains data integrity at database level
- Efficient cascading updates

## 📋 Trigger Dependencies

The triggers are created in a specific order to handle dependencies:

1. **User Triggers** (base level)
2. **Department Triggers** (depends on users)
3. **Service Triggers** (depends on departments)
4. **Appointment Triggers** (depends on services and users)
5. **Document Triggers** (depends on appointments)
6. **Notification Triggers** (depends on users)
7. **Feedback Triggers** (depends on appointments)
8. **Audit Triggers** (depends on all tables)

## 🧪 Testing Triggers

Use the `test_triggers.py` script to verify trigger functionality:

```bash
# Show current system status
python test_triggers.py --status

# Run trigger tests
python test_triggers.py --test

# Run both (default)
python test_triggers.py
```

## 🔧 Management Commands

### Create All Triggers
```bash
python create_tables.py
```

### Drop All Triggers
```bash
python create_tables.py --drop
```

### Database Dump (includes trigger information)
```bash
python database_dump.py
```

## ⚠️ Important Notes

1. **Trigger Order**: Triggers are executed in the order they were created
2. **Transaction Safety**: All trigger operations are wrapped in transactions
3. **Error Handling**: Triggers include error handling and rollback capabilities
4. **Performance**: Triggers are optimized for minimal performance impact
5. **Logging**: All trigger actions are logged for audit purposes

## 🎯 Use Cases

These triggers are particularly useful for:

- **Government Compliance**: Ensuring data integrity and audit trails
- **Multi-tenant Systems**: Maintaining data consistency across departments
- **Workflow Management**: Automatic status updates and notifications
- **Capacity Management**: Real-time availability tracking
- **Security**: Automatic deactivation of related entities

## 🔮 Future Enhancements

Potential trigger improvements:

1. **Email Notifications**: Automatic email sending on status changes
2. **SMS Alerts**: Real-time SMS notifications for critical changes
3. **Webhook Integration**: External system notifications
4. **Advanced Logging**: More detailed audit information
5. **Performance Monitoring**: Trigger execution time tracking

---

*This document provides a comprehensive overview of all database triggers in the Government Services Portal. For technical implementation details, refer to the `database_triggers.py` file.*
