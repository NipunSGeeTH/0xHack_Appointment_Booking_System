from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, UploadFile
from typing import Optional, List, Dict, Any
from datetime import datetime
import os
import shutil
from pathlib import Path

from ..models import Document, User, Appointment
from ..schemas import DocumentCreate, DocumentUpdate, DocumentResponse
from ..utils import (
    sanitize_filename, get_file_extension, is_allowed_file_type,
    calculate_file_size_mb, generate_audit_log_data
)

class DocumentService:
    def __init__(self, db: Session):
        self.db = db
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        
        # Allowed file types
        self.allowed_extensions = [
            'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'gif', 'bmp',
            'tiff', 'txt', 'rtf', 'xls', 'xlsx', 'ppt', 'pptx'
        ]
        
        # Maximum file size (10MB)
        self.max_file_size = 10 * 1024 * 1024

    def upload_document(self, user_id: int, file: UploadFile, 
                       document_type: str, appointment_id: Optional[int] = None) -> Document:
        """Upload a new document."""
        # Validate file type
        if not is_allowed_file_type(file.filename, self.allowed_extensions):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
            )
        
        # Validate file size
        if file.size and file.size > self.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size too large. Maximum size: {self.max_file_size // (1024 * 1024)}MB"
            )
        
        # Validate appointment if provided
        if appointment_id:
            appointment = self.db.query(Appointment).filter(
                Appointment.id == appointment_id,
                Appointment.user_id == user_id
            ).first()
            if not appointment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Appointment not found or access denied"
                )
        
        # Create user upload directory
        user_upload_dir = self.upload_dir / str(user_id)
        user_upload_dir.mkdir(exist_ok=True)
        
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        original_filename = sanitize_filename(file.filename)
        file_extension = get_file_extension(original_filename)
        unique_filename = f"{document_type}_{timestamp}_{original_filename}"
        file_path = user_upload_dir / unique_filename
        
        try:
            # Save file to disk
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Create document record
            db_document = Document(
                user_id=user_id,
                appointment_id=appointment_id,
                document_type=document_type,
                file_path=str(file_path),
                file_name=original_filename,
                file_size=file.size,
                mime_type=file.content_type
            )
            
            self.db.add(db_document)
            self.db.commit()
            self.db.refresh(db_document)
            
            return db_document
            
        except Exception as e:
            # Clean up file if database operation fails
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Document upload failed: {str(e)}"
            )

    def get_document_by_id(self, document_id: int) -> Optional[Document]:
        """Get document by ID."""
        return self.db.query(Document).filter(Document.id == document_id).first()

    def get_user_documents(self, user_id: int, appointment_id: Optional[int] = None) -> List[Document]:
        """Get documents for a specific user."""
        query = self.db.query(Document).filter(Document.user_id == user_id)
        if appointment_id:
            query = query.filter(Document.appointment_id == appointment_id)
        return query.order_by(Document.uploaded_at.desc()).all()

    def get_appointment_documents(self, appointment_id: int) -> List[Document]:
        """Get all documents for a specific appointment."""
        return self.db.query(Document).filter(
            Document.appointment_id == appointment_id
        ).order_by(Document.uploaded_at.desc()).all()

    def get_documents_by_type(self, user_id: int, document_type: str) -> List[Document]:
        """Get documents of a specific type for a user."""
        return self.db.query(Document).filter(
            Document.user_id == user_id,
            Document.document_type == document_type
        ).order_by(Document.uploaded_at.desc()).all()

    def update_document(self, document_id: int, document_data: DocumentUpdate) -> Optional[Document]:
        """Update document information."""
        document = self.get_document_by_id(document_id)
        if not document:
            return None
        
        # Update fields if provided
        if document_data.is_verified is not None:
            document.is_verified = document_data.is_verified
            if document_data.is_verified:
                document.verified_at = datetime.utcnow()
        
        if document_data.verification_notes is not None:
            document.verification_notes = document_data.verification_notes
        
        try:
            self.db.commit()
            self.db.refresh(document)
            return document
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Document update failed"
            )

    def verify_document(self, document_id: int, verification_notes: Optional[str] = None) -> bool:
        """Verify a document."""
        document = self.get_document_by_id(document_id)
        if not document:
            return False
        
        document.is_verified = True
        document.verification_notes = verification_notes
        document.verified_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def reject_document(self, document_id: int, rejection_notes: str) -> bool:
        """Reject a document."""
        document = self.get_document_by_id(document_id)
        if not document:
            return False
        
        document.is_verified = False
        document.verification_notes = rejection_notes
        document.verified_at = datetime.utcnow()
        
        try:
            self.db.commit()
            return True
        except IntegrityError:
            self.db.rollback()
            return False

    def delete_document(self, document_id: int, user_id: int) -> bool:
        """Delete a document (only by the user who uploaded it)."""
        document = self.get_document_by_id(document_id)
        if not document:
            return False
        
        if document.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only delete your own documents"
            )
        
        try:
            # Delete file from disk
            file_path = Path(document.file_path)
            if file_path.exists():
                file_path.unlink()
            
            # Delete database record
            self.db.delete(document)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Document deletion failed: {str(e)}"
            )

    def get_document_file_path(self, document_id: int) -> Optional[str]:
        """Get the file path for a document."""
        document = self.get_document_by_id(document_id)
        if not document:
            return None
        
        file_path = Path(document.file_path)
        if not file_path.exists():
            return None
        
        return str(file_path)

    def get_document_statistics(self, user_id: Optional[int] = None) -> Dict[str, Any]:
        """Get document statistics."""
        query = self.db.query(Document)
        if user_id:
            query = query.filter(Document.user_id == user_id)
        
        total_documents = query.count()
        verified_documents = query.filter(Document.is_verified == True).count()
        unverified_documents = query.filter(Document.is_verified == False).count()
        
        # Get document type distribution
        document_types = self.db.query(Document.document_type).distinct().all()
        type_distribution = {}
        for doc_type in document_types:
            count = query.filter(Document.document_type == doc_type[0]).count()
            type_distribution[doc_type[0]] = count
        
        return {
            "total_documents": total_documents,
            "verified_documents": verified_documents,
            "unverified_documents": unverified_documents,
            "verification_rate": (verified_documents / total_documents * 100) if total_documents > 0 else 0,
            "type_distribution": type_distribution
        }

    def search_documents(self, user_id: int, search_term: str = None, 
                        document_type: str = None, is_verified: bool = None) -> List[Document]:
        """Search documents with filters."""
        query = self.db.query(Document).filter(Document.user_id == user_id)
        
        if search_term:
            search_filter = f"%{search_term}%"
            query = query.filter(
                (Document.document_type.ilike(search_filter)) |
                (Document.file_name.ilike(search_filter)) |
                (Document.verification_notes.ilike(search_filter))
            )
        
        if document_type:
            query = query.filter(Document.document_type == document_type)
        
        if is_verified is not None:
            query = query.filter(Document.is_verified == is_verified)
        
        return query.order_by(Document.uploaded_at.desc()).all()

    def get_documents_needing_verification(self, limit: int = 100) -> List[Document]:
        """Get documents that need verification."""
        return self.db.query(Document).filter(
            Document.is_verified == False
        ).order_by(Document.uploaded_at.asc()).limit(limit).all()

    def get_documents_by_date_range(self, user_id: int, start_date: datetime, 
                                  end_date: datetime) -> List[Document]:
        """Get documents uploaded within a date range."""
        return self.db.query(Document).filter(
            Document.user_id == user_id,
            Document.uploaded_at >= start_date,
            Document.uploaded_at <= end_date
        ).order_by(Document.uploaded_at.desc()).all()

    def get_document_types_for_service(self, service_id: int) -> List[str]:
        """Get required document types for a specific service."""
        # This would typically come from the service configuration
        # For now, return common document types
        return [
            "national_id",
            "passport",
            "birth_certificate",
            "marriage_certificate",
            "utility_bill",
            "bank_statement",
            "employment_letter",
            "medical_certificate"
        ]

    def validate_document_requirements(self, appointment_id: int) -> Dict[str, Any]:
        """Validate if all required documents are uploaded for an appointment."""
        appointment = self.db.query(Appointment).filter(Appointment.id == appointment_id).first()
        if not appointment:
            return {"valid": False, "message": "Appointment not found"}
        
        # Get required documents for the service
        required_docs = self.get_document_types_for_service(appointment.service_id)
        
        # Get uploaded documents
        uploaded_docs = self.get_appointment_documents(appointment_id)
        uploaded_types = [doc.document_type for doc in uploaded_docs]
        
        # Check missing documents
        missing_docs = [doc_type for doc_type in required_docs if doc_type not in uploaded_types]
        
        # Check verification status
        unverified_docs = [doc for doc in uploaded_docs if not doc.is_verified]
        
        return {
            "valid": len(missing_docs) == 0 and len(unverified_docs) == 0,
            "required_documents": required_docs,
            "uploaded_documents": uploaded_types,
            "missing_documents": missing_docs,
            "unverified_documents": [doc.document_type for doc in unverified_docs],
            "total_uploaded": len(uploaded_docs),
            "total_verified": len([doc for doc in uploaded_docs if doc.is_verified])
        }
