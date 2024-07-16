from sqlalchemy.orm import Session
from services.video_service import upload_video_service, get_paths_service, get_video_path_service


async def upload_video(local_path: str, db: Session) -> dict[str, str]:
    return await upload_video_service(local_path, db)


def get_paths(db: Session) -> list[str]:
    return get_paths_service(db)


def get_video_path(video_id, db: Session) -> str:
    return get_video_path_service(video_id, db)
