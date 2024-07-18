import pytest
from sqlalchemy.exc import IntegrityError, DataError
from models import Metadata
from test_database import db_session, db_engine
from repositories.metadata_repository import create_metadata_repo, get_existing_metadata


def test_create_metadata_valid(db_session):
    tag = True
    fov = 8.954
    azimuth = 1.45
    elevation = 78.4

    create_metadata_repo(tag, fov, azimuth, elevation, db_session)

    metadata = db_session.query(Metadata).filter_by(frame_tag=True, fov=8.954, azimuth=1.45, elevation=78.4).first()

    assert (metadata.frame_tag, metadata.fov == 8.954, metadata.azimuth == 1.45, metadata.elevation == 78.4)


@pytest.mark.xfail
def test_create_metadata_invalid_value(db_session):
    tag = True
    fov = 'a'
    azimuth = 1.45
    elevation = 78.4

    try:
        create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    except DataError:
        db_session.rollback()


@pytest.mark.xfail
def test_create_metadata_null_value(db_session):
    tag = True
    fov = None
    azimuth = 1.45
    elevation = 78.4

    try:
        create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    except IntegrityError:
        db_session.rollback()


def test_create_metadata_check_duplicates(db_session):
    tag = True
    fov = 8.954
    azimuth = 1.45
    elevation = 78.4

    create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    create_metadata_repo(tag, fov, azimuth, elevation, db_session)

    metadata = db_session.query(Metadata).filter_by(frame_tag=True, fov=8.954, azimuth=1.45, elevation=78.4).all()

    assert (len(metadata) == 1)


def test_get_existing_metadata_non_existing_data(db_session):
    tag = True
    fov = 10
    azimuth = 1
    elevation = 70

    metadata = get_existing_metadata(tag, fov, azimuth, elevation, db_session)

    assert metadata is None


def test_get_existing_metadata_existing_data(db_session):
    tag = True
    fov = 10
    azimuth = 1
    elevation = 70

    create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    metadata = get_existing_metadata(tag, fov, azimuth, elevation, db_session)

    assert metadata


@pytest.mark.xfail
def test_get_existing_metadata_null_value(db_session):
    tag = True
    fov = None
    azimuth = 1
    elevation = 70

    try:
        metadata = get_existing_metadata(tag, fov, azimuth, elevation, db_session)
    except IntegrityError:
        db_session.rollback()
