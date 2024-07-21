import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models import Frame
from repositories.frame_repository import create_frame_repo, get_frame_repo


@pytest.mark.asyncio
async def test_create_frame_valid(db_session):
    valid_frame = {"video_id": 1,
                   "os_path": "frames/1_15",
                   "frame_index": 15,
                   "metadata_id": 13}

    new_frame = await create_frame_repo(valid_frame, db_session)

    result = await db_session.execute(select(Frame).filter_by(os_path="frames/1_15"))
    frame = result.scalar_one_or_none()

    assert (new_frame.id == frame.id)


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_frame_invalid_video(db_session):
    frame = {"video_id": 0,
             "os_path": "frames/0_15",
             "frame_index": 15,
             "metadata_id": 13}

    try:
        await create_frame_repo(frame, db_session)
    except IntegrityError:
        await db_session.rollback()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_frame_invalid_metadata(db_session):
    frame = {"video_id": 1,
             "os_path": "frames/1_15",
             "frame_index": 15,
             "metadata_id": 70}

    try:
        await create_frame_repo(frame, db_session)
    except IntegrityError:
        await db_session.rollback()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_frame_missing_field(db_session):
    frame = {"video_id": 1,
             "frame_index": 15,
             "metadata_id": 13}

    try:
        await create_frame_repo(frame, db_session)
    except KeyError:
        await db_session.rollback()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_frame_null_value(db_session):
    frame = {"video_id": 1,
             "os_path": None,
             "frame_index": 15,
             "metadata_id": 13}

    try:
        await create_frame_repo(frame, db_session)
    except IntegrityError:
        await db_session.rollback()


@pytest.mark.asyncio
async def test_get_frame_valid_input(db_session):
    video_id = 1
    frame_index = 212
    expected_path = "frames/1_212.jpg"

    frame = await get_frame_repo(video_id, frame_index, db_session)

    assert expected_path == frame


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_frame_invalid_input(db_session):
    video_id = 0
    frame_index = 212

    try:
        await get_frame_repo(video_id, frame_index, db_session)
    except TypeError:
        await db_session.rollback()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_frame_non_existing_video(db_session):
    video_id = 10000
    frame_index = 212

    try:
        await get_frame_repo(video_id, frame_index, db_session)
    except TypeError:
        await db_session.rollback()
