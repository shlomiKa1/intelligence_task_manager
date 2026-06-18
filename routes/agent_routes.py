from fastapi import APIRouter, HTTPException
from database.agent_db import agents_db
from logs.logger_config import logger

router_agents = APIRouter()

@router_agents.post("")
def add_agent(data: dict):
    logger.info("Go to database")
    added = agents_db.create_agent(data)

    if added["success"]:
        raise HTTPException(500, "Internal Server Error")
    logger.info("Agent created successfully: id=%s", added["id"])
    return added

@router_agents.get("")
def all_agents():
    agents = agents_db.get_all_agents()
    logger.info("Return '%s' agents", len(agents))
    return agents

