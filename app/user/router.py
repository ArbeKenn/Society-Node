from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from pwdlib import PasswordHash

from app.user.schemas import UserSchema, UserLoginSchema, UserUpdateSchema, UserResponseSchema, FollowersListSchema, FollowerUserSchema
from app.user.models import User as UserModel, Follower as FollowerModel
from app.database import get_db
from app.user.jwt import create_token, get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Authentication']
)

pwd = PasswordHash.recommended()

@router.get('/all')
async def all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    return result.scalars().all()


@router.post('/reg')
async def registration(
        user: UserSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserModel).where(
        UserModel.username == user.username
    ))
    existing_user = result.scalars().all()

    if existing_user:
        raise HTTPException(
            status_code=404,
            detail='The user already exists'
        )

    hashed_password = pwd.hash(user.password)

    new_user = UserModel(**user.model_dump())
    new_user.password = hashed_password

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post('/log')
async def login(
        user: UserLoginSchema,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserModel).where(
        UserModel.username == user.username
    ))
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
async def profile(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(select(UserModel).where(
        UserModel.id == user_id
    ))
    user_profile = result.scalar_one_or_none()

    if not user_profile:
        raise HTTPException(
            status_code=404,
            detail='User Not Found')

    return user_profile

@router.get('/my_profile/followers') #to correct
async def my_followers(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )

    followers = [f.follower for f in user.followers_rel]
    return followers


@router.get('/my_profile/following') #to correct
async def my_following(
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(UserModel)
        .options(
            selectinload(UserModel.following_rel)
            .selectinload(FollowerModel.following)
        )
        .where(UserModel.id == user_id)
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
async def edit_profile(
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
async def del_user(
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
async def follow(
        target_user_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(select(FollowerModel).filter_by(
        follower_id=user_id,
        following_id=target_user_id
    ))
    existing = result.scalar_one_or_none()

    result = await db.execute(select(UserModel).where(
        UserModel.id == target_user_id
    ))
    target_user = result.scalar_one_or_none()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
    target_user.followers += 1

    result = await db.execute(select(UserModel).where(
        UserModel.id == user_id
    ))
    current_user = result.scalar_one_or_none()

    if existing:
        await db.delete(existing)
        target_user.followers -= 1
        current_user.following -= 1
        await db.commit()
        return {'status': 'unfollowed'}
    else:
        db.add(FollowerModel(follower_id=user_id, following_id=target_user_id))
        target_user.followers += 1
        current_user.following += 1
        await db.commit()
        return {'status': 'followed'}

@router.get('/followers/{user_id}', response_model=FollowersListSchema) #to correct
async def get_followers(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(
        UserModel.id == user_id
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