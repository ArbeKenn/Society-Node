from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.posts.models import Post as PostModel, Like as LikeModel
from app.posts.schemas import PostCreateUpdateSchema
from app.user.jwt import get_current_user

router = APIRouter(
    prefix='/post',
    tags=['Publications']
)

limiter = Limiter(key_func=get_remote_address)

@router.get('/posts')
@limiter.limit('1/sec')
def all_posts(request: Request, db: Session = Depends(get_db)):
    posts = db.query(PostModel).limit(10)
    for post in posts:
        post.views +=1
        db.commit()
        db.refresh(post)
    return posts

@router.get('posts/{post_id}')
@limiter.limit('1/sec')
def detail_post(request: Request, post_id: int, db: Session = Depends(get_db)):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    post.views += 1
    db.commit()
    db.refresh(post)
    return post

@router.post('posts/{post_id}/like')
def like(
        post_id: int,
        db: Session = Depends(get_db),
        user_id: int =Depends(get_current_user)
):
    post = db.query(PostModel).filter(PostModel.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post Not Found'
        )
    existing = db.query(LikeModel).filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    if existing:
        db.delete(existing)
        post.like -= 1
        db.commit()
        return {'status': 'unliked'}

    else:
        db.add(LikeModel(user_id=user_id, post_id=post_id))
        post.like += 1
        db.commit()
        return {'status': 'liked'}

@router.post('/new_post')
def create_post(
        post: PostCreateUpdateSchema,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):

    new_post = PostModel(**post.model_dump())
    new_post.user_id = user_id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put('/edit/{post_id}')
def edit_post(
        post_id: int,
        post_schema: PostCreateUpdateSchema,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):

    post = db.query(PostModel).filter(
        PostModel.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post Not Found')

    for key, value in post_schema.model_dump().items():
        setattr(post, key, value)

    post.user_id = user_id
    db.commit()
    db.refresh(post)
    return post

@router.delete('/del/{post_id}')
def del_post(
        post_id: int,
        db: Session = Depends(get_db),
        user_id: int = Depends(get_current_user)
):

    post = db.query(PostModel).filter(
        PostModel.id == post_id
    ).first()

    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post Not Found')

    if post.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail='Not your post'
        )

    db.delete(post)
    db.commit()
    return {'message': 'Post deleted'}