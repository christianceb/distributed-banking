import sqlite3


def database() -> sqlite3.Connection:
    connection = sqlite3.connect("store.db", isolation_level=None)
    connection.row_factory = sqlite3.Row
    
    return connection
