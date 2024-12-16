import sqlite3
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

    def display(self):
        print(f"Module ID: {self.module_id}, Name: {self.module_name}, Grade: {self.grade}, "
              f"Status: {self.status}, ECTS: {self.ects}, Study Program ID: {self.study_program_id}")

    def input_float(self, prompt):
        while True:
            user_input = input(prompt).strip()
            user_input = user_input.replace(',', '.')  # Ersetze Komma durch Punkt
            try:
                return float(user_input)
            except ValueError:
                print("Ungültig! Bitte gib eine gültige Zahl ein.")

    def set_grade_and_status(self):
        print("Current values:")
        self.display()

        # Eingabe der Note
        new_grade = input("Gib eine neue Note ein (oder drücke Enter um zu überspringen): ")
        if new_grade:
            self.grade = self.input_float("Gib die Note ein (float value): ")
            # Setze den Status automatisch auf "Done", wenn die Note nicht NULL ist
            self.status = "Done"

        # Überprüfung, ob der Benutzer den Status ändern möchte
        new_status = self.get_valid_status()
        if new_status:
            self.status = new_status  # Status nur ändern, wenn ein neuer Status eingegeben wurde

        # Aktualisierung der Datenbank
        self.save_to_db()

    def get_valid_status(self):
        valid_statuses = ["In Progress", "Done", "Pending"]
        while True:
            new_status = input(
                f"Current status is '{self.status}'. Gib einen neuen Status ein (In Progress, Done, Pending; oder drücke Enter um zu überspringen): ")
            if new_status in valid_statuses or new_status == "":
                return new_status if new_status else None  # Wenn leer, behalte den aktuellen Status
            print(f"Ungültig, bitte verwende: {', '.join(valid_statuses)}")

    def save_to_db(self):
        try:
            # Debugging: Zeige die Daten, die gespeichert werden sollen
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