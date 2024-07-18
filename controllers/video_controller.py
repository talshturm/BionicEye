from sqlalchemy.orm import Session
from services.video_service import upload_video_service, get_paths_service, get_video_path_service, remove_video_service


async def upload_video(local_path: str, db: Session) -> dict[str, str]:
    return await upload_video_service(local_path, db)


async def get_paths(db: Session) -> list[str]:
    return await get_paths_service(db)


async def get_video_path(video_id: int, db: Session) -> str:
    return await get_video_path_service(video_id, db)


async def remove_video(video_path: str) -> None:
    await remove_video_service(video_path)
