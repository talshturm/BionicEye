from sqlalchemy.orm import Session
from services.video_service import upload_video_service


async def upload_video(local_path: str, db: Session) -> None:
    return await upload_video_service(local_path, db)
