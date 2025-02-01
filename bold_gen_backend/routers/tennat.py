from fastapi import APIRouter

router  = APIRouter(prefix="/tennant",tags=["tennant"])

@router.get('/')
def home():
    return {"message": "Tennant Router"}