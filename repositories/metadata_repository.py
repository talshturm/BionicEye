from typing import Type

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.metadata import Metadata
from logger import logger


async def create_metadata_repo(tag: bool, fov: float, azimuth: float, elevation: float, db: AsyncSession) -> (
        Type[Metadata] | Metadata):
    logger.info("trying to add metadata to db")
    existing_metadata = await get_existing_metadata(tag, fov, azimuth, elevation, db)
    if existing_metadata:
        logger.info("metadata already exists")
        return await existing_metadata

    metadata = Metadata(frame_tag=tag, fov=fov, azimuth=azimuth, elevation=elevation)
    db.add(metadata)
    await db.commit()
    await db.refresh(metadata)
    return metadata


async def get_existing_metadata(tag: bool, fov: float, azimuth: float, elevation: float, db: AsyncSession) -> (
        Type[Metadata] | None):
    metadata = await db.execute(select(Metadata).filter_by(frame_tag=tag,
                                                           fov=fov,
                                                           azimuth=azimuth,
                                                           elevation=elevation))
    return metadata.scalars().first()
