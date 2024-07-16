from typing import Dict
from sqlalchemy.orm import Session
from services.video_service import upload_video_service, get_paths_service


async def upload_video(local_path: str, db: Session) -> dict[str, str]:
    return await upload_video_service(local_path, db)


async def get_paths(dc: Session) -> None:
    return await get_paths_service(db)