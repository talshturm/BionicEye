import os
from sqlalchemy.ext.asyncio import AsyncSession
from repositories.video_repository import create_video_repo, get_paths_repo, get_video_path_repo
from utils.process_functions import extract_frames, upload_video_to_os, remove_video_from_os
from services.frame_service import create_frame_service
from logger import logger


async def upload_video_service(local_path: str, db: AsyncSession) -> dict[str, str]:
    frames = extract_frames(local_path)
    observation_point = os.path.basename(local_path).split("_")[0]
    frame_count = len(frames)

    video_path = upload_video_to_os(local_path)
    logger.info(f"video of observation point: {observation_point} uploaded to os")

    video_data = {
        "observation_point": observation_point,
        "os_path": video_path,
        "frame_count": frame_count
    }

    video = await create_video_repo(video_data, db)

    for index, frame in enumerate(frames):
        await create_frame_service(index, frame, video.id, db)

    logger.info("frames added to os")

    return {"message": "Video uploaded successfully"}


async def get_paths_service(db: AsyncSession) -> list[str]:
    return await get_paths_repo(db)


async def get_video_path_service(video_id: int, db: AsyncSession) -> str:
    return await get_video_path_repo(video_id, db)


async def remove_video_service(video_path: str) -> None:
    remove_video_from_os(video_path)
