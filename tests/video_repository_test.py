import pytest
from models import Video
from test_database import db_session, db_engine
from repositories.video_repository import create_video_repo


def test_create_video_valid(db_session):
    valid_video = {
        "observation_point": 'TelAviv',
        "os_path": 'videos/TelAviv_15_06_34_12_06_00.mp4',
        "frame_count": 467
    }

    create_video_repo(valid_video, db_session)

    video = db_session.query(Video).filter_by(os_path="videos/TelAviv_15_06_34_12_06_00.mp4").first()

    assert (video.observation_point == 'TelAviv' and video.os_path == "videos/TelAviv_15_06_34_12_06_00.mp4" and
            video.frame_count == 467)


@pytest.mark.xfail
def test_create_video_null_value(db_session):
    video = {
        "observation_point": 'TelAviv',
        "os_path": 'videos/TelAviv_15_06_34_12_06_00.mp4',
        "frame_count": None
    }

    try:
        create_video_repo(video, db_session)
    except Exception:
        db_session.rollback()


@pytest.mark.xfail
def test_create_video_missing_field(db_session):
    video = {
        "observation_point": 'TelAviv',
        "os_path": 'videos/TelAviv_15_06_34_12_06_00.mp4'
    }

    try:
        create_video_repo(video, db_session)
    except Exception:
        db_session.rollback()
