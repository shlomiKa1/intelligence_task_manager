from fastapi import APIRouter, HTTPException
from database.mission_db import missions_db
from logs.logger_config import logger


router_missions = APIRouter()

router_missions.post("")
def add_mission(data):
    created = missions_db.create_mission(data)

    if not created["success"]:
        raise HTTPException(500, "Internal Server Error")
    
    logger.info("Agent created successfully: id=%s", created["message"]["id"])
    return created

router_missions.get("")
def all_missions():
    missions = missions_db.get_all_missions()
    
    logger.info("Return '%s' missions", len(missions))
    return missions
