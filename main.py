from database import engine, Base
from models import Frame, Metadata, Video
from fastapi import FastAPI
from routers import video_router, frame_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(video_router.router)
app.include_router(frame_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Video Upload API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
