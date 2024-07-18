import pytest
from models import Frame
from test_database import db_session, db_engine


def test_create_frame_valid(db_session):

    valid_frame = Frame(video_id=1,
                        os_path="frames/1_15",
                        frame_index=15,
                        frame_metadata_id=13)

    db_session.add(valid_frame)
    db_session.commit()

    frame = db_session.query(Frame).filter_by(os_path="frames/1_15").first()

    assert (frame.video_id == 1 and frame.os_path == "frames/1_15" and frame.frame_index == 15 and
            frame.frame_metadata_id == 13)


@pytest.mark.xfail
def test_create_frame_invalid_video(db_session):
    valid_frame = Frame(video_id=0,
                        os_path="frames/0_15",
                        frame_index=15,
                        frame_metadata_id=13)

    db_session.add(valid_frame)
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()


@pytest.mark.xfail
def test_create_frame_invalid_metadata(db_session):
    valid_frame = Frame(video_id=1,
                        os_path="frames/1_15",
                        frame_index=15,
                        frame_metadata_id=70)

    db_session.add(valid_frame)
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()


@pytest.mark.xfail
def test_create_frame_missing_field(db_session):
    valid_frame = Frame(video_id=1,
                        frame_index=15,
                        frame_metadata_id=12)

    db_session.add(valid_frame)
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()


@pytest.mark.xfail
def test_create_frame_null_value(db_session):
    valid_frame = Frame(video_id=1,
                        os_path=None,
                        frame_index=15,
                        frame_metadata_id=12)

    db_session.add(valid_frame)
    try:
        db_session.commit()
    except Exception:
        db_session.rollback()
