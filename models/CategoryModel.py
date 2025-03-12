


from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from bson import ObjectId

class Category(BaseModel):
    name: str
    description: str

class CategoryOut(Category):
    id: str = Field(alias="_id")

    @validator("id", pre=True, always=True)
    def convert_objectId(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
