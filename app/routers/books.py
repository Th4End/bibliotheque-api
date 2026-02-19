from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.openlibrary import fetch_openlibrary
from app.services.googlebook import fetch_from_googlebook
from app.core.auth import get_current_user
from app.database import get_db
from app.models.Books import Book
from app.schemas.Books import Bookcreate, BookResponse, Bookupdate

router = APIRouter(
    prefix="/books",
    tags=["books"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=list[BookResponse], status_code=200)
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()

@router.post("/add", response_model= BookResponse, status_code=201)
def create_book(book: Bookcreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookResponse, status_code=200)
def update_book(book_id: int, book: Bookupdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    db.delete(db_book)
    db.commit()

@router.post("/isbn/{isbn}", response_model=BookResponse, status_code=200)
def get_book_by_isbn(isbn: str, db: Session = Depends(get_db)):
    book_data = fetch_openlibrary(isbn)
    if book_data is None:
        book_data = fetch_from_googlebook(isbn)
    if book_data is None:
        raise HTTPException(status_code=404, detail="Book not found in OpenLibrary or Google Books")

    book = Book(
        title=book_data["title"],
        author=book_data["authors"],
        year=book_data["year"],
        isbn=isbn
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

