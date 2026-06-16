from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.user.jwt import get_current_user
from app.notifications.models import Notification as NotificationModel
from app.notifications.schemas import NotificationSchema

router = APIRouter(
    prefix='/notification',
    tags=['Notification']
)

limiter = Limiter(key_func=get_remote_address)

@router.get('/', response_model=list[NotificationSchema])
@limiter.limit("50/1seconds")
async def Notification(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(NotificationModel)
        .where(NotificationModel.user_id == user_id))
    notifications = result.scalars().all()

    for notification in notifications:
        notification.is_read = True

    await db.commit()
    return notifications