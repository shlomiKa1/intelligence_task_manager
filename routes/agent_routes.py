from fastapi import APIRouter, HTTPException
from database.agent_db import agents_db
from logs.logger_config import logger

router_agents = APIRouter()

@router_agents.post("")
def add_agent(data: dict):
    logger.info("Go to database")
    created = agents_db.create_agent(data)

    if created["success"]:
        raise HTTPException(500, "Internal Server Error")
    
    logger.info("Agent created successfully: id=%s", created["message"]["id"])
    return created

@router_agents.get("")
def all_agents():
    agents = agents_db.get_all_agents()
    logger.info("Return '%s' agents", len(agents))
    return agents

@router_agents.get("/{id}")
def agent_by_id(id: int):
    agent = agents_db.get_agent_by_id(id)

    if not agent:
        raise HTTPException(404, "Agent not found")
    
    logger.info("Return agent ID: %s", id)
    return agent

@router_agents.put("/{id}")
def edit_agent(id: int, data):
    updated = agents_db.update_agent(id, data)

    if not updated["success"]:
        raise HTTPException(404, "Agent not found")

    logger.info("Agent ID: %s updated successfully", id)
    return updated

@router_agents.put("/{id}/deactivate")
def deactivate_agent_by_id(id: int):
    agent_by_id(id)

    deactivate = agents_db.deactivate_agent(id)

    if not deactivate["success"]:
        raise HTTPException(404, "Agent not found")
    
    logger.info("Agent ID: %s deactivated", id)
    return deactivate

@router_agents.get("/{id}/performance")
def performance_agent(id: int):
    performance = agents_db.get_agent_performance(id)

    if not performance:
        raise HTTPException(404, "Agent not found")
    
    logger.info("Return performance agent by ID: %s", id)
    return performance