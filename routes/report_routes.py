from fastapi import APIRouter, HTTPException
# from .agent_routes import agent_by_id, agents_db
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
