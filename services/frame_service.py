from boto3 import Session
from utils.process_functions import upload_to_os
from utils.given_functions import is_frame_tagged, generate_metadata
from repositories.frame_repository import create_frame_repo


async def create_frame_service(index: int, frame, video_id: int, db: Session):
    frame_path = upload_to_os(frame, video_id, index)
    metadata_info = generate_metadata(frame)
    tag = is_frame_tagged(frame)

    metadata_data = {
        "tag": tag,
        "fov": metadata_info["fov"],
        "azimuth": metadata_info["azimuth"],
        "elevation": metadata_info["elevation"]
    }
    metadata = create_metadata_repo(metadata_data, db)

    frame_data = {
        "video_id": video_id,
        "storage_path": frame_path,
        "frame_index": index,
        "metadata_id": metadata.id
    }
    create_frame_repo(frame_data, db)
