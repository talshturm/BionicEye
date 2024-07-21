from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


async def get_async_engine():
    return engine
