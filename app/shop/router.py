from fastapi import APIRouter

router = APIRouter(
    prefix='/shop',
    tags=['Shop']
)

@router.get('/')
def shop():
    return 'in development'