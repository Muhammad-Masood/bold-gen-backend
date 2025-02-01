from fastapi import APIRouter

router  = APIRouter(prefix="/buyer",tags=["buyer"])

@router.get('/')
def home():
    return {"message": "Buyer Router"}