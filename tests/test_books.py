import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.Books import Book
from app.models.tags import Tag
from app.database import Base

@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture(scope="function")
def session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


def test_create_book(session):
    book = Book(title="1984", author="George Orwell", year=1949, isbn="1234567890", user_id=1)
    session.add(book)
    session.commit()
    assert book.id is not None
    assert book.title == "1984"
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.isbn == "1234567890"
    assert book.user_id == 1


def test_book_tag_relationship(session):
    book = Book(title="Dune", author="Frank Herbert", year=1965, isbn="0987654321", user_id=2)
    tag = Tag(name="Science-Fiction")
    book.tags.append(tag)
    session.add(book)
    session.commit()
    assert tag in book.tags
    assert book in tag.books
