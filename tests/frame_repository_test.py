import pytest
from sqlalchemy.exc import IntegrityError
from models import Frame
from test_database import db_session, db_engine
from repositories.frame_repository import create_frame_repo, get_frame_repo


def test_create_frame_valid(db_session):
    valid_frame = {"video_id": 1,
                   "os_path": "frames/1_15",
                   "frame_index": 15,
                   "metadata_id": 13}

    create_frame_repo(valid_frame, db_session)

    frame = db_session.query(Frame).filter_by(os_path="frames/1_15").first()

    assert (frame.video_id == 1 and frame.os_path == "frames/1_15" and frame.frame_index == 15 and
            frame.frame_metadata_id == 13)


@pytest.mark.xfail
def test_create_frame_invalid_video(db_session):
    frame = {"video_id": 0,
             "os_path": "frames/0_15",
             "frame_index": 15,
             "metadata_id": 13}

    try:
        create_frame_repo(frame, db_session)
    except IntegrityError:
        db_session.rollback()


@pytest.mark.xfail
def test_create_frame_invalid_metadata(db_session):
    frame = {"video_id": 1,
             "os_path": "frames/1_15",
             "frame_index": 15,
             "metadata_id": 70}

    try:
        create_frame_repo(frame, db_session)
    except IntegrityError:
        db_session.rollback()


@pytest.mark.xfail
def test_create_frame_missing_field(db_session):
    frame = {"video_id": 1,
             "frame_index": 15,
             "metadata_id": 13}

    try:
        create_frame_repo(frame, db_session)
    except KeyError:
        db_session.rollback()


@pytest.mark.xfail
def test_create_frame_null_value(db_session):
    frame = {"video_id": 1,
             "os_path": None,
             "frame_index": 15,
             "metadata_id": 13}

    try:
        create_frame_repo(frame, db_session)
    except IntegrityError:
        db_session.rollback()


def test_get_frame_valid_input(db_session):
    video_id = 1
    frame_index = 212
    expected_path = "frames/1_212.jpg"

    frame = get_frame_repo(video_id, frame_index, db_session)

    assert expected_path == frame


@pytest.mark.xfail
def test_get_frame_invalid_input(db_session):
    video_id = 0
    frame_index = 212

    try:
        frame = get_frame_repo(video_id, frame_index, db_session)
    except TypeError:
        db_session.rollback()


@pytest.mark.xfail
def test_get_frame_non_existing_video(db_session):
    video_id = 4
    frame_index = 212

    try:
        frame = get_frame_repo(video_id, frame_index, db_session)
    except TypeError:
        db_session.rollback()
