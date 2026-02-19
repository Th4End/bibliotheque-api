from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.auth import get_current_user
from app.database import get_db
from app.schemas.users import CreateUser, UpdateUser, UserResponse
from app.models.users import User
from app.core.auth import require_role, upgrade_to_admin, upgrade_to_moderator, unrank_to_user
from app.schemas.users import CreateUser, UpdateUser, UserResponse, UserRole

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_user), Depends(require_role(UserRole.ADMIN))],
    responses={404: {"description": "Not found"}},
)

@router.get("/users", response_model=list[UserResponse], status_code=200)
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/users/add", response_model=UserResponse, status_code=201)
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.put("/users/{user_id}", response_model=UserResponse, status_code=200)
def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.get(User, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()

@router.put("/users/{user_id}/addadmin", response_model=UserResponse, status_code=200)
def upgrade_user_admin(user_id: int, db: Session = Depends(get_db)):
    return upgrade_to_admin(user_id, db)

@router.put("/users/{user_id}/addmoderator", response_model=UserResponse, status_code=200)
def upgrade_user_moderator(user_id: int, db: Session = Depends(get_db)):
    return upgrade_to_moderator(user_id, db)


@router.put("/users/{user_id}/unrank", response_model=UserResponse, status_code=200)
def unrank_user_to_user(user_id: int, db: Session = Depends(get_db)):
    return unrank_to_user(user_id=user_id, db=db)