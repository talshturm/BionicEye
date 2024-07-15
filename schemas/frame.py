from pydantic import BaseModel


class FrameBase(BaseModel):
    storage_path: str
    frame_index: int


class FrameCreate(FrameBase):
    video_id: int
    frame_metadata_id: int


class Frame(FrameBase):
    id: int
    video_id: int
    frame_metadata_id: int

    class Config:
        orm_mode = True
