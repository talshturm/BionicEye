from sqlalchemy.orm import Session
from services.frame_service import get_frames_service, get_frame_service, remove_threats_service


async def get_video_frames(video_id: int, db: Session) -> list[str]:
    return await get_frames_service(video_id, db)


async def get_frame(video_id: int, frame_index: int, db: Session) -> str:
    return await get_frame_service(video_id, frame_index, db)


async def remove_frames(video_id: int, db: Session) -> None:
    await remove_threats_service(video_id, db)
