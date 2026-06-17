from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.user.jwt import get_current_user
from app.shop.models import ShopItem as ShopItemModel
from app.shop.schemas import ItemCreateUpdateSchemas
from app.user.models import User as UserModel

router = APIRouter(
    prefix='/admin',
    tags=['Admin']
)

@router.get('/')
async def admin(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='You do not have administrator rights.'
        )

    return {'message': 'Admin panel'}


@router.post('/item')
async def create_item(
        shop_schemas: ItemCreateUpdateSchemas,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='You do not have administrator rights.'
        )
    else:
        new_item = ShopItemModel(**shop_schemas.model_dump())
        db.add(new_item)
        await db.commit()
        await db.refresh(new_item)

    return new_item

@router.put('/item/{item_id}')
async def update_item(
        item_id: int,
        shop_schemas: ItemCreateUpdateSchemas,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='You do not have administrator rights.'
        )

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

    for key, value in shop_schemas.model_dump().items():
        setattr(item, key, value)
        await db.commit()

    return item

@router.delete('/item/{item_id}')
async def del_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user.is_admin:
        raise HTTPException(
            status_code=403,
            detail='You do not have administrator rights.'
        )

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

    await db.delete(item)
    await db.commit()
    return {'message': 'Item deleted'}