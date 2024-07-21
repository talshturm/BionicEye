from sqlalchemy.ext.asyncio import AsyncSession
from services.video_service import upload_video_service, get_paths_service, get_video_path_service, remove_video_service


async def upload_video(local_path: str, db: AsyncSession) -> dict[str, str]:
    return await upload_video_service(local_path, db)


async def get_paths(db: AsyncSession) -> list[str]:
    return await get_paths_service(db)


async def get_video_path(video_id: int, db: AsyncSession) -> str:
    return await get_video_path_service(video_id, db)


async def remove_video(video_path: str) -> None:
    await remove_video_service(video_path)
