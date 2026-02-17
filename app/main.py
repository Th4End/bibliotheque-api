from fastapi import FastAPI
from app.core.init_admin import create_default_admin
from app.database import Base, engine
from app.routers import auth, books, tags, users

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(books.router)
app.include_router(tags.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.on_event("startup")
def startup_event():
    create_default_admin()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bibliotheque API!"}