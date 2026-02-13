from pydantic import BaseModel

class Tagscreate(BaseModel):
    name: str
    description: str | None = None

class Tagsupdate(BaseModel):
    name: str | None = None
    description: str | None = None

class TagsResponse(BaseModel):
    id: int
    name: str
    description: str | None

model_config = {
    "from_attributes": True,
}