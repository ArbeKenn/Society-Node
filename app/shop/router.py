from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.user.jwt import get_current_user
from app.shop.models import ShopItem as ShopItemModel
from app.shop.schemas import ShopItemSchema
from app.user.models import (
    User as UserModel,
    UserItem as UserItemModel
)

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

@router.post('/{item_id}/by')
async def by_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(ShopItemModel)
        .where(ShopItemModel.id == item_id)
    )
    item = result.scalar_one_or_none()

    if not item:
        raise HTTPException(
            status_code=404,
            detail='Item Not Found'
        )

    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()

    result = await db.execute(
        select(UserItemModel)
        .where(
            UserItemModel.user_id == user_id,
            UserItemModel.item_id == item_id
        )
    )
    user_item = result.scalar_one_or_none()

    if user.coin < item.price:
        raise HTTPException(
            status_code=403,
            detail='You don`t have enough coins'
        )

    user.coin -= item.price

    if user_item:
        user_item.quantity += 1
    else:
        new_item = UserItemModel(
            title=item.title,
            user_id=user_id,
            item_id=item_id,
            quantity=1
        )
        db.add(new_item)

    await db.commit()
    return {f'you have successfully purchased {item.title}'}
