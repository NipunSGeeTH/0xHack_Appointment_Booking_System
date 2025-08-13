from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from datetime import datetime, timedelta
from .middleware.custom_middleware import CustomMiddleware
from .controllers import (
    user_controller, appointment_controller, department_controller,
    service_controller, document_controller, notification_controller,
    feedback_controller, analytics_controller
)

app = FastAPI(
    title="Sri Lankan Government Services Portal API",
    description="A comprehensive API for managing government service appointments and citizen services",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add built-in CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add custom middleware
app.add_middleware(CustomMiddleware)

# Mount static files for document uploads
uploads_dir = os.path.join(os.path.dirname(__file__), "..", "uploads")
if os.path.exists(uploads_dir):
    app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

# Include all routers
app.include_router(user_controller.router, prefix="/api/v1")
app.include_router(appointment_controller.router, prefix="/api/v1")
app.include_router(department_controller.router, prefix="/api/v1")
app.include_router(service_controller.router, prefix="/api/v1")
app.include_router(document_controller.router, prefix="/api/v1")
app.include_router(notification_controller.router, prefix="/api/v1")
app.include_router(feedback_controller.router, prefix="/api/v1")
app.include_router(analytics_controller.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Sri Lankan Government Services Portal API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "government-services-portal"}

@app.get("/api/v1/info")
async def api_info():
    """API information endpoint."""
    return {
        "name": "Sri Lankan Government Services Portal API",
        "version": "1.0.0",
        "description": "Comprehensive API for government service management",
        "endpoints": {
            "users": "/api/v1/users",
            "appointments": "/api/v1/appointments",
            "departments": "/api/v1/departments",
            "services": "/api/v1/services",
            "documents": "/api/v1/documents",
            "notifications": "/api/v1/notifications",
            "feedback": "/api/v1/feedback",
            "analytics": "/api/v1/analytics"
        }
    }