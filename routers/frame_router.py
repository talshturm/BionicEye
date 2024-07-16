from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.frame_controller import get_video_frames, get_frame

router = APIRouter()


@router.get("/videos/{video_id}/frames")
def get_frames_paths(video_id: int, db: Session = Depends(get_db)) -> list[str]:
    try:
        frames_paths = get_video_frames(video_id, db)
        return frames_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/videos/{video_id}/frames/{frame_index}")
def get_frames_paths(video_id: int, frame_index: int, db: Session = Depends(get_db)) -> str:
    try:
        frame_paths = get_frame(video_id, frame_index, db)
        return frame_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
