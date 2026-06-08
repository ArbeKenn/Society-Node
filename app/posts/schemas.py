from pydantic import BaseModel, Field

class CommentCreateUpdateSchema(BaseModel):
    text: str

class CommentResponseSchema(BaseModel):
    id: int
    user_id: int
    text: str
    like: int

class PostCreateUpdateSchema(BaseModel):
    title: str = Field(min_length=4, max_length=128)
    description: str

class PostResponseSchema(BaseModel):
    id: int
    user_id: int
    title: str
    description: str | None
    like: int = 0
    views: int = 0
    favorite: int = 0
    comments: list[CommentResponseSchema]

class FavoriteResponseSchema(BaseModel):
    user_id: int
    post_id: int
