from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.tags import Tag

router = APIRouter(
    prefix="/tags",
    tags=["tags"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
def get_tags(db: Session = Depends(get_db)):
    return db.query(Tag).all()