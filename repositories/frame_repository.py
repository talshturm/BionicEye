from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Metadata
from models.frame import Frame
from utils.process_functions import remove_threat_frames_from_os
from logger import logger


async def create_frame_repo(frame_data: dict, db: AsyncSession) -> Frame:
    logger.info(f"trying to upload frame {frame_data["frame_index"]} of video {frame_data["video_id"]}")
    db_frame = Frame(
        video_id=frame_data["video_id"],
        os_path=frame_data["os_path"],
        frame_index=frame_data["frame_index"],
        frame_metadata_id=frame_data["metadata_id"]
    )
    db.add(db_frame)
    await db.commit()
    await db.refresh(db_frame)
    return db_frame


async def get_frame_repo(video: int, frame: int, db: AsyncSession) -> str:
    logger.info(f"trying to fetch frame {frame} of video {video}")
    frame = await db.execute(select(Frame.os_path).filter_by(video_id=video, frame_index=frame))
    return frame.scalar_one_or_none()


async def get_frames_repo(video: int, db: AsyncSession) -> list[str]:
    logger.info(f"Trying to fetch frames of video {video}")
    result = await db.execute(select(Frame.os_path).filter_by(video_id=video))
    frames_paths = result.scalars().all()
    return list(frames_paths)


async def remove_threats_repo(video: int, db: AsyncSession) -> None:
    result = await db.execute(
        select(Frame.os_path)
        .join(Metadata)
        .filter(Frame.video_id == video, Metadata.frame_tag)
    )
    frames = result.scalars().all()
    logger.info(f"Trying to remove {len(frames)} frames of video {video} tagged as threats from OS")
    remove_threat_frames_from_os(list(frames))
