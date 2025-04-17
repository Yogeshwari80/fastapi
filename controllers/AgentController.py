from models.AgentModel import Agent, AgentOut
from bson import ObjectId
from config.database import agent_collection, user_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse


async def add_agent(agent: Agent):
   
    if not ObjectId.is_valid(agent.user_id):
        raise HTTPException(status_code=400, detail="Invalid user_id format")

    agent_dict = agent.dict()
    agent_dict["user_id"] = ObjectId(agent.user_id)

    result = await agent_collection.insert_one(agent_dict)
    if result.inserted_id:
        return JSONResponse(status_code=201, content={"message": "Agent created successfully"})
    raise HTTPException(status_code=500, detail="Failed to create agent")


async def get_agents():
    agents = await agent_collection.find().to_list(None)
    return [AgentOut.from_mongo(agent) for agent in agents]


async def get_agent_by_id(agent_id: str):
    if not ObjectId.is_valid(agent_id):
        raise HTTPException(status_code=400, detail="Invalid agent ID")

    agent = await agent_collection.find_one({"_id": ObjectId(agent_id)})
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    return AgentOut.from_mongo(agent)


async def delete_agent(agent_id: str):
    if not ObjectId.is_valid(agent_id):
        raise HTTPException(status_code=400, detail="Invalid agent ID")

    result = await agent_collection.delete_one({"_id": ObjectId(agent_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found")

    return {"message": "Agent deleted successfully"}
