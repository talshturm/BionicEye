from typing import List, Any
from sqlalchemy import Column, Row
from sqlalchemy.orm import Session
from models.video import Video


def create_video_repo(video_data: dict, db: Session) -> Video:
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
    video_paths = db.query(Video.os_path).all()
    return [path[0] for path in video_paths]
