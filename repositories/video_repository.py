from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.video import Video
from logger import logger


async def create_video_repo(video_data: dict, db: AsyncSession) -> Video:
    logger.info(f"trying to upload video of observation point {video_data["observation_point"]}")
    db_video = Video(
        observation_point=video_data["observation_point"],
        os_path=video_data["os_path"],
        frame_count=video_data["frame_count"]
    )
    db.add(db_video)
    await db.commit()
    await db.refresh(db_video)
    return db_video


async def get_paths_repo(db: AsyncSession) -> list[str]:
    logger.info("Trying to fetch all video paths")
    result = await db.execute(select(Video.os_path))
    video_paths = result.scalars().all()
    return list(video_paths)


async def get_video_path_repo(video_id: int, db: AsyncSession) -> str:
    logger.info(f"Trying to fetch path of video with id {video_id}")
    result = await db.execute(select(Video.os_path).filter_by(id=video_id))
    video_path = result.scalar_one_or_none()
    if video_path is None:
        raise ValueError(f"Video with id {video_id} not found")
    return video_path
