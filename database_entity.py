from database import Database

class DatabaseEntity:
    def save_to_db(self):
        raise NotImplementedError("Die Methode 'save_to_db' muss in der Unterklasse implementiert werden.")

    @classmethod
    def from_db(cls, entity_id):
        row = Database.fetch_one(f'SELECT * FROM {cls.__name__} WHERE id = ?;', (entity_id,))
        if row:
            return cls(*row)
        return None

    @classmethod
    def fetch_all(cls):
        rows = Database.fetch_all(f'SELECT * FROM {cls.__name__};')
        return [cls(*row) for row in rows]