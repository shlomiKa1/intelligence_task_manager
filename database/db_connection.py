import mysql.connector
from config import CONNECTION, DATABASE


class ConnectionDB:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

        self.get_connect()
        self.create_database()
        self.create_tables()
    
    def get_connect(self):
        self._connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )

    @property
    def connection(self):
        if not self._connection.is_connected():
            self.get_connect()

        return self._connection
    
    def create_database(self):
        conn = self.connection
        with conn.cursor() as cursor:
            # f-string it's ok, because the users don't have access
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
            conn.commit()

    def create_tables(self):
        conn = self.connection

        with conn.cursor() as cursor:
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS agents(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        name VARCHAR(50) NOT NULL,
                        specialty VARCHAR(50) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        completed_missions INT DEFAULT 0,
                        failed_missions INT DEFAULT 0,
                        agent_rank ENUM("Junior", "Senior", "Commander")
                    )
                """
            )
            conn.commit()
        
            cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS missions(
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        title VARCHAR(75) NOT NULL,
                        description TEXT NOT NULL,
                        location VARCHAR(25) NOT NULL,
                        difficulty INT(10),
                        importance INT(10),
                        status ENUM("NEW", "ASSIGNED", "IN_PROGRESS", "COMPLETED", "FAILED", "CANCELLED"),
                        risk_level VARCHAR,
                        assigned_agent_id INT DEFAULT NULL
                    )
                """
            )
            conn.commit()