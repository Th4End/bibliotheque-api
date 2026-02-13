from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    email: str
    password: str

class UpdateUser(BaseModel):
    username: str | None = None
    email: str | None = None
    password: str | None = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    date_created: str

model_config = {
    "from_attributes": True,
}