import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.schemas.Books import Bookcreate, Bookupdate, BookResponse

def test_bookcreate_schema():
    data = {"title": "Test", "author": "Auteur", "isbn": "123", "year": 2020}
    book = Bookcreate(**data)
    assert book.title == "Test"
    assert book.author == "Auteur"
    assert book.isbn == "123"
    assert book.year == 2020

def test_bookupdate_schema():
    data = {"title": "Maj", "author": None, "isbn": None, "year": None}
    book = Bookupdate(**data)
    assert book.title == "Maj"
    assert book.author is None
    assert book.isbn is None
    assert book.year is None

def test_bookresponse_schema():
    data = {"id": 1, "title": "Livre", "author": "Auteur", "isbn": None, "year": None}
    book = BookResponse(**data)
    assert book.id == 1
    assert book.title == "Livre"
    assert book.author == "Auteur"
