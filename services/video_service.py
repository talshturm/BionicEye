import os
from sqlalchemy.orm import Session
from repositories.video_repository import create_video_repo, get_paths_repo, get_video_path_repo
from utils.process_functions import extract_frames, upload_video_to_os
from services.frame_service import create_frame_service


async def upload_video_service(local_path: str, db: Session) -> dict[str, str]:
    frames = extract_frames(local_path)
    observation_point = os.path.basename(local_path).split("_")[0]
    frame_count = len(frames)

    video_path = upload_video_to_os(local_path)

    video_data = {
        "observation_point": observation_point,
        "os_path": video_path,
        "frame_count": frame_count
    }

    video = create_video_repo(video_data, db)

    for index, frame in enumerate(frames):
        await create_frame_service(index, frame, video.id, db)

    return {"message": "Video uploaded successfully"}


def get_paths_service(db: Session) -> list[str]:
    return get_paths_repo(db)


def get_video_path_service(video_id, db: Session) -> str:
    return get_video_path_repo(video_id, db)
