from sqlalchemy.orm import Session
from services.frame_service import get_frames_service, get_frame_service


def get_video_frames(video_id: int, db: Session) -> list[str]:
    return get_frames_service(video_id, db)


def get_frame(video_id: int, frame_index: int, db: Session) -> str:
    return get_frame_service(video_id, frame_index, db)