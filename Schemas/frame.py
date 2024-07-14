from pydantic import BaseModel


class FrameBase(BaseModel):
    os_path: str
    frame_index: int


class FrameCreate(FrameBase):
    video_id: int
    metadata_id: int


class Frame(FrameBase):
    id: int
    video_id: int
    metadata_id: int

    class Config:
        orm_mode = True
