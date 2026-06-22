from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/ui", tags=["UI"])

@router.get("/health")
async def health_check():
    try:
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))