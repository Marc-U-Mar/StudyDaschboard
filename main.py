from module import Module
from study_time import StudyTime
from study_program import StudyProgram
from database import Database


def update_modules():
    modules = Module.fetch_all()

    for status in ['Done', 'In Progress', 'Pending']:
        edit_status = input(f"Do you want to edit modules with status '{status}'? (yes/no): ").strip().lower()
        if edit_status == 'yes':
            for module in modules:
                if module.status == status:
                    module.set_grade_and_status()


def update_study_time():
    # Lade die aktuelle StudyTime aus der Datenbank
    conn = Database.get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM StudyTime;')
    row = cursor.fetchone()
    conn.close()

    if row:
        study_time = StudyTime(*row)
        study_time.update_study_time()  # Ändere den Funktionsaufruf
    else:
        print("No study time data found in the database.")


if __name__ == "__main__":
    # Alle Entitäten abrufen
    modules = Module.fetch_all()
    study_programs = StudyProgram.fetch_all()
    study_times = StudyTime.fetch_all()

    # Alle Entitäten in einer Liste kombinieren
    all_entities = modules + study_programs + study_times

    # Aktualisiere die Module
    update_modules()

    # Aktualisiere die Studienzeit
    update_study_time()

    # Am Ende zeige die Datenbankinhalte an
    print("\nDisplaying current data in the database:")
    modules = Module.fetch_all()
    for module in modules:
        module.display()

    study_program = StudyProgram.from_db(1)
    if study_program:
        study_program.update_gpa()
        study_program.display_in_progress_modules()
        # Aktualisiere die gesammelten ECTS
        study_program.update_collected_ects()
        study_program.display_progress()

        total_ects_input = input("Hat sich an deiner Gesamt-ECTS etwas geändert, dann gib hier den neuen Wert ein? (drücke Enter, um aktuellen Wert beizubehalten): ")

        if total_ects_input.strip():  # Überprüfen, ob die Eingabe nicht leer ist
            new_total_ects = float(total_ects_input)
            study_program.update_total_ects(new_total_ects)
        else:
            print(f"Du musst insgesamt {study_program.total_ects} ECTS erreichen.")

        study_program.calculate_monthly_module_load()

        # Alle Entitäten in der Datenbank speichern
        Database.save_all_entities(all_entities)