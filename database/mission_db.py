from .db_connection import db
from .base_db import BaseDB
from services.service import calculate_risk_level


class MissionsDB(BaseDB):
    def __init__(self, db, table_name):
        super().__init__(db, table_name)

    
    def create_mission(self, data):
        level = (data["difficulty"] * 2) + data["importance"]
        calculate_level = calculate_risk_level(level)
        data = {**data, "risk_level": calculate_level}

        return self.create(data)
    
    def update_mission_status(self, id, status):
        if self.update(id, status):
            return {"message": f"ID '{id}' status mission updated successfully"}
        return {"message": f"Update - status mission ID '{id}' failed"}
    
    def get_all_missions(self):
        return self.get_all()
    
    def get_mission_by_id(self, id):
        return self.get_by_id(id)
    
    def assign_mission(self, m_id, a_id):
        agent_id = {"assigned_agent_id": a_id}

        if self.update(m_id, agent_id):
            return {"succes": True, "message": f"Assign mission ID '{m_id}' to agent ID '{a_id}' success"}
        return {"succes": False, "message": f"Assign mission ID '{m_id}' to agent ID '{a_id}' failed"}
