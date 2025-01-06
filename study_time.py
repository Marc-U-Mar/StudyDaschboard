from database import Database
from datetime import datetime
from database_entity import DatabaseEntity

# Verwaltet Informationen zur Studienzeit eines Studierenden
class StudyTime(DatabaseEntity):
    def __init__(self, study_time_id=None, start_date=None, end_date=None, standard_duration_months=None,
                 current_semester=1):
        self.study_time_id = study_time_id
        self.start_date = start_date
        self.end_date = end_date
        self.standard_duration_months = standard_duration_months
        self.current_semester = current_semester

    @classmethod
    def from_db(cls, study_time_id):
        row = Database.fetch_one('SELECT * FROM StudyTime WHERE id = ?;', (study_time_id,))
        if row:
            return cls(*row)
        return None

    def save_to_db(self):
        Database.execute('''UPDATE StudyTime SET start_date = ?, standard_duration_months = ?, current_semester = ? 
                                    WHERE id = ?;''',
                         (self.start_date, self.standard_duration_months, self.current_semester, self.study_time_id))
        print(f"Study Time mit ID {self.study_time_id} wurde erfolgreich gespeichert.")

    # Berechnet die verbleibenden Monate bis zum Studienende
    def calculate_remaining_months(self):
        if self.end_date:
            end_date = datetime.strptime(self.end_date, "%Y-%m-%d")
            remaining_months = (end_date.year - datetime.now().year) * 12 + (end_date.month - datetime.now().month)
            return remaining_months if remaining_months > 0 else 0
        return 0