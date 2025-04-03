from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from bson import ObjectId
from fastapi import File, UploadFile

class Property(BaseModel):
    property_name: Optional[str]
    category_id: Optional[str]
    listing_type: Optional[str] 
    base_price: Optional[float]
    negotiable: Optional[bool]
    address: Optional[str]
    state_id: Optional[str]
    city_id: Optional[str]
    area_id: Optional[str]
    landmarks: Optional[str]
    maps_link: Optional[str]
    user_id: Optional[str]
    built_up_area: Optional[float]
    carpet_area: Optional[float]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    balconies: Optional[int]
    furnishing: Optional[str]
    age_of_property: Optional[int]
    facing: Optional[str]
    floor_no: Optional[int]
    total_floors: Optional[int]
    parking_slots: Optional[int]
    image_url: Optional[str] = None  # Cloudinary/Image Path
    image: UploadFile = File(...)  # File Upload

class PropertyOut(BaseModel):
    id: str = Field(alias="_id")
    property_name: Optional[str]
    category_id: Optional[str]
    listing_type: Optional[str]
    base_price: Optional[float]
    negotiable: Optional[bool]
    address: Optional[str]
    state_id: Optional[str]
    city_id: Optional[str]
    area_id: Optional[str]
    landmarks: Optional[str]
    maps_link: Optional[str]
    user_id: Optional[str]
    built_up_area: Optional[float]
    carpet_area: Optional[float]
    bedrooms: Optional[int]
    bathrooms: Optional[int]
    balconies: Optional[int]
    furnishing: Optional[str]
    age_of_property: Optional[int]
    facing: Optional[str]
    floor_no: Optional[int]
    total_floors: Optional[int]
    parking_slots: Optional[int]
    image_url: Optional[str] = None
    category: Optional[Dict[str, Any]] = None
    user: Optional[Dict[str, Any]] = None
    area: Optional[Dict[str, Any]] = None

    @validator("id", "category_id", "state_id", "city_id", "area_id", "user_id", pre=True, always=True)
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
