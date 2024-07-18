from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.frame_controller import get_video_frames, get_frame, remove_frames
from logger import logger

router = APIRouter(prefix="/videos/{video_id}/frames")


@router.get("/")
def get_frames_paths(video_id: int, db: Session = Depends(get_db)) -> list[str]:
    try:
        frames_paths = get_video_frames(video_id, db)
        logger.info(f"success fetching {len(frames_paths)} frames of video {video_id}")
        return frames_paths
    except Exception as e:
        logger.error(f"error fetching frames of video {video_id}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{frame_index}")
def get_frame_path(video_id: int, frame_index: int, db: Session = Depends(get_db)) -> str:
    try:
        frame_paths = get_frame(video_id, frame_index, db)
        logger.info(f"success fetching frame {frame_index} of video {video_id}")
        return frame_paths
    except Exception as e:
        logger.error(f"error fetching frame {frame_index} of video {video_id}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/threats")
def remove_threat_frames(video_id: int, db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        remove_frames(video_id, db)
        logger.info(f"success removing threat frames of video {video_id} from os")
        return {"message": "Frames removed successfully"}
    except Exception as e:
        logger.error(f"error removing threat frames of video {video_id} from os")
        raise HTTPException(status_code=500, detail=str(e))
