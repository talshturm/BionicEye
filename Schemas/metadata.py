from pydantic import BaseModel
from typing import List
from Models.frame import Frame


class MetadataBase(BaseModel):
    tag: str
    fov: float
    azimuth: float
    elevation: float


class MetadataCreate(MetadataBase):
    pass


class Metadata(MetadataBase):
    id: int
    frames: List[Frame] = []

    class Config:
        orm_mode = True
