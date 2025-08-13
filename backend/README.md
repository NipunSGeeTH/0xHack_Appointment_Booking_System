# Sri Lankan Government Services Portal - Backend API

A comprehensive FastAPI-based backend for managing government service appointments and citizen services in Sri Lanka.

## Features

### 🏛️ Core Functionality
- **Unified Appointment Booking System** - Browse departments, select services, and book appointments
- **Interactive Calendar Interface** - View available time slots and manage bookings
- **QR Code Generation** - Unique booking confirmations with QR codes
- **Citizen Dashboard** - Personal dashboard for managing appointments and documents
- **Document Pre-submission** - Upload and verify required documents
- **Government Officer Interface** - Secure dashboard for managing appointments
- **Automated Notifications** - Email and SMS notifications for appointments
- **Analytics Dashboard** - Data visualization for optimization
- **Feedback System** - Rating and feedback collection

### 🔐 Security Features
- JWT-based authentication
- Role-based access control (Citizen, Government Officer, Admin)
- Secure document uploads
- Input validation and sanitization
- Audit logging

### 📊 Data Management
- PostgreSQL database with SQLAlchemy ORM
- Comprehensive data models
- Efficient querying and pagination
- Data analytics and reporting

## Tech Stack

- **Framework**: FastAPI 0.104.1
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Authentication**: JWT with Passlib
- **File Handling**: FastAPI File uploads
- **Documentation**: Auto-generated OpenAPI/Swagger docs
- **Testing**: Pytest
- **Deployment**: Docker with docker-compose

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis (optional, for caching)
- Docker & Docker Compose (for containerized deployment)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd backend
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the backend directory:
```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/gov_services_db

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email Configuration (for notifications)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=noreply@gov.lk

# SMS Configuration (optional)
SMS_API_KEY=your-sms-api-key
SMS_API_URL=your-sms-api-url

# File Upload
MAX_FILE_SIZE=10485760  # 10MB in bytes
UPLOAD_DIR=uploads
```

### 5. Database Setup
```bash
# Create database
createdb gov_services_db

# Run migrations (if using Alembic)
alembic upgrade head

# Or create tables directly
python create_tables.py
```

#### Database Scripts

The project includes several database management scripts:

- **`create_tables.py`**: Creates all database tables and triggers
- **`init_database.py`**: Populates the database with sample data
- **`database_dump.py`**: Exports database schema and data for backup

#### Creating Database Triggers

The system automatically creates database triggers when you run `create_tables.py`. These triggers ensure:

- **Data Consistency**: When a user is deactivated, related appointments are cancelled
- **Referential Integrity**: Department deactivation cascades to services and officers
- **Automatic Updates**: Time slot capacity updates when appointments change status
- **Audit Logging**: All important changes are automatically logged
- **Document Verification**: Appointment status updates when documents are verified

#### Sample Data

The `init_database.py` script creates:
- 5 Government Departments (Motor Traffic, Immigration, Registration, etc.)
- 12 Government Services (Vehicle Registration, Passport Application, etc.)
- 9 Sample Users (1 Admin, 3 Officers, 5 Citizens)
- Multiple Time Slots for the next 30 days
- Sample Appointments, Documents, Notifications, and Feedback

**Default Login Credentials**:
- **Admin**: `admin` / `admin123`
- **Officers**: `officer1`, `officer2`, `officer3` / `officer123`
- **Citizens**: `citizen1`, `citizen2`, `citizen3`, `citizen4`, `citizen5` / `citizen123`

### 6. Run the Application
```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Docker Deployment

### Using Docker Compose
```bash
# Build and run all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Manual Docker Build
```bash
# Build image
docker build -t gov-services-portal .

# Run container
docker run -p 8000:8000 --env-file .env gov-services-portal
```

## API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`
- **OpenAPI Schema**: `/openapi.json`

### API Endpoints

#### Authentication & Users
- `POST /api/v1/users/register` - User registration
- `POST /api/v1/users/login` - User authentication
- `GET /api/v1/users/me` - Get current user info
- `PUT /api/v1/users/me` - Update user profile

#### Appointments
- `POST /api/v1/appointments/` - Create appointment
- `GET /api/v1/appointments/me` - Get user appointments
- `PUT /api/v1/appointments/{id}` - Update appointment
- `DELETE /api/v1/appointments/{id}` - Cancel appointment

#### Departments
- `GET /api/v1/departments/` - List all departments
- `GET /api/v1/departments/{id}` - Get department details
- `GET /api/v1/departments/{id}/services` - Get department services

#### Services
- `GET /api/v1/services/` - List all services
- `GET /api/v1/services/{id}` - Get service details
- `GET /api/v1/services/department/{dept_id}` - Get services by department

#### Documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/me` - Get user documents
- `PUT /api/v1/documents/{id}/verify` - Verify document

#### Notifications
- `GET /api/v1/notifications/me` - Get user notifications
- `PUT /api/v1/notifications/{id}/read` - Mark as read

#### Feedback
- `POST /api/v1/feedback/` - Submit feedback
- `GET /api/v1/feedback/me` - Get user feedback

#### Analytics
- `GET /api/v1/analytics/dashboard/overview` - Dashboard statistics
- `GET /api/v1/analytics/appointments/trends` - Appointment trends

## Database Schema

### Core Entities
- **Users** - Citizens, government officers, and admins
- **Departments** - Government departments
- **Services** - Services offered by departments
- **Appointments** - Booked appointments
- **TimeSlots** - Available time slots
- **Documents** - Uploaded documents
- **Notifications** - System notifications
- **Feedback** - User feedback and ratings
- **AuditLogs** - System audit trail

### Key Relationships
- Users can have multiple appointments
- Services belong to departments
- Appointments are linked to services and time slots
- Documents are associated with users and appointments
- Feedback is linked to appointments

## Security Features

### Authentication
- JWT token-based authentication
- Password hashing with bcrypt
- Token expiration and refresh

### Authorization
- Role-based access control
- Resource-level permissions
- API endpoint protection

### Data Protection
- Input validation and sanitization
- SQL injection prevention
- File upload security
- Audit logging

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_users.py

# Run with verbose output
pytest -v
```

### Test Structure
```
tests/
├── test_users.py
├── test_appointments.py
├── test_departments.py
├── test_services.py
├── test_documents.py
├── test_notifications.py
├── test_feedback.py
└── test_analytics.py
```

## Monitoring & Logging

### Health Checks
- `/health` - Basic health check
- `/api/v1/info` - API information

### Logging
- Structured logging with structlog
- Request/response logging
- Error tracking and monitoring

### Metrics
- Prometheus metrics integration
- Performance monitoring
- Business metrics tracking

## Deployment

### Production Considerations
- Use environment variables for configuration
- Enable HTTPS/TLS
- Configure proper CORS settings
- Set up monitoring and alerting
- Implement rate limiting
- Use production-grade database
- Set up backup and recovery

### Environment Variables
```bash
# Production settings
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=info
DATABASE_URL=postgresql://user:pass@host:port/db
REDIS_URL=redis://localhost:6379
```

## Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Write docstrings for functions
- Keep functions small and focused

## Support & Documentation

### API Documentation
- Interactive API docs at `/docs`
- Comprehensive endpoint descriptions
- Request/response examples
- Error code documentation

### Additional Resources
- Database schema documentation
- Deployment guides
- Troubleshooting guides
- Performance optimization tips

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI community for the excellent framework
- SQLAlchemy team for the ORM
- All contributors and maintainers

---

For more information, please contact the development team or refer to the project documentation.

