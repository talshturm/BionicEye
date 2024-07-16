from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.video_controller import upload_video, get_paths

router = APIRouter()


@router.post("/videos/{local_path}")
async def upload(local_path: str, db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        await upload_video(local_path, db)
        return {"message": "Video processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/videos")
def get_all_paths(db: Session = Depends(get_db)) -> list[str]:
    try:
        video_paths = get_paths(db)
        return video_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
