from fastapi import FastAPI
from app.database import engine, Base
from app.models import Books, tags, users

app = FastAPI()
Base.metadata.create_all(bind=engine)
