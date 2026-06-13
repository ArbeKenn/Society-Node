from pydantic import BaseModel, Field
class SearchSchema(BaseModel):
    q: str = Field(..., min_length=1, max_length=100)
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0)
