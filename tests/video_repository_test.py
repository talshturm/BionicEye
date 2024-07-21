import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from models import Video
from repositories.video_repository import create_video_repo, get_video_path_repo


@pytest.mark.asyncio
async def test_create_video_valid(db_session: AsyncSession):
    valid_video = {
        "observation_point": 'TelAviv',
        "os_path": 'videos/TelAviv_15_06_34_12_06_00.mp4',
        "frame_count": 467
    }
    new_video = await create_video_repo(valid_video, db_session)

    result = await db_session.execute(select(Video).filter_by(id=new_video.id))
    video = result.scalar_one_or_none()

    assert (video.observation_point == 'TelAviv' and video.os_path == "videos/TelAviv_15_06_34_12_06_00.mp4" and
            video.frame_count == 467)


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_video_null_value(db_session: AsyncSession):
    video = {
        "observation_point": 'TelAviv',
        "os_path": 'videos/TelAviv_15_06_34_12_06_00.mp4',
        "frame_count": None
    }

    try:
        await create_video_repo(video, db_session)
    except IntegrityError:
        await db_session.rollback()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_create_video_missing_field(db_session):
    video = {
        "observation_point": 'TelAviv',
        "os_path": 'videos/TelAviv_15_06_34_12_06_00.mp4'
    }

    try:
        await create_video_repo(video, db_session)
    except KeyError:
        await db_session.rollback()


@pytest.mark.asyncio
async def test_get_video_path_valid_input(db_session):
    video_id = 1
    expected = "videos/TelAviv_15_06_34_12_06_00.mp4"

    actual = await get_video_path_repo(video_id, db_session)

    assert expected == actual


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_video_path_null_value(db_session):
    video_id = None

    try:
        await get_video_path_repo(video_id, db_session)
    except ValueError:
        await db_session.rollback()


@pytest.mark.asyncio
@pytest.mark.xfail
async def test_get_video_path_non_existing_video(db_session):
    video_id = 10000

    try:
        await get_video_path_repo(video_id, db_session)
    except ValueError:
        await db_session.rollback()
