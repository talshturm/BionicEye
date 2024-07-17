from sqlalchemy.orm import Session
from models.video import Video
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    filename='log_file.log',
                    level=logging.INFO)


def create_video_repo(video_data: dict, db: Session) -> Video:
    logger.info(f"trying to upload video of observation point {video_data["observation_point"]}")
    db_video = Video(
        observation_point=video_data["observation_point"],
        os_path=video_data["os_path"],
        frame_count=video_data["frame_count"]
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def get_paths_repo(db: Session) -> list[str]:
    logger.info("trying to fetch all videos paths")
    video_paths = db.query(Video.os_path).all()
    return [path[0] for path in video_paths]


def get_video_path_repo(video_id, db: Session) -> str:
    logger.info(f"trying to fetch path of video with id {video_id}")
    return db.query(Video.os_path).filter_by(id=video_id).first()[0]
