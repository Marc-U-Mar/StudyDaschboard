from database import Database
from database_entity import DatabaseEntity

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

    def update_study_time(self):
        print("Aktuelle Werte:")
        self.display()

        confirmation = input("Möchtest du etwas an deinen Studienzeiten überarbeiten? (yes/no): ").strip().lower()
        if confirmation != 'yes':
            print("Update Abgebrochen.")
            return

        new_start_date = input("Gib das Startdatum ein (YYYY-MM-DD) oder drücke Enter um zu überspringen: ")
        if new_start_date:
            self.start_date = new_start_date

        new_duration = input("Bitte gib deine Regelstudienzeit ein oder drücke Enter: ")
        if new_duration:
            self.standard_duration_months = int(new_duration)

        new_semester = input("Gib dein aktuelles Semester ein oder drücke Enter: ")
        if new_semester:
            self.current_semester = int(new_semester)

        if self.start_date and self.standard_duration_months:
            self.end_date = self.calculate_end_date(self.start_date, self.standard_duration_months)

        self.save_to_db()

    def display(self):
        print(f"Study Time ID: {self.study_time_id}, Start Date: {self.start_date}, End Date: {self.end_date}, "
              f"Standard Duration: {self.standard_duration_months}, Current Semester: {self.current_semester}")

    """
    def calculate_end_date(self, start_date, duration_months):
        # Berechnung des Enddatums basierend auf dem Startdatum und der Dauer in Monaten
        # ...
        pass
    """

    def save_to_db(self):
        Database.execute('''UPDATE StudyTime SET start_date = ?, standard_duration_months = ?, current_semester = ? 
                                    WHERE id = ?;''',
                         (self.start_date, self.standard_duration_months, self.current_semester, self.study_time_id))
        print(f"Study Time mit ID {self.study_time_id} wurde erfolgreich gespeichert.")