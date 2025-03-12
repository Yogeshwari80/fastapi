
from pydantic import BaseModel, Field, validator
from typing import Optional, List,Dict,Any
from bson import ObjectId
from fastapi import File, UploadFile,Form

class Property(BaseModel):
    property_name: str 
    category_id: str

    listing_type: str 
    
    base_price: float
    negotiable: Optional[bool]
    address: str
    state_id: str 
    city_id: str 
    area_id: Optional[str]
    landmarks: Optional[str] 
    maps_link: Optional[str]
    built_up_area: Optional[float] 
    carpet_area: Optional[float]
    bedrooms: Optional[int] 
    bathrooms: Optional[int] 
    balconies: Optional[int] 
    furnishing: Optional[str] 
    age_of_property: Optional[int] 
    floor_no: Optional[int] 
    total_floors: Optional[int] 
    facing: Optional[str]
    parking_slots: Optional[int]
    amenities: Optional[List[str]] 
    property_images: Optional[List[str]] = []
    image: UploadFile = File(...)  # Accepting file upload

   

   

   
    @validator("city_id", pre=True, always=True)
    def convert_city_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

class PropertyOut(Property):
    id: str = Field(..., alias="_id")
    category: Optional[Dict[str, Any]] = None
    city: Optional[Dict[str, Any]] = None
    state: Optional[Dict[str, Any]] = None 
    class Config:
        orm_mode = True
