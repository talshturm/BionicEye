from database import engine, Base
from models import Frame, Metadata, Video

Base.metadata.create_all(bind=engine)
