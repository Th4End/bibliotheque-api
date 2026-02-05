import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

try:
    with engine.connect() as connection:
        print("Database connected successfully.")
except Exception as e:
    print("Failed to connect to the database:", e)

class Base(DeclarativeBase):
    pass