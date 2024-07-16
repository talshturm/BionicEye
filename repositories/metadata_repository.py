from typing import Type

from sqlalchemy.orm import Session

from models import Metadata
from models.metadata import Metadata


def create_metadata_repo(tag: bool, fov: float, azimuth: float, elevation: float, db: Session) -> Type[
                                                                                                      Metadata] | Metadata:
    existing_metadata = get_existing_metadata(tag, fov, azimuth, elevation, db)
    if existing_metadata:
        return existing_metadata

    metadata = Metadata(frame_tag=tag, fov=fov, azimuth=azimuth, elevation=elevation)
    db.add(metadata)
    db.commit()
    db.refresh(metadata)
    return metadata


def get_existing_metadata(tag: bool, fov: float, azimuth: float, elevation: float, db: Session) -> Type[
                                                                                                       Metadata] | None:
    return db.query(Metadata).filter_by(frame_tag=tag,
                                        fov=fov,
                                        azimuth=azimuth,
                                        elevation=elevation).first()
