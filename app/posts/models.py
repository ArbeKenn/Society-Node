from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped
from app.database import Base

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String, nullable=True)
    like = Column(Integer, default=0)
    views = Column(Integer, default=0)
    favorite = Column(Integer, default=0)

    user = relationship(
        'User',
        back_populates='posts',
        lazy='selectin'
    )
    comments = relationship(
        'Comment',
        back_populates='post',
        cascade='all, delete-orphan',
        lazy='selectin'
    )
    likes = relationship(
        'Like',
        back_populates='post',
        cascade='all, delete-orphan',
        lazy='selectin'
    )

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'))
    like = Column(Integer, default=0)

    post = relationship(
        'Post',
        back_populates='comments',
        lazy='selectin'

    )
    likes = relationship(
        'CommentLike',
        back_populates='comment',
        cascade='all, delete-orphan',
        lazy='selectin'
    )


class Like(Base):
    __tablename__ = 'likes'

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    )
    post_id = Column(
        Integer,
        ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True
    )

    post = relationship(
        'Post',
        back_populates='likes',
        lazy='selectin'
    )


class CommentLike(Base):
    __tablename__ = 'comment_likes'

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    )
    comment_id = Column(
        Integer,
        ForeignKey('comments.id', ondelete='CASCADE'),
        primary_key=True
    )

    comment = relationship(
        'Comment',
        back_populates='likes',
        lazy='selectin'
    )

class Favorite(Base):
    __tablename__ = 'favorites'

    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        primary_key=True
    )

    post_id = Column(
        Integer,
        ForeignKey('posts.id', ondelete='CASCADE'),
        primary_key=True
    )