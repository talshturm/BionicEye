from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()


@router.post("/videos/upload")
async def upload_video(local_path: str, db: Session = Depends(get_db)):
    return await upload_video(local_path, db)
