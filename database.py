import sqlite3

# Stellt statische Methoden für Datenbankoperationen bereit
class Database:

    # Stellt eine Verbindung zur SQLite-Datenbank her
    @staticmethod
    def get_connection():
        return sqlite3.connect('StudyDashboard.sql')

    # Führt eine SELECT-Abfrage aus und gibt alle Ergebnisse zurück
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

    # Führt eine SQL-Abfrage aus und committet die Änderungen
    @staticmethod
    def execute(query, params=()):
        conn = Database.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    # Speichert eine Liste von Entitäten in der Datenbank
    @staticmethod
    def save_all_entities(entities):
        for entity in entities:
            entity.save_to_db()