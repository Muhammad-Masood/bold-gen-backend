from fastapi import APIRouter
from services.auth_service import store_new_user, login_user_for_access_token, get_user_by_email, recover_user_password, reset_user_password, authenticate_user
from database.models.user import User, UserLogin, Token
from database.connection import get_session
from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer

router  = APIRouter(prefix="/auth",tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.get('/')
def home():
    return {"message": "User Authentication Router"}

@router.post('/signup')
def create_user(user: User, db: Session = Depends(get_session)):
    store_new_user(db=db, user=user)
    return {"message": "User created successfully"}

@router.post('/login')
def login_user(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_session)):
    print(form_data.username, form_data.password)
    token: Token = login_user_for_access_token(user=UserLogin(email=form_data.username, password=form_data.password), db=db)
    response = JSONResponse(token.model_dump())    
    response.set_cookie(key="Authorization", value=f"Bearer {token.access_token}", httponly=True)
    return response

@router.post('/forget-password')
def forget_password(user: UserLogin, db: Session = Depends(get_session)):
    return recover_user_password(user=user, db=db)

@router.post('/reset-password')
def reset_password(user: UserLogin, db: Session = Depends(get_session)):
    return reset_user_password(user=user, db=db)
