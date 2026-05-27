from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String, nullable=True)
    like = Column(Integer, default=0)
    views = Column(Integer, default=0)

    user = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post', cascade='all, delete-orphan')

class Like(Base):
    __tablename__ = 'likes'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True)
    post = relationship('Post', back_populates='likes')
