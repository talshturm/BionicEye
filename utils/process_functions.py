import os
from typing import Any

import cv2
import boto3
from botocore.exceptions import NoCredentialsError
from numpy import ndarray


def extract_frames(video_path) -> list[ndarray | Any]:
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    frames = []
    while success:
        frames.append(image)
        success, image = vidcap.read()
    return frames


def upload_to_os(frame, video_id, frame_index) -> str | None:
    s3 = boto3.client('s3')
    frame_path = f"frames/{video_id}_{frame_index}.jpg"
    local_path = f"temp/{video_id}_{frame_index}.jpg"
    cv2.imwrite(local_path, frame)
    try:
        s3.upload_file(local_path, "frames", frame_path)
    except NoCredentialsError:
        return None
    os.remove(local_path)
    return frame_path
