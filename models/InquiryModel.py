from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId

class InquiryModel(BaseModel):
    fullname: str 
    email: EmailStr 
    phone_number: str
    message: Optional[str] = None

class InquiryOut(InquiryModel):
    id: str

    class Config:
        orm_mode = True

