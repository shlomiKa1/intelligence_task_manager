from fastapi import APIRouter
from .mission_routes import missions_db, agents_db
from logs.logger_config import logger


router_reports = APIRouter()

@router_reports.get("/summary")
def get_summary():
    logger.info("Retrun summary report")
    return {
        "active_agents_count": agents_db.count_active_agents(),
        "total_missions": missions_db.count_all_missions(),
        "open_missions": missions_db.count_open_missions(),
        "completed_missions": missions_db.count_by_status("COMPLETED"),
        "failed_missions": missions_db.count_by_status("FAILED"),
        "critical_missions": missions_db.count_critical_missions()
    }

@router_reports.get("/missions-by-status")
def get_missions_by_status():
    logger.info("Return statuses of missions")
    
    return {
        "open": missions_db.count_by_status("ASSIGNED"),
        "in_progress": missions_db.count_by_status("IN_PROGRESS"),
        "completed": missions_db.count_by_status("COMPLETED"),
        "failed": missions_db.count_by_status("FAILED"),
        "critical": missions_db.count_critical_missions()    
    }

@router_reports.get("/top_agent")
def get_top_agent():
    logger.info("Check top agent in database")
    agents = missions_db.get_top_agent()

    logger.info("Return '%s' top agents", len(agents))
    return agents