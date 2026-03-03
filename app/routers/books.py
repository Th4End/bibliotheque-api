from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
import re
from app.services.openlibrary import fetch_openlibrary
from app.services.googlebook import fetch_from_googlebook
from app.services.storage import delete_file_from_supabase, upload_file_to_supabase
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


def _normalize_isbn(raw_isbn: str) -> str:
    normalized = re.sub(r"[^0-9Xx]", "", raw_isbn).upper()
    if normalized.startswith("ISBN"):
        normalized = normalized.replace("ISBN", "", 1)
    return normalized

@router.get("/", response_model=list[BookResponse], status_code=200)
def get_books(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Book).filter(Book.user_id == current_user.id).all()

@router.post("/add", response_model= BookResponse, status_code=201)
def create_book(book: Bookcreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_book = Book(**book.model_dump(), user_id=current_user.id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.put("/{book_id}", response_model=BookResponse, status_code=200)
def update_book(book_id: int, book: Bookupdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id, Book.user_id == current_user.id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_book = db.query(Book).filter(Book.id == book_id, Book.user_id == current_user.id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    await delete_file_from_supabase(db_book.cover_url)

    db.delete(db_book)
    db.commit()

@router.post("/isbn/{isbn}", response_model=BookResponse, status_code=200)
def get_book_by_isbn(isbn: str, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    normalized_isbn = _normalize_isbn(isbn)
    if not normalized_isbn:
        raise HTTPException(status_code=400, detail="Invalid ISBN")

    book_data = fetch_openlibrary(normalized_isbn)
    if book_data is None:
        book_data = fetch_from_googlebook(normalized_isbn)
    if book_data is None:
        raise HTTPException(status_code=404, detail="Book not found in OpenLibrary or Google Books")

    book = Book(
        title=book_data["title"],
        author=book_data["authors"],
        year=book_data["year"],
        isbn=normalized_isbn,
        user_id= current_user.id
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}/cover", response_model=BookResponse, status_code=200)
async def update_book_cover(
    book_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    db_book = db.query(Book).filter(Book.id == book_id, Book.user_id == current_user.id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    old_cover_url = db_book.cover_url
    cover_url = await upload_file_to_supabase(file=file, folder=f"books/{book_id}")
    if old_cover_url and old_cover_url != cover_url:
        await delete_file_from_supabase(old_cover_url)

    db_book.cover_url = cover_url
    db.commit()
    db.refresh(db_book)
    return db_book

