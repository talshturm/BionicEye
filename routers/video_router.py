from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controllers.video_controller import upload_video, get_paths, get_video_path, remove_video
import logging


router = APIRouter(prefix="/videos")

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    filename='log_file.log',
                    level=logging.DEBUG)


@router.post("/{local_path}")
async def upload(local_path: str, db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        await upload_video(local_path, db)
        logger.info(f"success uploading video {local_path}")
        return {"message": "Video processed successfully"}
    except Exception as e:
        logger.error(f"error uploading video {local_path}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_all_paths(db: Session = Depends(get_db)) -> list[str]:
    try:
        video_paths = get_paths(db)
        logger.info(f"success fetching {len(video_paths)} videos")
        return video_paths
    except Exception as e:
        logger.error(f"error fetching videos")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}")
def get_video(video_id: int, db: Session = Depends(get_db)) -> str:
    try:
        video_path = get_video_path(video_id, db)
        logger.info(f"success fetching path of video with id {video_id}")
        return video_path
    except Exception as e:
        logger.error(f"error fetching path of video with id {video_id}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{video_path}")
def remove_video_from_os(video_path: str) -> dict[str, str]:
    try:
        remove_video(video_path)
        logger.info(f"success removing video {video_path} from os")
        return {"message": "Video removed successfully"}
    except Exception as e:
        logger.error(f"error removing video {video_path} from os")
        raise HTTPException(status_code=500, detail=str(e))
