from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Frame(Base):
    __tablename__ = "frames"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, ForeignKey('videos.id'))
    os_path = Column(String, nullable=False)
    frame_index = Column(Integer, nullable=False)
    metadata_id = Column(Integer, ForeignKey('metadata.id'))

    video = relationship("Video", back_populates="frames")
    metadata = relationship("Metadata", back_populates="frames")
