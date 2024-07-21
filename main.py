from contextlib import asynccontextmanager

from database import engine, Base
from models import Frame, Metadata, Video
from fastapi import FastAPI
from routers import video_router, frame_router

app = FastAPI()

app.include_router(video_router.router)
app.include_router(frame_router.router)


@asynccontextmanager
async def lifespan():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
