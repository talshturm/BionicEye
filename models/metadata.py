from sqlalchemy import Column, Integer, Boolean, Float
from sqlalchemy.orm import relationship
from database import Base


class Metadata(Base):
    __tablename__ = "metadata"

    id = Column(Integer, primary_key=True, index=True)
    frame_tag = Column(Boolean, nullable=False)
    fov = Column(Float, nullable=False)
    azimuth = Column(Float, nullable=False)

    frames = relationship("Frame", back_populates="frame_metadata")
