from sqlalchemy import Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.tags import Tag


book_tags = Table(
    "book_tags",
    Base.metadata,
    mapped_column("book_id", Integer, ForeignKey("books.id"), primary_key=True),
    mapped_column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    isbn: Mapped[str | None] = mapped_column(String(20), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    tags = relationship("Tag", secondary=book_tags, back_populates="books")