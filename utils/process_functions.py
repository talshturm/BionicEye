import os
from typing import Any
import cv2
import boto3
from botocore.exceptions import NoCredentialsError
from numpy import ndarray

minio_endpoint = 'http://localhost:9000'
minio_access_key = 'talsht'
minio_secret_key = '12345678'

s3 = boto3.client(
    's3',
    endpoint_url=minio_endpoint,
    aws_access_key_id=minio_access_key,
    aws_secret_access_key=minio_secret_key,
)


def extract_frames(video_path) -> list[ndarray | Any]:
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    frames = []
    while success:
        frames.append(image)
        success, image = vidcap.read()
    return frames


def upload_frame_to_os(frame, video_id, frame_index) -> str:
    bucket_name = 'frames'

    frame_path = f"{video_id}_{frame_index}.jpg"
    local_path = f"temp/{video_id}_{frame_index}.jpg"
    cv2.imwrite(local_path, frame)
    try:
        s3.upload_file(local_path, bucket_name, frame_path)
    except NoCredentialsError:
        return "upload failed"
    finally:
        os.remove(local_path)
    return f"frames/{frame_path}"


def upload_video_to_os(video_path) -> str:
    bucket_name = 'videos'

    try:
        s3.upload_file(video_path, bucket_name, video_path)
    except NoCredentialsError:
        return "upload failed"

    return f"videos/{video_path}"


def remove_video_from_os(video_path) -> str:
    bucket_name = 'videos'

    try:
        s3.delete_object(Bucket=bucket_name, Key=video_path)
    except NoCredentialsError:
        raise NoCredentialsError
    return "removal succeeded"
