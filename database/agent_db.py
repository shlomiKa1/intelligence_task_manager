from .db_connection import db
from .base_db import BaseDB


class AgentDB(BaseDB):
    def __init__(self, db, table_name):
        super().__init__(db, table_name)
    
    def create_agent(self, data):
        return self.create(data)
    
    def update_agent(self, id, data):
        return self.update(id, data)
    
    def get_all_agents(self):
        return self.get_all()
    
    def get_agent_by_id(self, id):
        return self.get_by_id(id)
    
    def deactivate_agent(self, id):
        conn = self.db.connection

        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE agent SET is_active = False WHERE id = %s",
                (id,)
            )
            if cursor.rowcount > 0:
                return {"message": f"ID '{id}' agent is deactivate"}
            return {"message": f"deactivate agent ID '{id}' faild"}