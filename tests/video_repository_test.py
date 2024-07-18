import pytest
from sqlalchemy.exc import IntegrityError

from models import Video
from test_database import db_session, db_engine
from repositories.video_repository import create_video_repo, get_video_path_repo


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
    except IntegrityError:
        db_session.rollback()


@pytest.mark.xfail
def test_create_video_missing_field(db_session):
    video = {
        "observation_point": 'TelAviv',
        "os_path": 'videos/TelAviv_15_06_34_12_06_00.mp4'
    }

    try:
        create_video_repo(video, db_session)
    except KeyError:
        db_session.rollback()


def test_get_video_path_valid_input(db_session):
    video_id = 1
    expected = "videos/TelAviv_15_06_34_12_06_00.mp4"

    actual = get_video_path_repo(video_id, db_session)

    assert expected == actual


@pytest.mark.xfail
def test_get_video_path_null_value(db_session):
    video_id = None

    try:
        get_video_path_repo(video_id, db_session)
    except TypeError:
        db_session.rollback()


@pytest.mark.xfail
def test_get_video_path_non_existing_video(db_session):
    video_id = 7

    try:
        get_video_path_repo(video_id, db_session)
    except TypeError:
        db_session.rollback()
