from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controllers.video_controller import upload_video

router = APIRouter()


@router.post("/videos/upload")
async def upload(local_path: str, db: Session = Depends(get_db)) -> None:
    return await upload_video(local_path, db)
