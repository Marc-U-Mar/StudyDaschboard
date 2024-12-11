import sqlite3

class Database:
    @staticmethod
    def get_connection():
        return sqlite3.connect('StudyDashboard.sql')

    @staticmethod
    def fetch_all(query, params=()):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def fetch_one(query, params=()):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()
        return row

    @staticmethod
    def execute(query, params=()):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()