from fastapi import APIRouter
router = APIRouter(
    prefix='/violations',
    tags=['Violations']
)

@router.get('/')
def all_violations():
    return 'in development'