from fastapi import APIRouter
from controllers.AgentController import add_agent, get_agents, get_agent_by_id, delete_agent
from models.AgentModel import Agent

router = APIRouter()

@router.post("/agent/")
async def create_agent(agent: Agent):
    return await add_agent(agent)

@router.get("/agents/")
async def list_agents():
    return await get_agents()

@router.get("/agent/{agent_id}/")
async def fetch_agent(agent_id: str):
    return await get_agent_by_id(agent_id)

@router.delete("/agent/{agent_id}/")
async def remove_agent(agent_id: str):
    return await delete_agent(agent_id)
