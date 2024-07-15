from sqlalchemy.orm import Session
from models.video import Video


def create_video_repo(video_data: dict, db: Session):
    db_video = Video(
        observation_point=video_data["observation_point"],
        storage_path=video_data["storage_path"],
        frame_count=video_data["frame_count"]
    )
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
