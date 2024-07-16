from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.video_controller import get_video_frames

router = APIRouter()


@router.get("/videos/{video_id}/frames")
def get_frames_paths(video_id: int, db: Session = Depends(get_db)) -> list[str]:
    try:
        frames_paths = get_video_frames(video_id, db)
        return frames_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
