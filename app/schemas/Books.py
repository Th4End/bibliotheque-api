from pydantic import BaseModel

class Bookcreate(BaseModel):
    title: str
    author: str
    isbn: str | None = None
    year: int | None = None

class Bookupdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    year: int | None = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    isbn: str | None
    year: int | None
    model_config = {
        "from_attributes": True,
    }
