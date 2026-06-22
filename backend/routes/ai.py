from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from database.models import Query, QuerySource
from database.config import get_db
from backend.services.auth_service import get_current_user
from backend.services.ai_service import (
    ingest_documents_service,
    query_service,
)

router = APIRouter(prefix="/ai", tags=["AI"])

# Pydantic Schemas
class QueryBase(BaseModel):
    question: str
    answer: str
    created_at: datetime

class QueryResponse(QueryBase):
    id: UUID
    user_id: UUID
    session_id: UUID

class QueryCreate(BaseModel):
    question: str

class QuerySourceResponse(BaseModel):
    id: UUID
    query_id: UUID
    chunk_id: UUID
    similarity_score: float

# Routes
@router.post("/ingest")
async def ingest_documents(
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    try:
        await ingest_documents_service(db, current_user)
        return {"message": "Documents ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def ai_query(
    query: QueryCreate,
    top_k: int = Form(5),
    db: Session = Depends(get_db),
    current_user: UUID = Depends(get_current_user),
):
    try:
        response = await query_service(query, top_k, db, current_user)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))