from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    role: str | None = None


class UpdateUser(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None

class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role : UserRole
    date_created: datetime

    model_config = {
        "from_attributes": True
    }
 