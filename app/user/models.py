from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, Numeric, ForeignKey
from sqlalchemy.orm import relationship, Mapped
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

    posts: Mapped[list['Post']] = relationship(
        'Post',
        back_populates='user',
        lazy='selectin'
    )

    followers_rel: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.following_id',
        back_populates='following',
        lazy='selectin'
    )
    following_rel: Mapped[list['Follower']] = relationship(
        'Follower',
        foreign_keys='Follower.follower_id',
        back_populates='follower',
        lazy='selectin'
    )


class Follower(Base):
    __tablename__ = 'followers'

    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    following_id = Column(Integer, ForeignKey('users.id'), primary_key=True)

    follower: Mapped['User'] = relationship(
        'User',
        foreign_keys=[follower_id],
        back_populates='following_rel',
        lazy='selectin'
    )
    following: Mapped['User'] = relationship(
        'User',
        foreign_keys=[following_id],
        back_populates='followers_rel',
        lazy='selectin'
    )