from sqlite3 import Connection
import sqlite3
from typing import Optional


class BankingService:
    db_context: Connection = None

    def __init__(self):
        pass

    def get_transactions(self, account_id):
        pass

    def init_data_store(self) -> sqlite3.Connection:
        self.db_connection = sqlite3.connect("store.db", isolation_level=None)
        self.db_connection.row_factory = sqlite3.Row
        return self.db_connection

    def close_data_store_connection(self):
        self.db_connection.close()

    def validate_user(self, username, password) -> Optional[int]:
        connection = self.init_data_store()

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

        connection.commit()

        rows = cursor.fetchall()

        self.close_data_store_connection()

        if (len(rows)):
            return rows[0]['id']
        else:
            return None
