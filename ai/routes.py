from fastapi import APIRouter, HTTPException, Depends, UploadFile, Form
from pydantic import BaseModel
from typing import Dict
from database.config import get_db
from backend.services.auth_service import get_current_user
from ai.ingest import ingest_document
from ai.rag import answer_question

router = APIRouter(prefix="/api/ai")

# Pydantic models for request and response
class IngestRequest(BaseModel):
    session_id: str
    user_id: int

class QueryRequest(BaseModel):
    query: str
    session_id: str
    user_id: int

class QueryResponse(BaseModel):
    answer: str
    context: Dict[str, str]

@router.post("/ingest")
async def ingest(file: UploadFile, session_id: str = Form(...), user_id: int = Form(...), db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Endpoint to ingest a document into the vector store.
    """
    try:
        # Save the uploaded file temporarily
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Call the ingest_document function
        result = ingest_document(file_path, session_id, user_id)

        # Clean up the temporary file
        import os
        os.remove(file_path)

        return {"status": "success", "details": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest, db=Depends(get_db), current_user=Depends(get_current_user)):
    """
    Endpoint to query the vector store and generate an answer.
    """
    try:
        # Call the answer_question function
        result = answer_question(request.query, request.session_id, request.user_id)

        return QueryResponse(answer=result["answer"], context=result["context"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))