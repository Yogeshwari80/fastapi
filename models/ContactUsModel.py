from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactUs(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str
    created_at: Optional[datetime] = datetime.utcnow()
