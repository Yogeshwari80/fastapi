from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId


class Agent(BaseModel):
    user_id: Optional[str]
    license_no: str
    agency_name: str
    experience_years: int
    rating: Optional[float] = None
    address: str


class AgentOut(Agent):
    id: str = Field(alias="_id")

    @classmethod
    def from_mongo(cls, agent):
        """Convert MongoDB document to Pydantic model"""
        agent["_id"] = str(agent["_id"])
        agent["user_id"] = str(agent["user_id"])
        return cls(**agent)