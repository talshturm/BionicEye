import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, ProgrammingError
from models import Metadata
from repositories.metadata_repository import create_metadata_repo, get_existing_metadata


@pytest.mark.asyncio
async def test_create_metadata_valid(db_session):
    tag = True
    fov = 8.954
    azimuth = 1.45
    elevation = 78.4

    new_metadata = await create_metadata_repo(tag, fov, azimuth, elevation, db_session)

    result = await db_session.execute(select(Metadata).filter_by(frame_tag=True, fov=8.954, azimuth=1.45, elevation=78.4))
    metadata = result.scalar_one_or_none()

    assert (new_metadata.id == metadata.id)


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_metadata_invalid_value(db_session):
    tag = True
    fov = 'a'
    azimuth = 1.45
    elevation = 78.4

    try:
        await create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    except ProgrammingError:
        await db_session.rollback()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_metadata_null_value(db_session):
    tag = True
    fov = None
    azimuth = 1.45
    elevation = 78.4

    try:
        await create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    except IntegrityError:
        await db_session.rollback()


@pytest.mark.asyncio
async def test_create_metadata_check_duplicates(db_session):
    tag = True
    fov = 8.954
    azimuth = 1.45
    elevation = 78.4

    await create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    await create_metadata_repo(tag, fov, azimuth, elevation, db_session)

    metadata = await db_session.execute(select(Metadata).filter_by(frame_tag=True, fov=8.954, azimuth=1.45, elevation=78.4))

    assert (len(metadata.scalars().all()) == 1)


@pytest.mark.asyncio
async def test_get_existing_metadata_non_existing_data(db_session):
    tag = True
    fov = 10
    azimuth = 1
    elevation = 70

    metadata = await get_existing_metadata(tag, fov, azimuth, elevation, db_session)

    assert metadata is None


@pytest.mark.asyncio
async def test_get_existing_metadata_existing_data(db_session):
    tag = True
    fov = 10
    azimuth = 1
    elevation = 70

    await create_metadata_repo(tag, fov, azimuth, elevation, db_session)
    metadata = await get_existing_metadata(tag, fov, azimuth, elevation, db_session)

    assert metadata


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_existing_metadata_null_value(db_session):
    tag = True
    fov = None
    azimuth = 1
    elevation = 70

    try:
        await get_existing_metadata(tag, fov, azimuth, elevation, db_session)
    except IntegrityError:
        await db_session.rollback()
