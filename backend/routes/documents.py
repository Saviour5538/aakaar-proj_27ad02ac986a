from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from database.models import Document
from database.config import get_db
from backend.services.document_service import (
    get_documents_service,
    upload_document_service,
)
from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/documents", tags=["Documents"])

# Pydantic Schemas
class DocumentBase(BaseModel):
    filename: str
    file_type: str
    status: str
    uploaded_at: datetime
    processed_at: Optional[datetime] = None
    error_message: Optional[str] = None

class DocumentResponse(DocumentBase):
    id: UUID
    user_id: UUID
    session_id: UUID

class DocumentCreate(BaseModel):
    filename: str
    file_type: str

# Routes
@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    try:
        documents = await get_documents_service(db, current_user)
        return documents
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile,
    metadata: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    try:
        document = await upload_document_service(file, metadata, db, current_user)
        return document
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))