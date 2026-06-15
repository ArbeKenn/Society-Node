from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime


class ShopItemSchema(BaseModel):
    id: int
    title: str
    image: str
    price: int = Field(ge=20)
    rarity: Literal["base","unusual","rare","epic","legendary"]
    is_active: bool
    created_at: datetime

class ItemCreateUpdateSchemas(BaseModel):
    title: str
    image: str
    price: int = Field(ge=20)
    rarity: Literal["base", "unusual", "rare", "epic", "legendary"]
    is_active: bool