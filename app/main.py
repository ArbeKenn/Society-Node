from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import create_tables, get_db
from app.posts.models import Post as PostModel

from app.user.router import router as user_router
from app.posts.routers import router as posts_router
from app.shop.router import router as shop_router
from app.notifications.router import router as notification_router
from app.search.router import router as search_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield

app = FastAPI(
    title='Society Node',
    description='The API for the Society Node social platform. Posting, comments, feed, internal economy (coins), and a perk and feature store.',
    version='0.4.0',
    lifespan=lifespan,
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(user_router)
app.include_router(posts_router)
app.include_router(notification_router)
app.include_router(shop_router)
app.include_router(search_router)

@app.get('/')
@limiter.limit('1/sec')
async def home(
        request: Request,
        db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PostModel))
    posts = result.scalars().all()
    return {
        'latest_posts': posts,
    }
