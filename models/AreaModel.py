
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from bson import ObjectId

class Area(BaseModel):
    name: str
    city_id: Optional[str]  # Ensure city_id is a string

class AreaOut(Area):
    id: str = Field(alias="_id")
    city: Optional[Dict[str, Any]] = None    

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        """ Convert ObjectId to string for MongoDB _id """
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("city_id", pre=True, always=True)
    def convert_city_id(cls, v):
        """ Convert ObjectId to string for city_id """
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("city", pre=True, always=True)
    def convert_city(cls, v):
        """ Convert city ObjectId to string """
        if isinstance(v, dict) and "_id" in v:
            v["_id"] = str(v["_id"])
        return v
