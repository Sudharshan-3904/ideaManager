import sqlite3
from components.idea import Idea

CONNECTED_DB = None

class DBHandler:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        return self.conn

    def close(self):
        self.conn.close()

    def execute(self, query, params=()):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        self.close()

    def fetchall(self, query, params=()):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        self.close()
        return rows

    def fetchone(self, query, params=()):
        self.connect()
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        self.close()
        return row