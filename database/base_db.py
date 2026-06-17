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
        
    def update(self, id, data):
        placeparts = ", ".join([f"{key} = %s" for key in data.keys()])
        conn = self.db.connection
        
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE {self.table_name} SET ({placeparts})",
                tuple(list(data.values()) + [id])
            )
            conn.commit()

            if cursor.rowcount > 0:
                return {"messege": f"ID '{id}' updated successfully"}
            return {"messege": f"ID '{id}' update failed"}
            
    def get_all(self):
        conn = self.db.connection
        
        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name}")
            return cursor.fetchall()
        
    def get_by_id(self, id):
        conn = self.db.connection

        with conn.cursor(dictionary=True) as cursor:
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE id = %s", (id,))
            return cursor.fetchone()