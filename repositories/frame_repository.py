from sqlalchemy.orm import Session
from models.frame import Frame


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
