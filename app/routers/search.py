from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.Books import Book
from app.routers import books

router = APIRouter(
    prefix="/search",
    tags=["search"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)

@router.get("/search", response_model=list[books.BookResponse])
def search_books(q: str, db: Session = Depends(get_db)):
    return db.query(Book).filter(
        Book.title.ilike(f"%{q}%") |
        Book.author.ilike(f"%{q}%") |
        Book.isbn.ilike(f"%{q}%")
    ).all()
