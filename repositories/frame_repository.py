from sqlalchemy.orm import Session
from models import Metadata
from models.frame import Frame
from utils.process_functions import remove_threat_frames_from_os


def create_frame_repo(frame_data: dict, db: Session) -> Frame:
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


def get_frames_repo(video: int, db: Session) -> list[str]:
    frames_paths = db.query(Frame.os_path).filter_by(video_id=video)
    return [path[0] for path in frames_paths]


def get_frame_repo(video: int, frame: int, db: Session) -> str:
    return db.query(Frame.os_path).filter_by(video_id=video, frame_index=frame).first()[0]


def remove_threats_repo(video: int, db: Session) -> None:
    frames = db.query(Frame.os_path).join(Metadata).filter(Frame.video_id == video, Metadata.frame_tag).all()
    remove_threat_frames_from_os([path[0] for path in frames])
