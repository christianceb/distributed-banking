from sqlite3 import Connection
from typing import Optional


class AuthIdentityService:
    db_context: Connection = None

    def __init__(self, db_context: Connection):
        self.db_context = db_context

    def validate_user(self, username, password) -> Optional[int]:
        db = self.db_context

        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))

        db.commit()

        rows = cursor.fetchall()

        if (len(rows) > 1):
            return rows[0].id
        else:
            return None
