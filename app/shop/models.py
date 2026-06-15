from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base
class ShopItem(Base):
    __tablename__ = 'shop_items'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    image = Column(String)
    price = Column(Integer, nullable=False)
    rarity = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())