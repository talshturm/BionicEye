import os
from sqlalchemy.orm import Session
from repositories.video_repository import create_video_repo, get_paths_repo, get_video_path_repo
from utils.process_functions import extract_frames, upload_video_to_os, remove_video_from_os
from services.frame_service import create_frame_service
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    filename='log_file.log',
                    level=logging.DEBUG)


async def upload_video_service(local_path: str, db: Session) -> dict[str, str]:
    frames = extract_frames(local_path)
    observation_point = os.path.basename(local_path).split("_")[0]
    frame_count = len(frames)

    video_path = upload_video_to_os(local_path)
    logger.info(f"video of observation point: {observation_point} uploaded to os")

    video_data = {
        "observation_point": observation_point,
        "os_path": video_path,
        "frame_count": frame_count
    }

    video = create_video_repo(video_data, db)

    for index, frame in enumerate(frames):
        await create_frame_service(index, frame, video.id, db)

    logger.info("frames added to os")

    return {"message": "Video uploaded successfully"}


def get_paths_service(db: Session) -> list[str]:
    return get_paths_repo(db)


def get_video_path_service(video_id: int, db: Session) -> str:
    return get_video_path_repo(video_id, db)


def remove_video_service(video_path: str) -> None:
    remove_video_from_os(video_path)
