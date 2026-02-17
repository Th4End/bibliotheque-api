from os import getenv

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.models.users import UserRole
from app.database import get_db
from app.models.users import User

load_dotenv()
secret_key = getenv("secret_key")
algorithm = getenv("algorithm")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    user = db.get(User, user_id)

    if user is None:
        raise credentials_exception

    return user

def require_role(*allowed_roles: UserRole):
    def role_checker(get_current_user: User = Depends(get_current_user)):
        if get_current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return get_current_user
    return role_checker

def upgrade_to_admin(*allowed_roles: UserRole):
    def role_checker(get_current_user: User = Depends(get_current_user)):
        if get_current_user.role not in allowed_roles:
            get_current_user.role = UserRole.ADMIN
            db: Session = get_db()
            db.add(get_current_user)
            db.commit()
            db.refresh(get_current_user)
        else: 
            raise HTTPException(status_code=403, detail="Forbidden")
        return get_current_user
    return role_checker

def unrank_to_user(*allowed_roles: UserRole):
    def role_checker(get_current_user: User = Depends(get_current_user)):
        if get_current_user.role in allowed_roles:
            get_current_user.role = UserRole.USER
            db: Session = get_db()
            db.add(get_current_user)
            db.commit()
            db.refresh(get_current_user)
        else: 
            raise HTTPException(status_code=403, detail="Forbidden")
        return get_current_user
    return role_checker