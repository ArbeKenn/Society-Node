from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, Numeric
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    is_staff = Column(Boolean, default=False)
    age = Column(Integer)
    gender = Column(String)
    coin = Column(Numeric, default=0)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    date_joined = Column(DateTime, default=func.now())
    last_login = Column(DateTime, nullable=True)

    posts = relationship('Post', back_populates='user')