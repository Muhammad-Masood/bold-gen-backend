from fastapi import APIRouter

router  = APIRouter(prefix="/landlord",tags=["landlord"])

@router.get('/')
def home():
    return {"message": "Landlord Router"}