from sqlalchemy.orm import Session
from models.frame import Frame


def create_frame_repo(frame_data: dict, db: Session):
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
