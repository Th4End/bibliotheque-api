from fastapi import FastAPI
from app.core.init_admin import create_default_admin
from app.database import Base, engine
from app.routers import admin, auth, books, tags, users, health
from app.routers import search
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
load_dotenv()

origins = os.getenv("Origins").split(",")

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_methods=["*"], 
    allow_headers=["*"], 
    allow_credentials=True
)

app.include_router(books.router)
app.include_router(tags.router)
app.include_router(admin.router)
app.include_router(auth.router)
app.include_router(search.router)
app.include_router(users.router)
app.include_router(health.router)

@app.on_event("startup")
def startup_event():
    create_default_admin()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Bibliotheque API!"}