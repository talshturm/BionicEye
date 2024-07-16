from database import engine, Base
from models import Frame, Metadata, Video
from fastapi import FastAPI
from routers import video_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(video_router.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Video Upload API"}
