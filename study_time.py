import sqlite3
from datetime import datetime, timedelta
import calendar


class StudyTime:
    def __init__(self, study_time_id=None, start_date=None, end_date=None, standard_duration_months=None,
                 current_semester=1):
        self.study_time_id = study_time_id

        # Überprüfen, ob start_date ein String ist und in datetime umwandeln
        if isinstance(start_date, str):
            self.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()  # Umwandlung in ein Date-Objekt
        elif isinstance(start_date, datetime):
            self.start_date = start_date.date()  # Nur das Datum behalten
        else:
            self.start_date = None  # Wenn None, setze auf None

        self.end_date = end_date
        self.standard_duration_months = standard_duration_months
        self.current_semester = current_semester
        self.current_date = datetime.now().strftime("%Y-%m-%d")  # Aktuelles Datum in YYYY-MM-DD Format

    @classmethod
    def from_db(cls, study_time_id):
        conn = sqlite3.connect('StudyDashboard.sql')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM StudyTime WHERE id = ?;', (study_time_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None

    def update_study_time(self):
        print("Aktuelle Werte:")
        self.display()

        # Abfrage, ob die Daten aktualisiert werden sollen
        confirmation = input("Möchtest du etwas an deinen Studienzeiten überarbeiten? (yes/no): ").strip().lower()
        if confirmation != 'yes':
            print("Update Abgebrochen.")
            return

        # Input for start_date
        new_start_date = input("Gib das Startdatum ein (YYYY-MM-DD) oder drücke Enter um zu überspringen: ")
        if new_start_date:
            self.start_date = datetime.strptime(new_start_date, "%Y-%m-%d").date()  # Nur Datum, keine Zeit

        # Input for standard_duration_months
        new_duration = input("Bitte gib deine Regelstudienzeit ein oder drücke Enter: ")
        if new_duration:
            self.standard_duration_months = int(new_duration)

        # Input for current_semester
        new_semester = input("Gib dein aktuelles Semester ein oder drücke Enter: ")
        if new_semester:
            self.current_semester = int(new_semester)

        # Calculate end_date
        if self.start_date and self.standard_duration_months is not None:
            self.end_date = self.calculate_end_date(self.start_date.strftime("%Y-%m-%d"), self.standard_duration_months)

        # Update the database
        self.save_to_db()

    def display(self):
        # Das start_date wird nun als YYYY-MM-DD formatiert
        print(f"Study Time ID: {self.study_time_id}, Start Date: {self.start_date}, End Date: {self.end_date}, "
              f"Standard Duration: {self.standard_duration_months}, Current Semester: {self.current_semester},"
              f" Current Date: {self.current_date}")

    def calculate_end_date(self, start_date, duration_months):
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")

        # Berechnung des Enddatums basierend auf der Regelstudienzeit in Monaten
        end_year = start_date_obj.year
        end_month = start_date_obj.month + duration_months

        # Berechnung des richtigen Jahres und Monats
        if end_month > 12:
            end_year += end_month // 12
            end_month = end_month % 12 if end_month % 12 != 0 else 12

        # Letzter Tag des Monats berechnen
        if end_month == 1:
            end_year -= 1
            end_month = 12
        else:
            end_month -= 1

        last_day_of_month = calendar.monthrange(end_year, end_month)[1]

        # Setze das Enddatum auf den letzten Tag des Monats
        return f"{end_year}-{end_month:02d}-{last_day_of_month}"

    def save_to_db(self):
        conn = sqlite3.connect('StudyDashboard.sql')
        cursor = conn.cursor()
        cursor.execute('''UPDATE StudyTime 
                          SET start_date = ?, standard_duration_months = ?, current_semester = ? 
                          WHERE id = ?;''',
                       (self.start_date.strftime("%Y-%m-%d") if self.start_date else None,
                        self.standard_duration_months if self.standard_duration_months is not None else 0,
                        self.current_semester if self.current_semester is not None else 1,
                        self.study_time_id))  # Füge die ID hinzu, um die richtige Zeile zu aktualisieren
        conn.commit()
        conn.close()
        print("Studienzeit wurde erfolgreich aktualisiert.")
