from database import Database

# Basisklasse für Entitäten, die in der Datenbank gespeichert werden
class DatabaseEntity:

    # peichert die Entität in der Datenbank
    # Diese Methode muss in den Unterklassen implementiert werden
    def save_to_db(self):
        raise NotImplementedError("Die Methode 'save_to_db' muss in der Unterklasse implementiert werden.")

    # Lädt eine Entität aus der Datenbank anhand ihrer ID
    @classmethod
    def from_db(cls, entity_id):
        row = Database.fetch_one(f'SELECT * FROM {cls.__name__} WHERE id = ?;', (entity_id,))
        if row:
            return cls(*row)
        return None

    #  Lädt alle Entitäten dieser Klasse aus der Datenbank in eine Liste
    @classmethod
    def fetch_all(cls):
        rows = Database.fetch_all(f'SELECT * FROM {cls.__name__};')
        return [cls(*row) for row in rows]