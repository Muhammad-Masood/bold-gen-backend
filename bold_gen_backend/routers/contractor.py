from fastapi import APIRouter

router  = APIRouter(prefix="/contractor",tags=["contractor"])

@router.get('/')
def home():
    return {"message": "Contractor Router"}