from fastapi import APIRouter, Depends
from database.connection import get_session
from sqlmodel import Session
from services.admin_service import get_all_users, require_admin

router  = APIRouter(prefix="/admin",tags=["admin"])

@router.get('/')
def home():
    return {"message": "Admin Router"}

@router.get('/')
def get_users(db: Session = Depends(get_session)):
    return get_all_users(db=db)

@router.get("/dashboard")
def admin_dashboard(admin=Depends(require_admin)):
    return {"message": "Welcome to the admin dashboard"}