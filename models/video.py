from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    observation_point = Column(String, index=True, nullable=False)
    os_path = Column(String, nullable=False)
    frame_count = Column(Integer, nullable=False)
    frames = relationship("Frame", back_populates="video")