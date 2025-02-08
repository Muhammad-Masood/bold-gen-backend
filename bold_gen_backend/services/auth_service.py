from fastapi import HTTPException, status, Depends
from database.models.user import User, UserLogin, Token, PasswordRecoverMessage, PasswordReset
from sqlmodel import Session, select
from utils.security import hash_password, verify_password, create_access_token, generate_password_reset_token, generate_reset_password_email, send_email, verify_password_reset_token, get_token, verify_token
import jwt

def get_current_user(db: Session, token: str = Depends(get_token)):
    try:
        email = verify_token(token)
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_email(email=email, db=db)
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_user_by_email(email: str, db: Session) -> User:
    user = db.exec(select(User).where(User.email == email)).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def store_new_user(db: Session, user: User):
    existing_user = get_user_by_email(user.email, db)
    print(existing_user)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed_password: str = hash_password(user.password)
    new_user = User(full_name=user.full_name, email=user.email, password=hashed_password)
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

def authenticate_user(user: UserLogin, db: Session):
    user_found: User = get_user_by_email(user.email, db)
    if not verify_password(user.password, user_found.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},)
    return user_found

def login_user_for_access_token(user: UserLogin, db: Session) -> Token:
    user = authenticate_user(user, db)
    access_token = create_access_token({"sub": user.email})
    token: Token = Token(access_token=access_token, token_type="bearer")
    return token

def recover_user_password(user: UserLogin, db: Session) -> PasswordRecoverMessage:
    """
    Password Recovery: Generate a password reset token and send an email
    """
    user = get_user_by_email(email=user.email, db=db)
    user_email = user.email
    password_reset_token = generate_password_reset_token(email=user_email)
    email_data = generate_reset_password_email(
        email_to=user.email, email=user_email, token=password_reset_token
    )
    send_email(
        email_to=user.email,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return PasswordRecoverMessage(message="Password recovery email sent")

def reset_user_password(data: PasswordReset, db: Session) -> PasswordRecoverMessage:
    """
    Reset Password: Validate token and update password.
    """
    email = verify_password_reset_token(data.token)
    if not email:
        return PasswordRecoverMessage(message="Invalid or expired token")

    user = get_user_by_email(email=email, db=db)
    if not user:
        return PasswordRecoverMessage(message="User not found")

    # Hash new password and update user
    user.password = hash_password(data.new_password)
    db.add(user)
    db.commit()
    db.refresh(user)

    return PasswordRecoverMessage(message="Password reset successfully")
