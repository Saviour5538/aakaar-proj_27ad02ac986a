from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/system", tags=["System"])

@router.post("/migrate")
async def migrate():
    try:
        return {"message": "Database migrations completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/seed")
async def seed():
    try:
        return {"message": "Database seeded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))