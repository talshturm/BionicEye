from sqlalchemy.orm import Session
from models import Metadata
from utils.given_functions import is_frame_tagged, generate_metadata
from repositories.metadata_repository import create_metadata_repo


async def create_metadata_service(frame, db: Session) -> Metadata:
    fov, azimuth, elevation = generate_metadata(frame)
    tag = is_frame_tagged(frame)

    metadata_data = {
        "tag": tag,
        "fov": fov,
        "azimuth": azimuth,
        "elevation": elevation
    }
    metadata = create_metadata_repo(metadata_data, db)

    return metadata
