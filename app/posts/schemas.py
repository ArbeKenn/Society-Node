"""
comments
"""
from pydantic import BaseModel

class PostCreateUpdateSchema(BaseModel):
    title: str
    description: str | None

class PostResponseSchema(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    like: int = 0
    views: int = 0
