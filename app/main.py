from fastapi import FastAPI
from app.database import engine, Base
from app.routers import books

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(books.router)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Bibliotheque API!"}