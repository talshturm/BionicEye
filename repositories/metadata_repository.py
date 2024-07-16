from sqlalchemy.orm import Session
from models.metadata import Metadata


def create_metadata_repo(metadata_data: dict, db: Session):
    db_metadata = Metadata(
        frame_tag=metadata_data["tag"],
        fov=metadata_data["fov"],
        azimuth=metadata_data["azimuth"],
        elevation=metadata_data["elevation"]
    )
    db.add(db_metadata)
    db.commit()

    db.refresh(db_metadata)
    return db_metadata