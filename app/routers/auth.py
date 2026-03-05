from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.database import get_db
from app.models.users import User
from app.schemas.users import CreateUser, Token, UserLogin

router = APIRouter(
)


@router.post("/register", response_model=Token, status_code=201)
def register(user: CreateUser, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")

    new_user = User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        date_created=datetime.utcnow(),
    )

    db.add(new_user)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        error_message = str(exc.orig).lower()
        if "users_username_key" in error_message:
            raise HTTPException(status_code=400, detail="Username already taken")
        if "users_email_key" in error_message:
            raise HTTPException(status_code=400, detail="Email already registered")
        raise HTTPException(status_code=400, detail="User already exists")

    db.refresh(new_user)

    token = create_access_token(data={"sub": str(new_user.id), "role": new_user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": new_user.role,
    }


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"sub": str(db_user.id), "role": db_user.role})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role,
    }
