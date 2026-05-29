from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.database import get_db
from app.posts.models import (
    Post as PostModel,
    Like as LikeModel,
    Comment as CommentModel,
    CommentLike as CommentLikeModel
)
from app.posts.schemas import (
    PostCreateUpdateSchema,
    CommentCreateUpdateSchema
)
from app.user.jwt import get_current_user

router = APIRouter(
    prefix='/posts',
    tags=['Publications']
)

limiter = Limiter(key_func=get_remote_address)

@router.get('/')
@limiter.limit('1/sec')
async def all_posts(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(PostModel))
    posts = result.scalars().all()

    for post in posts:
        post.views +=1
    await db.commit()
    return posts

@router.get('/{post_id}')
@limiter.limit('1/sec')
async def detail_post(
        request: Request,
        post_id: int, db:
        AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PostModel)
        .where(PostModel.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post not found'
        )

    post.views += 1
    await db.commit()
    await db.refresh(post)
    return post

@router.post('/{post_id}/like')
@limiter.limit('1/sec')
async def like(
        request: Request,
        post_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int =Depends(get_current_user)
):
    result = await db.execute(
        select(PostModel)
        .where(PostModel.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post Not Found'
        )
    result = await db.execute(
        select(LikeModel)
        .where(LikeModel.user_id == user_id, LikeModel.post_id == post_id)
    )

    existing = result.scalar_one_or_none()

    if existing:
        await db.delete(existing)
        post.like -= 1
        await db.commit()
        return {'status': 'unliked'}

    else:
        db.add(LikeModel(user_id=user_id, post_id=post_id))
        post.like += 1
        await db.commit()
        return {'status': 'liked'}

@router.post('/new_post')
@limiter.limit('1/sec')
async def create_post(
        request: Request,
        post_schema: PostCreateUpdateSchema,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):

    new_post = PostModel(**post_schema.model_dump())
    new_post.user_id = user_id
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


@router.put('/{post_id}')
@limiter.limit('1/sec')
async def edit_post(
        request: Request,
        post_id: int,
        post_schema: PostCreateUpdateSchema,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):

    result = await db.execute(
        select(PostModel)
        .where(PostModel.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post Not Found')

    if post.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail='Not your post')

    for key, value in post_schema.model_dump().items():
        setattr(post, key, value)

    post.user_id = user_id
    await db.commit()
    await db.refresh(post)
    return post

@router.delete('/{post_id}')
@limiter.limit('1/sec')
async def del_post(
        request: Request,
        post_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):

    result = await db.execute(select(PostModel).where(
        PostModel.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post Not Found')

    if post.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail='Not your post'
        )

    await db.delete(post)
    await db.commit()
    return {'message': 'Post deleted'}


@router.get('/comments/{post_id}')
@limiter.limit('1/sec')
async def all_comments(
        request: Request,
        post_id: int,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(PostModel)
        .where(PostModel.id == post_id)
    )
    post = result.scalar_one_or_none()

    if not post:
        raise HTTPException(
            status_code=404,
            detail='Post not found'
        )

    result = await db.execute(select(CommentModel))
    comments = result.scalars().all()

    return comments

@router.post('/comments/{post_id}')
@limiter.limit('1/sec')
async def create_comment(
        request: Request,
        post_id: int,
        comment_schemas: CommentCreateUpdateSchema,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(PostModel)
        .where(PostModel.id == post_id)
    )
    post = result.scalar_one_or_none()
    if not post:

        raise HTTPException(
            status_code=404,
            detail='Post not found'
        )

    new_comment = CommentModel(
        **comment_schemas.model_dump(),
        user_id=user_id,
        post_id=post_id
    )
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment

@router.put('/comments/{comment_id}')
@limiter.limit('1/sec')
async def edit_comment(
        request: Request,
        comment_id: int,
        comment_schemas: CommentCreateUpdateSchema,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(CommentModel)
        .where(CommentModel.id == comment_id)
    )
    comment = result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail='Comment not found'
        )

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail='Not your comment'
        )

    comment.text = comment_schemas.text
    await db.commit()
    await db.refresh(comment)

    return comment



@router.delete('/comments/{comment_id}')
@limiter.limit('1/sec')
async def del_comment(
        request: Request,
        comment_id: int,
        db: AsyncSession = Depends(get_db),
        user_id: int = Depends(get_current_user)
):
    result = await db.execute(
        select(CommentModel)
        .where(CommentModel.id == comment_id)
    )
    comment =  result.scalar_one_or_none()

    if not comment:
        raise HTTPException(
            status_code=404,
            detail='Post not found'
        )

    if comment.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail='Not your post'
        )
    await db.delete(comment)
    await db.commit()
    return {'message': 'Comment deleted'}