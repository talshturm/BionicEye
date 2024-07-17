from typing import Type
from sqlalchemy.orm import Session
from models.metadata import Metadata
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S',
                    filename='log_file.log',
                    level=logging.INFO)


def create_metadata_repo(tag: bool, fov: float, azimuth: float, elevation: float, db: Session) -> (
        Type[Metadata] | Metadata):
    logger.info("trying to add metadata to db")
    existing_metadata = get_existing_metadata(tag, fov, azimuth, elevation, db)
    if existing_metadata:
        logger.info("metadata already exists")
        return existing_metadata

    metadata = Metadata(frame_tag=tag, fov=fov, azimuth=azimuth, elevation=elevation)
    db.add(metadata)
    db.commit()
    db.refresh(metadata)
    return metadata


def get_existing_metadata(tag: bool, fov: float, azimuth: float, elevation: float, db: Session) -> (
        Type[Metadata] | None):
    return db.query(Metadata).filter_by(frame_tag=tag,
                                        fov=fov,
                                        azimuth=azimuth,
                                        elevation=elevation).first()
