from pydantic import BaseModel
from bson import ObjectId
from datetime import datetime

class Favourite(BaseModel):
    user_id: str
    property_id: str
    added_date: datetime = datetime.utcnow()

    class Config:
        orm_mode = True
