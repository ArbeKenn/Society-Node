from sqlalchemy import Column, Integer, String, Boolean, Date
from app.database import Base
import datetime
class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    image = Column(String)
    price = Column(Integer, nullable=False)
    rarity = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, default=datetime.utcnow)