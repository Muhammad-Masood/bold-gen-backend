from fastapi import HTTPException, status, Depends
from bold_gen_backend.database.models.property import Property, PropertyImage, PropertyBase, PropertyListedMessage, PropertyMessage
from bold_gen_backend.database.models.user import User
from bold_gen_backend.database.connection import get_session
from bold_gen_backend.utils.security import get_token
from sqlmodel import Session, select
from uuid import UUID

def get_landlord_properties(user_id: UUID, db: Session):
    properties = db.exec(select(Property).where(Property.user_id == user_id)).all()
    return properties

def store_landlord_property(property: Property, user: User, db: Session):
    db.add(property)
    db.commit()
    db.refresh(property)
    return PropertyListedMessage(message="Your property has been listed successfully", property=property)

def get_property_by_id(property_id: UUID, db: Session):
    property = db.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    return property

def update_property(property_id: UUID, property_update: PropertyBase, user_id: UUID, db: Session):
    property = db.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    if property.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this property")

    for key, value in property_update.model_dump(exclude_unset=True).items():
        setattr(property, key, value)

    db.add(property)
    db.commit()
    db.refresh(property)
    return PropertyListedMessage(message="Property updated successfully", property=property)

def delete_property(property_id: UUID, user_id: UUID, db: Session):
    property = db.get(Property, property_id)
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")

    if property.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this property")

    db.delete(property)
    db.commit()
    return PropertyMessage(message="Property deleted successfully")