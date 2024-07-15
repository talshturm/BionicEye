from pydantic import BaseModel
from typing import List
from .frame import Frame


class VideoBase(BaseModel):
    observation_point_name: str
    storage_path: str
    frame_count: int


class VideoCreate(VideoBase):
    pass


class Video(VideoBase):
    id: int
    frames: List[Frame] = []

    class Config:
        orm_mode = True
