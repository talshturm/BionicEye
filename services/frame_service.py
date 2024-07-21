from numpy import ndarray
from sqlalchemy.ext.asyncio import AsyncSession
from utils.process_functions import upload_frame_to_os
from repositories.frame_repository import create_frame_repo, get_frames_repo, get_frame_repo, remove_threats_repo
from services.metadata_service import create_metadata_service


async def create_frame_service(index: int, frame: ndarray, video_id: int, db: AsyncSession) -> None:
    frame_path = upload_frame_to_os(frame, video_id, index)

    metadata = await create_metadata_service(frame, db)

    frame_data = {
        "video_id": video_id,
        "os_path": frame_path,
        "frame_index": index,
        "metadata_id": metadata.id
    }
    await create_frame_repo(frame_data, db)


async def get_frames_service(video_id: int, db: AsyncSession) -> list[str]:
    return await get_frames_repo(video_id, db)


async def get_frame_service(video_id: int, frame_index: int, db: AsyncSession) -> str:
    return await get_frame_repo(video_id, frame_index, db)


async def remove_threats_service(video_id: int, db: AsyncSession) -> None:
    await remove_threats_repo(video_id, db)
