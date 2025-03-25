from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class InquiryModel(BaseModel):
    fullname: str 
    email: EmailStr 
    phone_number: str
    property_type: str 
    listing_type: Optional[str]
    address: str 
    state_id: str
    city_id: str 
    area_id: str 
    budget: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    balconies: Optional[int] = None
    furnishing_status: Optional[str] = None
    parking_slot: Optional[int] = None
    message: Optional[str] = None

class InquiryOut(InquiryModel):
    id: str

    class Config:
        orm_mode = True
