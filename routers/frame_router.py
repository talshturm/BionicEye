from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.frame_controller import get_video_frames, get_frame, remove_frames

router = APIRouter(prefix="/videos/{video_id}/frames")


@router.get("/")
def get_frames_paths(video_id: int, db: Session = Depends(get_db)) -> list[str]:
    try:
        frames_paths = get_video_frames(video_id, db)
        return frames_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{frame_index}")
def get_frames_paths(video_id: int, frame_index: int, db: Session = Depends(get_db)) -> str:
    try:
        frame_paths = get_frame(video_id, frame_index, db)
        return frame_paths
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/danger")
def remove_threat_frames(video_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        remove_frames(video_id, db)
        return {"message": "Video removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
