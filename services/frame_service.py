from sqlalchemy.orm import Session
from repositories.metadata_repository import create_metadata_repo
from utils import generate_metadata, is_frame_tagged
from utils.process_functions import upload_frame_to_os
from repositories.frame_repository import create_frame_repo, get_frames_repo, get_frame_repo


async def create_frame_service(index: int, frame, video_id: int, db: Session) -> None:
    frame_path = upload_frame_to_os(frame, video_id, index)

    fov, azimuth, elevation = generate_metadata(frame)
    tag = is_frame_tagged(frame)

    metadata = create_metadata_repo(tag, fov, azimuth, elevation, db)

    frame_data = {
        "video_id": video_id,
        "os_path": frame_path,
        "frame_index": index,
        "metadata_id": metadata.id
    }
    create_frame_repo(frame_data, db)


def get_frames_service(video_id: int, db: Session) -> list[str]:
    return get_frames_repo(video_id, db)


def get_frame_service(video_id: int, frame_index: int, db: Session) -> str:
    return get_frame_repo(video_id, frame_index, db)
