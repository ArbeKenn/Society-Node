from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.user.schemas import UserSchema, UserLoginSchema, UserUpdateSchema, UserResponseSchema, FollowersListSchema
from app.user.models import User as UserModel, Follower as FollowerModel
from app.database import get_db
from app.user.jwt import create_token, get_current_user

router = APIRouter(
    prefix='/user',
    tags=['Authentication']
)

pwd = PasswordHash.recommended()

@router.get('/all')
def all_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()


@router.post('/reg')
def registration(
        user: UserSchema,
        db: Session = Depends(get_db)
):
    existing_user = db.query(UserModel).filter(
        UserModel.username == user.username
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=404,
            detail='The user already exists'
        )

    hashed_password = pwd.hash(user.password)

    new_user = UserModel(**user.model_dump())
    new_user.password = hashed_password

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/log')
def login(
        user: UserLoginSchema,
        db: Session = Depends(get_db)
):
    db_user = db.query(UserModel).filter(
        UserModel.username == user.username
    ).first()

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
def profile(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    user_profile = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not user_profile:
        raise HTTPException(
            status_code=404,
            detail='User Not Found')

    return user_profile

@router.get('/my_profile/followers')
def my_followers(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )

    followers = [f.follower for f in user.followers_rel]
    return followers


@router.get('/my_profile/following')
def my_following(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User not found'
        )
    following = [f.following for f in user.following_rel]
    return following

@router.put('/my_profile/edit', response_model=UserUpdateSchema)
def edit_profile(
        user: UserUpdateSchema,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    db_user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=404,
            detail='User Not Found')

    for key, value in user.model_dump().items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete('/my_profile/del')
def del_user(
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail='User Not Found'
        )
    db.delete(user)
    db.commit()
    return {'message': 'Account deleted'}

@router.post('/follow/{target_user_id}')
def follow(
        target_user_id: int,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    existing = db.query(FollowerModel).filter_by(
        follower_id=user_id,
        following_id=target_user_id
    ).first()

    target_user = db.query(UserModel).filter(
        UserModel.id == target_user_id
    ).first()
    current_user = db.query(UserModel).filter(
        UserModel.id == user_id
    ).first()

    if existing:
        db.delete(existing)
        target_user.followers -= 1
        current_user.following -= 1
        db.commit()
        return {'status': 'unfollowed'}
    else:
        db.add(FollowerModel(follower_id=user_id, following_id=target_user_id))
        target_user.followers += 1
        current_user.following += 1
        db.commit()
        return {'status': 'followed'}

@router.get('/followers/{user_id}', response_model=FollowersListSchema)
def get_followers(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()

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