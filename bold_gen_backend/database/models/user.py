from sqlmodel import Field, SQLModel
from uuid import uuid4, UUID
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4)
    email: str = Field(nullable=False)
    password: str = Field(nullable=False)
