from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    observation_point = Column(String, index=True)
    storage_path = Column(String)
    frame_count = Column(Integer)
    frames = relationship("Frame", back_populates="video")