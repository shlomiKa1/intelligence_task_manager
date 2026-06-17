from .db_connection import ConnectionDB


class BaseDB:
    def __init__(self, db: ConnectionDB, table_name: str):
        self.db = db
        self.table_name = table_name

    def create(self, data):
        columns = ", ".join(data.key())
        placeparts = "%s".join(data.keys())
        conn = self.db.connection

        with conn.cursor() as cursor:
            cursor.execute(
                f"INSERT INTO {self.table_name} ({columns}) VALUES({placeparts})",
                tuple(data.values())
            )
            conn.commit()
            
            if cursor.lastrowid:
                return data
            return {"message": "Failed to created"}
    
        

