from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.posts.models import Post as PostModel
from app.user.models import User as UserModel
from app.shop.models import ShopItem as ShopItemModel

from app.user.schemas import UserResponseSchema
from app.posts.schemas import PostResponseSchema
from app.search.schemas import SearchSchema
from app.shop.schemas import ShopItemSchema

router = APIRouter(
    prefix='/search',
    tags=['Search']
)

limiter = Limiter(key_func=get_remote_address)

@router.get('/post', response_model=list[PostResponseSchema])
@limiter.limit('50/1seconds')
async def search_post(
        request: Request,
        schemas: SearchSchema = Depends(),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PostModel)
        .where(or_(PostModel.title.ilike(f'%{schemas.q}%')))
        .offset(schemas.offset)
        .limit(schemas.limit)
    )
    posts = result.scalars().all()
    return posts

@router.get('/user', response_model=list[UserResponseSchema])
@limiter.limit('50/1seconds')
async def search_user(
        request: Request,
        schemas: SearchSchema = Depends(),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserModel)
        .where(or_(UserModel.username.ilike(f'%{schemas.q}%')))
        .offset(schemas.offset)
        .limit(schemas.limit)
    )
    users = result.scalars().all()
    return users

@router.get('/shop', response_model=list[ShopItemSchema])
@limiter.limit('50/1seconds')
async def search_in_shop(
        request: Request,
        schemas: SearchSchema = Depends(),
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ShopItemModel)
        .where(or_(ShopItemModel.title.ilike(f'%{schemas.q}%')))
        .offset(schemas.offset)
        .limit(schemas.limit)
    )
    items = result.scalars().all()
    return items