from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.database import get_db
from app.posts.models import Post as PostModel
from app.user.models import User as UserModel
from app.user.schemas import UserResponseSchema
from app.posts.schemas import PostResponseSchema
from app.search.schemas import SearchSchema

router = APIRouter(
    prefix='/search',
    tags=['Search']
)

@router.get('/post', response_model=list[PostResponseSchema])
async def search_post(
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
async def search_user(
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

@router.get('/shop')
async def search_in_shop():
    pass