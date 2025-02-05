from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
import os
from dataclasses import dataclass
import secrets
from email.mime.text import MIMEText
import smtplib
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
# SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
EMAIL_RESET_TOKEN_EXPIRE_MINUTES= 60
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "your-email@example.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "your-email-password")
PROJECT_NAME = os.getenv("PROJECT_NAME")
CLIENT_URL = os.getenv("CLIENT_URL")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

@dataclass
class EmailData:
    html_content: str
    subject: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> str | None:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return email
    except jwt.PyJWTError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload:dict = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"email": email}
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=EMAIL_RESET_TOKEN_EXPIRE_MINUTES)
    now = datetime.now(timezone.utc)
    expires = now + delta
    encoded_jwt = jwt.encode(
        {"exp": expires, "nbf": now, "sub": email},
        key=SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt

def verify_password_reset_token(token: str) -> str:
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")  # Return email if valid
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
    
def generate_reset_password_email(email_to: str, email: str, token: str) -> EmailData:
    subject = f"{PROJECT_NAME} - Password recovery for user {email}"
    reset_url = f"${CLIENT_URL}/reset-password?token={token}"
    html_content = f"""
    <html>
    <body>
        <p>Hello {email},</p>
        <p>You requested a password reset. Click the link below to reset your password:</p>
        <a href="{reset_url}">Reset Password</a>
        <p>This link will expire in 15 minutes.</p>
    </body>
    </html>
    """
    return {"subject": subject, "html_content": html_content}

def send_email(email_to: str, subject: str, html_content: str):
    msg = MIMEText(html_content, "html")
    msg["Subject"] = subject
    msg["From"] = SMTP_USER
    msg["To"] = email_to

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, email_to, msg.as_string())