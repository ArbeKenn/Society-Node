from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from app.database import Base

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user_id_from_whom = Column(Integer, ForeignKey('users.id'))
    is_read = Column(Boolean)
