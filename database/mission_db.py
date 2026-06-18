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
    
    def get_open_missions_by_agent(self, id):
        conn = self.db.connection

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """SELECT * FROM missions
                WHERE assigned_agent_id = %s AND (status = IN_PROGRESS OR status = ASSIGNED)""",
                (id,)
            )
        
            return cursor.fetchall()

    def count_all_missions(self):
        conn = self.db.connection

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT COUNT(title) FROM missions")
            return cursor.fetchone()["COUNT(title)"]
    
    def count_by_status(self, status):
        conn = self.db.connection

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                "SELECT COUNT(status) FROM missions WHERE status = %s",
                (status,)
            )

            return cursor.fetchone()["COUNT(status)"]
        
    def count_open_missions(self):
        return self.count_by_status("IN_PROGRESS")

    def count_critical_missions(self):
        conn = self.db.connection

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """SELECT COUNT(risk_level) FROM missions
                WHERE risk_level = CRITICAL"""
            )

            return cursor.fetchone(["COUNT(risk_level)"])
        
    def get_top_agent(self):
        conn = self.db.connection

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(
                """SELECT * FROM missions
                WHERE status = COMPLETED AND (SELECT MAX(status) FROM missions)"""
            )

            return cursor.fetchall()
 

missions_db = MissionsDB(db, "missions")