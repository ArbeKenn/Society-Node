from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database import create_tables, get_db

from app.user.router import router as user_router
from app.posts.router import router as post_router
from app.posts.models import Post as PostModel
from app.shop.router import router as shop_router


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
app.include_router(post_router)
app.include_router(shop_router)

@app.get('/')
def home(db: Session = Depends(get_db)):
    posts = db.query(PostModel).order_by(PostModel.id.desc()).limit(10).all()
    return {
        'latest_posts': posts,
    }
