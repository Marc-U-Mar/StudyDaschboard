from database import Database
from database_entity import DatabaseEntity

class Module(DatabaseEntity):
    def __init__(self, module_id=None, module_name=None, grade=0.0, status="Pending", ects=5, study_program_id=None):
        self.module_id = module_id
        self.module_name = module_name
        self.grade = grade
        self.status = status
        self.ects = ects
        self.study_program_id = study_program_id

    def save_to_db(self):
        try:
            print(
                f"Speichere Modul: ID={self.module_id}, Name={self.module_name}, Note={self.grade}, Status={self.status}, ECTS={self.ects}, Study Program ID={self.study_program_id}")

            # Führe das Update aus
            Database.execute(
                '''UPDATE Module 
                SET module_name = ?, grade = ?, status = ?, ects = ?, study_program_id = ? 
                WHERE id = ?;''',
                (self.module_name, self.grade, self.status, self.ects, self.study_program_id, self.module_id)
            )
            print(f"Module mit ID {self.module_id} wurde erfolgreich gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern des Moduls: {e}")
            raise

    @classmethod
    def fetch_all(cls):
        return super().fetch_all()