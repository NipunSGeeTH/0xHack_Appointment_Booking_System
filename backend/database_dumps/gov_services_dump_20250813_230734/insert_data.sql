-- Government Services Portal Sample Data
-- Generated on: 2025-08-13 23:07:34

BEGIN;

-- Error inserting data into departments: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT departments.id AS departments_id, departments.name AS departments_name, departments.description AS departments_description, departments.location AS departments_location, departments.contact_number AS departments_contact_number, departments.email AS departments_email, departments.operating_hours AS departments_operating_hours, departments.is_active AS departments_is_active, departments.created_at AS departments_created_at, departments.updated_at AS departments_updated_at 
FROM departments]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into services: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT services.id AS services_id, services.name AS services_name, services.description AS services_description, services.department_id AS services_department_id, services.duration_minutes AS services_duration_minutes, services.max_daily_appointments AS services_max_daily_appointments, services.required_documents AS services_required_documents, services.is_active AS services_is_active, services.created_at AS services_created_at, services.updated_at AS services_updated_at 
FROM services]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into users: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT users.id AS users_id, users.username AS users_username, users.email AS users_email, users.hashed_password AS users_hashed_password, users.first_name AS users_first_name, users.last_name AS users_last_name, users.phone_number AS users_phone_number, users.national_id AS users_national_id, users.address AS users_address, users.role AS users_role, users.is_active AS users_is_active, users.created_at AS users_created_at, users.updated_at AS users_updated_at 
FROM users]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into government_officers: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT government_officers.id AS government_officers_id, government_officers.user_id AS government_officers_user_id, government_officers.department_id AS government_officers_department_id, government_officers.officer_id AS government_officers_officer_id, government_officers.designation AS government_officers_designation, government_officers.is_active AS government_officers_is_active, government_officers.created_at AS government_officers_created_at, government_officers.updated_at AS government_officers_updated_at 
FROM government_officers]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into time_slots: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT time_slots.id AS time_slots_id, time_slots.service_id AS time_slots_service_id, time_slots.start_time AS time_slots_start_time, time_slots.end_time AS time_slots_end_time, time_slots.is_available AS time_slots_is_available, time_slots.max_capacity AS time_slots_max_capacity, time_slots.current_bookings AS time_slots_current_bookings, time_slots.created_at AS time_slots_created_at 
FROM time_slots]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into appointments: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT appointments.id AS appointments_id, appointments.user_id AS appointments_user_id, appointments.service_id AS appointments_service_id, appointments.time_slot_id AS appointments_time_slot_id, appointments.status AS appointments_status, appointments.booking_reference AS appointments_booking_reference, appointments.qr_code AS appointments_qr_code, appointments.notes AS appointments_notes, appointments.created_at AS appointments_created_at, appointments.updated_at AS appointments_updated_at 
FROM appointments]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into documents: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT documents.id AS documents_id, documents.user_id AS documents_user_id, documents.appointment_id AS documents_appointment_id, documents.document_type AS documents_document_type, documents.file_path AS documents_file_path, documents.file_name AS documents_file_name, documents.file_size AS documents_file_size, documents.mime_type AS documents_mime_type, documents.is_verified AS documents_is_verified, documents.verification_notes AS documents_verification_notes, documents.uploaded_at AS documents_uploaded_at, documents.verified_at AS documents_verified_at 
FROM documents]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into notifications: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT notifications.id AS notifications_id, notifications.user_id AS notifications_user_id, notifications.type AS notifications_type, notifications.title AS notifications_title, notifications.message AS notifications_message, notifications.is_read AS notifications_is_read, notifications.sent_via_email AS notifications_sent_via_email, notifications.sent_via_sms AS notifications_sent_via_sms, notifications.created_at AS notifications_created_at, notifications.read_at AS notifications_read_at 
FROM notifications]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into feedback: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT feedback.id AS feedback_id, feedback.user_id AS feedback_user_id, feedback.appointment_id AS feedback_appointment_id, feedback.rating AS feedback_rating, feedback.comment AS feedback_comment, feedback.created_at AS feedback_created_at 
FROM feedback]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error inserting data into audit_logs: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT audit_logs.id AS audit_logs_id, audit_logs.user_id AS audit_logs_user_id, audit_logs.action AS audit_logs_action, audit_logs.table_name AS audit_logs_table_name, audit_logs.record_id AS audit_logs_record_id, audit_logs.old_values AS audit_logs_old_values, audit_logs.new_values AS audit_logs_new_values, audit_logs.ip_address AS audit_logs_ip_address, audit_logs.user_agent AS audit_logs_user_agent, audit_logs.created_at AS audit_logs_created_at 
FROM audit_logs]
(Background on this error at: https://sqlalche.me/e/20/2j85)

COMMIT;

-- End of data insertion script