from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID
from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr
# from .property import Property

if TYPE_CHECKING:
    from .property import Property

# User Model

class UserRoleLink(SQLModel, table=True):
    user_id: UUID = Field(foreign_key="user.id", primary_key=True)
    role_id: UUID = Field(foreign_key="userrole.id", primary_key=True)

class UserRole(SQLModel, table=True):
    id: UUID = Field(primary_key=True, default_factory=uuid4, index=True)
    name: str = Field(nullable=False, unique=True)
    users: list["User"] = Relationship(back_populates="roles", link_model=UserRoleLink)

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4, index=True)
    full_name: str = Field(nullable=False, min_length=3, max_length=50)
    email: EmailStr = Field(nullable=False, unique=True, index=True)
    password: str = Field(nullable=False, min_length = 4)
    roles: list["UserRole"] = Relationship(back_populates="users", link_model=UserRoleLink)
    properties: list["Property"] = Relationship(back_populates="user")

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
