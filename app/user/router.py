from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pwdlib import PasswordHash
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.user.schemas import (
    UserSchema, UserLoginSchema, UserUpdateSchema,
    UserResponseSchema, UserItemResponseSchema,
    FollowersListSchema, FollowerUserSchema
)
from app.user.models import (
    User as UserModel,
    UserItem as UserItemModel,
    Follower as FollowerModel
)
from app.posts.models import (
    Favorite as FavoriteModel,
    Post as PostModel
)
from app.notifications.models import Notification as NotificationModel
from app.posts.schemas import PostResponseSchema
from app.database import get_db
from app.user.jwt import create_token, get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Authentication']
)

pwd = PasswordHash.recommended()
limiter = Limiter(key_func=get_remote_address)

@router.post('/reg')
@limiter.limit('1/sec')
async def registration(
        request: Request,
        user: UserSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.username == user.username)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=404,
            detail='The user already exists'
        )

    hashed_password = pwd.hash(user.password)

    new_user = UserModel(**user.model_dump())
    new_user.password = hashed_password
    new_user.coin = 100
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post('/log')
@limiter.limit('1/sec')
async def login(
        request: Request,
        user: UserLoginSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.username == user.username)
    )
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='Incorrect login or password'
        )

    if not pwd.verify(user.password, db_user.password):
        raise HTTPException(
            status_code=400,
            detail='Incorrect login or password'
        )

    token = create_token(db_user.id)
    return {'token': token}

@router.get('/my_profile', response_model=UserResponseSchema)
@limiter.limit('1/sec')
async def profile(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
    )
    user_profile = result.scalar_one_or_none()

    if not user_profile:
        raise HTTPException(
            status_code=404,
            detail='User Not Found')

    return user_profile

@router.get('/my_profile/favorites', response_model=list[PostResponseSchema])
@limiter.limit('1/sec')
async def my_favorites(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(PostModel)
        .join(FavoriteModel, FavoriteModel.post_id == PostModel.id)
        .where(FavoriteModel.user_id == user_id)
    )
    favorites = result.scalars().all()
    return favorites

@router.get('/my_profile/my_item', response_model=list[UserItemResponseSchema])
async def my_item(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserItemModel)
        .where(UserItemModel.user_id == user_id)
    )
    items = result.scalars().all()

    return items

@router.get('/my_profile/followers', response_model=list[FollowerUserSchema])
@limiter.limit('1/sec')
async def my_followers(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.followers_rel)
                 .selectinload(FollowerModel.follower))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )

    followers = [f.follower for f in user.followers_rel]
    return followers


@router.get('/my_profile/following', response_model=list[FollowerUserSchema])
@limiter.limit('1/sec')
async def my_following(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.following_rel)
                 .selectinload(FollowerModel.following))
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    following = [f.following for f in user.following_rel]
    return following

@router.put('/my_profile/edit', response_model=UserUpdateSchema)
@limiter.limit('1/sec')
async def edit_profile(
        request: Request,
        user: UserUpdateSchema,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(select(UserModel).where(
        UserModel.id == user_id
    ))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User Not Found')

    for key, value in user.model_dump().items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)
    return db_user


@router.delete('/my_profile/del')
@limiter.limit('1/sec')
async def del_user(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(select(UserModel).where(
        UserModel.id == user_id
    ))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail='User Not Found'
        )
    await db.delete(user)
    await db.commit()
    return {'message': 'Account deleted'}

@router.post('/follow/{target_user_id}')
@limiter.limit('1/sec')
async def follow(
        request: Request,
        target_user_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(select(FollowerModel).where(
        FollowerModel.follower_id == user_id,
        FollowerModel.following_id == target_user_id
    ))
    existing = result.scalar_one_or_none()

    result = await db.execute(select(UserModel).where(
        UserModel.id == target_user_id
    ))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user_id == target_user_id:
        raise HTTPException(
            status_code=400,
            detail='Can`t follow yourself'
        )

    result = await db.execute(select(UserModel).where(
        UserModel.id == user_id
    ))
    current_user = result.scalar_one_or_none()

    if existing:
        await db.delete(existing)
        target_user.followers -= 1
        current_user.following -= 1
        db.add(target_user)
        db.add(current_user)
        await db.commit()
        return {'status': 'unfollowed'}
    else:

        new_notification = NotificationModel(
            user_id=target_user_id,
            user_id_from_whom=user_id,
            title=f"User {current_user.username} has subscribed to you",
            is_read=False
        )
        db.add(new_notification)
        await db.commit()

        db.add(FollowerModel
               (follower_id=user_id,
                following_id=target_user_id)
               )
        target_user.followers += 1
        current_user.following += 1
        db.add(target_user)
        db.add(current_user)
        await db.commit()
        return {'status': 'followed'}

@router.get('/followers/{user_id}', response_model=FollowersListSchema)
@limiter.limit('1/sec')
async def get_followers(
        request: Request,
        user_id: int,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserModel)
        .where(UserModel.id == user_id)
        .options(selectinload(UserModel.following_rel)
                 .selectinload(FollowerModel.following),
                 selectinload(UserModel.followers_rel)
                 .selectinload(FollowerModel.follower)
    ))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    followers = [f.follower for f in user.followers_rel]
    following = [f.following for f in user.following_rel]

    return {
        'followers': followers,
        'following': following,
        'followers_count': user.followers,
        'following_count': user.following
    }