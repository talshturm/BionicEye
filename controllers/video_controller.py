from sqlalchemy.orm import Session
from services.video_service import process_upload


async def upload_video(local_path: str, db: Session):
    return await process_upload(local_path, db)
