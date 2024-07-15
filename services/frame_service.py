from boto3 import Session
from utils.process_functions import upload_to_os
from repositories.frame_repository import create_frame_repo
from metadata_service import create_metadata_service


async def create_frame_service(index: int, frame, video_id: int, db: Session) -> None:
    frame_path = upload_to_os(frame, video_id, index)

    metadata = create_metadata_service(frame, db)

    frame_data = {
        "video_id": video_id,
        "os_path": frame_path,
        "frame_index": index,
        "metadata_id": metadata.id
    }
    create_frame_repo(frame_data, db)
