from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    os_path = Column(String, nullable=False)
    frame_index = Column(Integer, nullable=False)
    frame_metadata_id = Column(Integer, ForeignKey('metadata.id'))

    video = relationship("Video", back_populates="frames")
    frame_metadata = relationship("Metadata", back_populates="frames")
