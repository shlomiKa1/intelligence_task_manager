from fastapi import APIRouter, HTTPException
from database.mission_db import missions_db
from database.agent_db import agents_db
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

@router_missions.get("/{id}")
def mission_by_id(id: int):
    mission = missions_db.get_mission_by_id(id)

    if not mission:
        raise HTTPException(404, "Mission not found")
    
    logger.info("Return mission by ID: %s", id)
    return mission

@router_missions.put("/{id}/start")
def start_mission(id: int):
    mission = mission_by_id(id)

    logger.info("Chack if can start mission")
    if check_status(mission, "ASSIGNED"):
        started = missions_db.update_mission_status(id, "IN_PROGRESS")
        logger.info("Mission ID '%s' start successfully", id)
        return started
    
    raise HTTPException(400, "Mission not available")

@router_missions.put("/{id}/complate")
def complate_mission(id: int):
    mission = mission_by_id(id)

    if check_status(mission, "IN_PROGRESS"):
        comleted = missions_db.update_mission_status(id, "COMPLETED")
        logger.info("Mission ID '%s' comleted successfully", id)
        return comleted
    
    raise HTTPException(400, "Mission not available")

@router_missions.put("/{id}/fail")
def fail_mission(id: int):
    mission = mission_by_id(id)

    if check_status(mission, "IN_PROGRESS"):
        failed = missions_db.update_mission_status(id, "FAILED")
        logger.info("Mission ID '%s' failed successfully", id)
        return failed
    
    raise HTTPException(400, "Mission not available")

@router_missions.put("/{id}/cancel")
def cancel_mission(id: int):
    mission = mission_by_id(id)

    if check_status(mission, "NEW") or check_status(mission, "ASSIGNED"):
        cancelled = missions_db.update_mission_status(id, "CANCELLED")
        logger.info("Mission ID '%s' cancelled successfully", id)
        return cancelled
    
    raise HTTPException(400, "Mission not available")

def check_status(mission, status):
    return mission["status"] == status

