from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.database import get_db
from app.schemas.users import CreateUser, UpdateUser, UserResponse
from app.models.users import User
from app.core.auth import require_role, upgrade_to_admin, upgrade_to_moderator, unrank_to_user
from app.schemas.users import CreateUser, UpdateUser, UserResponse, UserRole

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)
@router.get("/profile", response_model=UserResponse, status_code=200)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/profile", response_model=UserResponse, status_code=200)
def update_profile(user: UpdateUser, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    update_data = user.model_dump(exclude_unset=True)
    if "password" in update_data:
        update_data["password"] = User.hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(current_user, key, value)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/profile", status_code=204)
def delete_profile(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    db.delete(current_user)
    db.commit()