from fastapi import APIRouter
from app.posts.routers.posts import router as posts_router
from app.posts.routers.comments import router as comments_router

router = APIRouter(
    prefix='/posts',
    tags=['Publications']
)
router.include_router(posts_router)
router.include_router(comments_router)