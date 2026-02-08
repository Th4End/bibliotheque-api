from fastapi import FastAPI
from app.database import engine, Base
from app.models import Books, tags, users
from sqlalchemy import inspect
from app.database import engine

app = FastAPI()
Base.metadata.create_all(bind=engine)
