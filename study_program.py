import sqlite3
from datetime import datetime
from database import Database

class StudyProgram:
    def __init__(self, program_id=None, program_name=None, current_gpa=0.0, total_ects=0, collected_ects=0,
                 monthly_module_load=0, study_time_id=None):
        self.program_id = program_id
        self.program_name = program_name
        self.current_gpa = current_gpa
        self.total_ects = total_ects
        self.collected_ects = collected_ects
        self.monthly_module_load = monthly_module_load
        self.study_time_id = study_time_id

    @classmethod
    def from_db(cls, program_id):
        row = Database.fetch_one('SELECT * FROM StudyProgram WHERE id = ?;', (program_id,))
        if row:
            return cls(*row)
        return None

    def display(self):
        print(f"Program ID: {self.program_id}, Name: {self.program_name}, GPA: {self.current_gpa}, "
              f"Total ECTS: {self.total_ects}, Collected ECTS: {self.collected_ects}, "
              f"Monthly Module Load: {self.monthly_module_load}")

    @staticmethod
    def calculate_done_modules_gpa():
        result = Database.fetch_one('''
                SELECT AVG(grade) FROM Module
                WHERE status = 'Done' AND grade > 0.0
            ''')
        if result:
            average_gpa = result[0]
            if average_gpa is not None:
                print(f"Durchschnitt der Noten für deine Module lautet: {average_gpa:.2f}")
                return average_gpa
            else:
                print("Keine Module mit dem Status 'Done' gefunden.")
                return None

    def update_gpa(self):
        average_gpa = self.calculate_done_modules_gpa()
        if average_gpa is not None:
            Database.execute('''
                       UPDATE StudyProgram SET current_gpa = ? WHERE id = ?
                   ''', (average_gpa, self.program_id))

    def update_total_ects(self, new_total_ects):
        self.total_ects = new_total_ects
        Database.execute('''
               UPDATE StudyProgram SET total_ects = ? WHERE id = ?
           ''', (self.total_ects, self.program_id))
        print(f"Total ECTS wurde auf {self.total_ects} aktualisiert.")

    def update_collected_ects(self):
        result = Database.fetch_one('''
               SELECT SUM(ects) FROM Module
               WHERE status = 'Done';
           ''')
        self.collected_ects = result[0] or 0
        Database.execute('''
               UPDATE StudyProgram SET collected_ects = ? WHERE id = ?
           ''', (self.collected_ects, self.program_id))
        print(f"Du hast aktuell {self.collected_ects} ECTS.")

    def display_in_progress_modules(self):
        rows = Database.fetch_all('SELECT module_name FROM Module WHERE status = "In Progress";')
        if rows:
            print("Module, welche aktuell in Bearbeitung sind:")
            for row in rows:
                print(f"- {row[0]}")
        else:
            print("Aktuell sind keine Module in Bearbeitung, es ist also Zeit für ein neues Modul!")

    def calculate_monthly_module_load(self):
        conn = sqlite3.connect('StudyDashboard.sql')
        cursor = conn.cursor()

        # Das Enddatum des Studiums abfragen
        cursor.execute('SELECT end_date FROM StudyTime WHERE id = ?', (self.study_time_id,))
        end_date_row = cursor.fetchone()
        conn.close()

        if end_date_row:
            end_date = datetime.strptime(end_date_row[0], '%Y-%m-%d')  # Annahme des Formats
            # Berechnung der verbleibenden Monate:
            remaining_months = (end_date.year - datetime.now().year) * 12 + (end_date.month - datetime.now().month)

            # Anzahl der Module mit Status 'In Progress' und 'Pending' zählen
            conn = sqlite3.connect('StudyDashboard.sql')
            cursor = conn.cursor()
            cursor.execute('''
                        SELECT COUNT(*) FROM Module WHERE status IN ('In Progress', 'Pending')
                    ''')
            total_modules_in_progress = cursor.fetchone()[0]
            conn.close()

            # Berechnung des durchschnittlichen Modulaufwands pro Monat
            if remaining_months > 0:
                self.monthly_module_load = total_modules_in_progress / remaining_months
                print(f"Du musst noch durchschnittlich {self.monthly_module_load:.2f} Module pro Monat abschließen.")
                self.update_monthly_module_load_in_db()
            else:
                print("Du hast leider keinen vollen Monat mehr Zeit.")
        else:
            print("Kein Enddatum für das Studium gefunden.")

    def update_monthly_module_load_in_db(self):
        conn = sqlite3.connect('StudyDashboard.sql')
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE StudyProgram SET monthly_module_load = ? WHERE id = ?
        ''', (self.monthly_module_load, self.program_id))
        conn.commit()
        conn.close()

    def display_progress(self):
        if self.total_ects == 0:
            print("Gesamt-ECTS ist 0, Fortschritt kann nicht berechnet werden.")
            return
        progress_percentage = (self.collected_ects / self.total_ects) * 100
        print(f"Dein Studienfortschritt auf Grundlage der ECTS beträgt {progress_percentage:.2f}%.")