from fastapi import APIRouter, Depends
from bold_gen_backend.database.connection import get_session
from sqlmodel import Session
from bold_gen_backend.services.admin_service import get_all_users, require_admin
from bold_gen_backend.utils.security import get_token

router  = APIRouter(prefix="/admin",tags=["admin"])

@router.get('/')
def home():
    return {"message": "Admin Router"}

@router.get('/users')
def get_users(db: Session = Depends(get_session), token: str = Depends(get_token)):
    admin = require_admin(db, token)
    return get_all_users(db=db)

@router.get("/dashboard")
def admin_dashboard(db: Session = Depends(get_session), token: str = Depends(get_token)):
    admin = require_admin(db, token)
    return {"message": "Welcome to the admin dashboard"}

@router.get('/properties')
def get_all_properties():
    pass