from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
from bson import ObjectId



class InquiryBase(BaseModel):
    property_id: str = Field(..., description="ID of the property")
    user_id: str = Field(..., description="ID of the user")
    message: Optional[str] = None
    status: str = Field(default="Open", enum=["Open", "Resolved", "Closed"])
    inquiry_date: datetime = Field(default_factory=datetime.utcnow)



class InquiryOut(InquiryBase):
    id: str = Field(alias="_id")

    @validator("id", pre=True, always=True)
    def convert_objectid(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    @validator("property_id", "user_id", pre=True, always=True)
    def convert_objectid_fields(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
