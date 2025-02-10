from fastapi import HTTPException, status, Depends
from database.models.user import User, UserLogin, Token, PasswordRecoverMessage, PasswordReset
from sqlmodel import Session, select
from services.auth_service import get_current_user
import os
from dotenv import load_dotenv
from database.connection import get_session

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def get_all_users(db: Session):
    users = db.exec(select(User)).all()
    return users

def require_admin(db: Session, token: str):
    user = get_current_user(db, token)
    if user.email != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user