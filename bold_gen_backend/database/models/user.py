from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID
from typing import Optional
from pydantic import EmailStr

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4, index=True)
    full_name: str = Field(nullable=False, min_length=3, max_length=50)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, min_length = 4)

class UserLogin(SQLModel):
    email: EmailStr
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str

class PasswordRecoverMessage(SQLModel):
    message: str

class PasswordReset(SQLModel):
    token: str
    new_password: str