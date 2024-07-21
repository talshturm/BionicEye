from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from database import get_db
from controllers.video_controller import upload_video, get_paths, get_video_path, remove_video
from logger import logger

router = APIRouter(prefix="/videos")


@router.post("/{local_path}")
async def upload(local_path: str, db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    try:
        await upload_video(local_path, db)
        logger.info(f"success uploading video {local_path}")
        return {"message": "Video processed successfully"}
    except Exception as e:
        logger.error(f"error uploading video {local_path}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
async def get_all_paths(db: AsyncSession = Depends(get_db)) -> list[str]:
    try:
        video_paths = await get_paths(db)
        logger.info(f"success fetching {len(video_paths)} videos")
        return video_paths
    except Exception as e:
        logger.error(f"error fetching videos")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{video_id}")
async def get_video(video_id: int, db: AsyncSession = Depends(get_db)) -> str:
    try:
        video_path = await get_video_path(video_id, db)
        logger.info(f"success fetching path of video with id {video_id}")
        return video_path
    except Exception as e:
        logger.error(f"error fetching path of video with id {video_id}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{video_path}")
async def remove_video_from_os(video_path: str) -> dict[str, str]:
    try:
        await remove_video(video_path)
        logger.info(f"success removing video {video_path} from os")
        return {"message": "Video removed successfully"}
    except Exception as e:
        logger.error(f"error removing video {video_path} from os")
        raise HTTPException(status_code=500, detail=str(e))
