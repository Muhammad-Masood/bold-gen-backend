from fastapi import HTTPException, status, Depends
from database.models.user import User, UserLogin, Token, PasswordRecoverMessage, PasswordReset
from sqlmodel import Session, select
from utils.security import get_current_user
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def get_all_users(db: Session):
    users = db.exec(select(User)).all()
    return users

def require_admin(user=Depends(get_current_user)):
    if user["email"] != ADMIN_EMAIL:
        raise HTTPException(status_code=403, detail="Admin access required")
    return user