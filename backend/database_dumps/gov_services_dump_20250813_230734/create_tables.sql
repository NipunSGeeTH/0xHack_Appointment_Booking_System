-- Government Services Portal Database Schema
-- Generated on: 2025-08-13 23:07:34

BEGIN;

-- Error getting table definition for time_slots: (psycopg2.errors.UndefinedFunction) function pg_get_tabledef(unknown) does not exist
LINE 1: SELECT pg_get_tabledef('time_slots')
               ^
HINT:  No function matches the given name and argument types. You might need to add explicit type casts.

[SQL: SELECT pg_get_tabledef('time_slots')]
(Background on this error at: https://sqlalche.me/e/20/f405)

-- Error getting table definition for appointments: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('appointments')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for documents: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('documents')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for feedback: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('feedback')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for departments: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('departments')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for services: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('services')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for users: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('users')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for government_officers: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('government_officers')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for notifications: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('notifications')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

-- Error getting table definition for audit_logs: (psycopg2.errors.InFailedSqlTransaction) current transaction is aborted, commands ignored until end of transaction block

[SQL: SELECT pg_get_tabledef('audit_logs')]
(Background on this error at: https://sqlalche.me/e/20/2j85)

COMMIT;

-- End of schema creation script