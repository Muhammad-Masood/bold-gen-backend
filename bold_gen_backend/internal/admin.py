from fastapi import APIRouter

router  = APIRouter(prefix="/admin",tags=["admin"])

@router.get('/')
def home():
    return {"message": "Admin Router"}