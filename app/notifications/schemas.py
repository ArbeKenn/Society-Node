from pydantic import BaseModel
class NotificationSchema(BaseModel):
    id: int
    title: str
    user_id: int
    user_id_from_whom: int
    is_read: bool