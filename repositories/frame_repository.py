from sqlalchemy.orm import Session
from models import Metadata
from models.frame import Frame
from utils.process_functions import remove_threat_frames_from_os
from logger import logger


async def create_frame_repo(frame_data: dict, db: Session) -> Frame:
    logger.info(f"trying to upload frame {frame_data["frame_index"]} of video {frame_data["video_id"]}")
    db_frame = Frame(
        video_id=frame_data["video_id"],
        os_path=frame_data["os_path"],
        frame_index=frame_data["frame_index"],
        frame_metadata_id=frame_data["metadata_id"]
    )
    db.add(db_frame)
    db.commit()
    db.refresh(db_frame)
    return db_frame


async def get_frames_repo(video: int, db: Session) -> list[str]:
    logger.info(f"trying to fetch frames of video {video}")
    frames_paths = db.query(Frame.os_path).filter_by(video_id=video)
    return [path[0] for path in frames_paths]


async def get_frame_repo(video: int, frame: int, db: Session) -> str:
    logger.info(f"trying to fetch frame {frame} of video {video}")
    return db.query(Frame.os_path).filter_by(video_id=video, frame_index=frame).first()[0]


async def remove_threats_repo(video: int, db: Session) -> None:
    frames = db.query(Frame.os_path).join(Metadata).filter(Frame.video_id == video, Metadata.frame_tag).all()
    logger.info(f"trying to remove {len(frames)} frames tagged as threats of video {video} from os")
    remove_threat_frames_from_os([path[0] for path in frames])
