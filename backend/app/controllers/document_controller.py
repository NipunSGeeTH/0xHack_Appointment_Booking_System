from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..db import get_db
from ..models import User
from ..schemas import (
    DocumentCreate, DocumentUpdate, DocumentResponse
)
from ..services.document_service import DocumentService
from ..utils import get_current_active_user, require_role

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    document_type: str = Query(..., description="Type of document"),
    appointment_id: Optional[int] = Query(None, description="Associated appointment ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Upload a new document."""
    document_service = DocumentService(db)
    return document_service.upload_document(
        current_user.id, file, document_type, appointment_id
    )

@router.get("/me", response_model=List[DocumentResponse])
async def get_my_documents(
    appointment_id: Optional[int] = Query(None, description="Filter by appointment ID"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get current user's documents."""
    document_service = DocumentService(db)
    return document_service.get_user_documents(current_user.id, appointment_id)

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get document by ID."""
    document_service = DocumentService(db)
    document = document_service.get_document_by_id(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check if user can access this document
    if document.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return document

@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: int,
    document_data: DocumentUpdate,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Update document (government officers only)."""
    document_service = DocumentService(db)
    updated_document = document_service.update_document(document_id, document_data)
    
    if not updated_document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return updated_document

@router.put("/{document_id}/verify")
async def verify_document(
    document_id: int,
    verification_notes: Optional[str] = None,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Verify a document (government officers only)."""
    document_service = DocumentService(db)
    success = document_service.verify_document(document_id, verification_notes)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"message": "Document verified successfully"}

@router.put("/{document_id}/reject")
async def reject_document(
    document_id: int,
    rejection_notes: str,
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Reject a document (government officers only)."""
    document_service = DocumentService(db)
    success = document_service.reject_document(document_id, rejection_notes)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"message": "Document rejected successfully"}

@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a document."""
    document_service = DocumentService(db)
    success = document_service.delete_document(document_id, current_user.id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return {"message": "Document deleted successfully"}

@router.get("/appointment/{appointment_id}", response_model=List[DocumentResponse])
async def get_appointment_documents(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all documents for a specific appointment."""
    document_service = DocumentService(db)
    return document_service.get_appointment_documents(appointment_id)

@router.get("/type/{document_type}", response_model=List[DocumentResponse])
async def get_documents_by_type(
    document_type: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get documents of a specific type for the current user."""
    document_service = DocumentService(db)
    return document_service.get_documents_by_type(current_user.id, document_type)

@router.get("/search/me")
async def search_my_documents(
    search_term: Optional[str] = Query(None, description="Search term"),
    document_type: Optional[str] = Query(None, description="Filter by document type"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Search current user's documents with filters."""
    document_service = DocumentService(db)
    return document_service.search_documents(
        current_user.id, search_term, document_type, is_verified
    )

@router.get("/needing-verification", response_model=List[DocumentResponse])
async def get_documents_needing_verification(
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get documents that need verification (government officers only)."""
    document_service = DocumentService(db)
    return document_service.get_documents_needing_verification(limit)

@router.get("/statistics/overview")
async def get_document_statistics(
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    current_user: User = Depends(require_role("government_officer")),
    db: Session = Depends(get_db)
):
    """Get document statistics (government officers only)."""
    document_service = DocumentService(db)
    return document_service.get_document_statistics(user_id)

@router.get("/types/required/{service_id}")
async def get_required_document_types(
    service_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get required document types for a specific service."""
    document_service = DocumentService(db)
    return document_service.get_document_types_for_service(service_id)

@router.get("/validation/{appointment_id}")
async def validate_document_requirements(
    appointment_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Validate if all required documents are uploaded for an appointment."""
    document_service = DocumentService(db)
    return document_service.validate_document_requirements(appointment_id)

@router.get("/download/{document_id}")
async def download_document(
    document_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get document file path for download."""
    document_service = DocumentService(db)
    document = document_service.get_document_by_id(document_id)
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Check if user can access this document
    if document.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    file_path = document_service.get_document_file_path(document_id)
    if not file_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document file not found"
        )
    
    return {
        "file_path": file_path,
        "file_name": document.file_name,
        "mime_type": document.mime_type
    }
