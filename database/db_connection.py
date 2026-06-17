import mysql.connector
from config import CONNECTION, DATABASE


class ConnectionDB:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

        self.get_connect()
    
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