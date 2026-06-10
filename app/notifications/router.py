from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.user.jwt import get_current_user
from app.user.models import User as UserModel
from app.notifications.models import Notification as NotificationModel

router = APIRouter(
    prefix='/notification',
    tags=['Notification']
)

@router.get('/')
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