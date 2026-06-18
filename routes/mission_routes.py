from fastapi import APIRouter, HTTPException
from database.mission_db import missions_db
from .agent_routes import agent_by_id, agents_db
from logs.logger_config import logger
from services.service import check_status
from config import MAX_MISSIONS
from models.mission_model import Mission

router_missions = APIRouter()

@router_missions.post("")
def add_mission(data: Mission):
    created = missions_db.create_mission(data.model_dump())
    
    logger.info("Agent created successfully: id=%s", created["new_id"])
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
        logger.error("Mission not found: id=%s", id)
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
    
    logger.error("Mission not available: id=%s", id)
    raise HTTPException(400, "Mission not available")

@router_missions.put("/{id}/complete")
def complete_mission(id: int):
    mission = mission_by_id(id)

    logger.info("Chack if can complete mission")
    if check_status(mission, "IN_PROGRESS"):
        comleted = missions_db.update_mission_status(id, "COMPLETED")
        agents_db.increment_completed()
        logger.info("Mission ID '%s' comleted successfully", id)
        return comleted
    
    logger.error("Mission not available: id=%s", id)
    raise HTTPException(400, "Mission not available")

@router_missions.put("/{id}/fail")
def fail_mission(id: int):
    mission = mission_by_id(id)

    logger.info("Chack if can fail mission")
    if check_status(mission, "IN_PROGRESS"):
        failed = missions_db.update_mission_status(id, "FAILED")
        agents_db.increment_failed()
        logger.info("Mission ID '%s' failed successfully", id)
        return failed
    
    logger.error("Mission not available: id=%s", id)
    raise HTTPException(400, "Mission not available")

@router_missions.put("/{id}/cancel")
def cancel_mission(id: int):
    mission = mission_by_id(id)

    logger.info("Chack if can cancel mission")
    if check_status(mission, "NEW") or check_status(mission, "ASSIGNED"):
        cancelled = missions_db.update_mission_status(id, "CANCELLED")
        logger.info("Mission ID '%s' cancelled successfully", id)
        return cancelled
    
    raise HTTPException(400, "Mission not available")

@router_missions.put("/{id}/assign/{agent_id}")
def assign_mission_by_ids(id: int, agent_id: int):
    mission = mission_by_id(id)
    agent = agent_by_id(agent_id)

    if not check_status(mission, "NEW"):
        logger.error("Mission is not available: id=%s", id)
        raise HTTPException(400, "Mission not available")
    
    if not agent["is_active"]:
        logger.error("Agent is not active: id=%s", agent_id)
        raise HTTPException(400, "Agent is not active")
    
    if len(missions_db.get_open_missions_by_agent(id)) >= MAX_MISSIONS:
        logger.error("Agent has reached maximum missions: id=%s", agent_id)
        raise HTTPException(400, "Agent has reached maximum missions")
    
    if not (mission["risk_level"] == "CRITICAL" and agent["agent_rank"] == "Commander"):
        logger.error("Only Commander can handle critical missions: mission_id=%s, agent_id=%s", id, agent_id)
        raise HTTPException(400, "Only Commander can handle critical missions")

    assigned = missions_db.assign_mission(id, agent_id)

    logger.info("Mission '%s' assigned to agent '%s'", id, agent_id)
    return assigned