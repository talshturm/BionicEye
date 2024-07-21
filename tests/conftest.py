import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/postgres"

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)


@pytest_asyncio.fixture(scope='session')
async def db_engine():
    return engine


@pytest_asyncio.fixture(scope='function')
async def db_session() -> AsyncSession:
    connection = await engine.connect()
    transaction = await connection.begin()

    async with SessionLocal(bind=connection) as session:
        yield session
        await session.rollback()
