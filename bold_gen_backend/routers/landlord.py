from fastapi import APIRouter, Depends
from uuid import UUID
from bold_gen_backend.services.landlord_service import get_landlord_properties, store_landlord_property, get_property_by_id, delete_property, update_property
from bold_gen_backend.database.connection import get_session, Session
from bold_gen_backend.database.models.property import Property, PropertyBase
from bold_gen_backend.database.models.user import User
from bold_gen_backend.services.auth_service import get_current_user
from bold_gen_backend.utils.security import get_token
from typing import Annotated

router  = APIRouter(prefix="/landlord",tags=["Landlord Properties"])

@router.get('/')
def home():
    return {"message": "Landlord Router"}

# Property Management

# Get all properties
@router.get('/properties/{user_id}')
def get_properties(user_id: UUID, db: Session = Depends(get_session)):
    properties = get_landlord_properties(user_id=user_id, db=db)
    return properties

# List Property for Sell
@router.post('/properties/list')
def list_property(property: Property, db: Session = Depends(get_session), token: str = Depends(get_token)):
    user = get_current_user(db, token)
    response = store_landlord_property(property=property, user=user, db=db)
    return response

# # Get property by id
@router.get("/properties/{property_id}")
def get_property(property_id: UUID, session: Session = Depends(get_session)):
    property = get_property_by_id(property_id=property_id, db=session)
    return property

# Update Property listed for sale
@router.put("/properties/update/{property_id}")
def update_landlord_property(
    property_id: UUID,
    property_update: PropertyBase,
    db: Session = Depends(get_session),
    token: str = Depends(get_token)
):
    user = get_current_user(db, token)
    update_response = update_property(property_id,property_update,user_id=user.id, db=db)
    return update_response

# # Delete the listed property
@router.delete("/properties/delete/{property_id}")
def delete_landlord_property(property_id: UUID, db: Session = Depends(get_session), token: str = Depends(get_token)):
    user = get_current_user(db, token)
    response = delete_property(property_id=property_id, user_id=user.id, db=db)
    return response