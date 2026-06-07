from pydantic import BaseModel

class CommentCreateUpdateSchema(BaseModel):
    text: str

class CommentResponseSchema(BaseModel):
    id: int
    user_id: int
    text: str
    like: int

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
    favorite: int = 0
    comments: list[CommentResponseSchema]

class FavoriteResponseSchema(BaseModel):
    user_id: int
    post_id: int
