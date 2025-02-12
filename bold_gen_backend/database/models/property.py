from sqlmodel import Field, SQLModel, Relationship
from uuid import uuid4, UUID
from typing import Optional, List, TYPE_CHECKING
# from bold_gen_backend.database.models.user import User
# from pydantic import HttpUrl

if TYPE_CHECKING:
    from .user import User

# Property Model

class PropertyImage(SQLModel, table = True):
    id: UUID = Field(primary_key=True, default_factory=uuid4, index=True)
    url: str = Field(nullable=False)
    property_id: UUID = Field(foreign_key="property.id", nullable=False)
    property: Optional["Property"] = Relationship(back_populates="images")

class PropertyBase(SQLModel):
    title: Optional[str] = Field(default=None, min_length=3)
    location: Optional[str] = Field(default=None, min_length=3)
    property_type: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = Field(default=None, min_length=3)
    furnish_status: Optional[str] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    is_parking_available: Optional[bool] = Field(default=False)

class Property(PropertyBase, table=True):
    id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4, index=True)
    user_id: UUID = Field(foreign_key="user.id", nullable=False)
    user: Optional["User"] = Relationship(back_populates="properties")
    images: List["PropertyImage"] = Relationship(back_populates="property")
    price: int
    is_sold: bool = Field(default=False)

# class PropertyRent(PropertyBase, table=True):
#     id: Optional[UUID] = Field(primary_key=True, default_factory=uuid4, index=True)
#     user_id: UUID = Field(foreign_key="user.id", nullable=False)
#     user: User | None = Relationship(back_populates="properties")
#     images: List["PropertyImage"] = Relationship(back_populates="property")
#     price: int
#     is_sold: bool = Field(default=False)

class PropertyMessage(SQLModel):
    message: str

class PropertyListedMessage(SQLModel):
    property: Property
    message: str
