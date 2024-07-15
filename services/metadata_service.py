from boto3 import Session

from models import Metadata
from utils.given_functions import is_frame_tagged, generate_metadata
from repositories.frame_repository import create_metadata_repo


async def create_metadata_service(frame, db: Session) -> Metadata:
    metadata_info = generate_metadata(frame)
    tag = is_frame_tagged(frame)

    metadata_data = {
        "tag": tag,
        "fov": metadata_info["fov"],
        "azimuth": metadata_info["azimuth"],
        "elevation": metadata_info["elevation"]
    }
    metadata = create_metadata_repo(metadata_data, db)

    return metadata
