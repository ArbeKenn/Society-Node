from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.user.jwt import get_current_user
from app.shop.models import ShopItem as ShopItemModel
from app.shop.schemas import ShopItemSchema

router = APIRouter(
    prefix='/shop',
    tags=['Shop']
)

@router.get('/', response_model=list[ShopItemSchema])
async def get_shop(
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(ShopItemModel))
    items_shop = result.scalars().all()

    return items_shop