from database import engine, Base
from models import Frame, Metadata, Video
from fastapi import FastAPI

app = FastAPI()
Base.metadata.create_all(bind=engine)
