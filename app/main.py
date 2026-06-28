from fastapi import FastAPI, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.cors import CORSMiddleware

from app.database import get_db
from app.posts.models import Post as PostModel
from app.admin.router import router as admin_router
from app.user.router import router as user_router
from app.posts.routers import router as posts_router
from app.shop.router import router as shop_router
from app.notifications.router import router as notification_router
from app.search.router import router as search_router


app = FastAPI(
    title='Society Node',
    description='The API for the Society Node social platform. Posting, comments, feed, internal economy (coins), and a perk and feature store.',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(admin_router)
app.include_router(user_router)
app.include_router(posts_router)
app.include_router(shop_router)
app.include_router(notification_router)
app.include_router(search_router)

@app.get('/')
@limiter.limit('50/1seconds')
async def home(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(PostModel))
    posts = result.scalars().all()
    return {'posts': posts}
