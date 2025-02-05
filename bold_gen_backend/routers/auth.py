from fastapi import APIRouter
from services.auth_service import store_new_user, login_user_for_access_token, get_user_by_email, recover_user_password, reset_user_password
from database.models.user import User, UserLogin, Token
from database.connection import get_session
from fastapi import Depends
from sqlmodel import Session

router  = APIRouter(prefix="/auth",tags=["auth"])

@router.get('/')
def home():
    return {"message": "User Authentication Router"}

@router.post('/signup')
def create_user(user: User, db: Session = Depends(get_session)):
    store_new_user(session=db, user=user)
    return {"message": "User created successfully"}

@router.post('/login')
def login_user(user: UserLogin, db: Session = Depends(get_session)):
    token: Token = login_user_for_access_token(user=user, db=db)
    return token

@router.post('/forget-password')
def forget_password(user: UserLogin, db: Session = Depends(get_session)):
    return recover_user_password(user=user, db=db)

@router.post('/reset-password')
def reset_password(user: UserLogin, db: Session = Depends(get_session)):
    return reset_user_password(user=user, db=db)
