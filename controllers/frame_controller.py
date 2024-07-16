from sqlalchemy.orm import Session
from services.frame_service import get_frames_service


def get_video_frames(video_id: int, db: Session) -> list[str]:
    return get_frames_service(video_id, db)
