from database import Database
from database_entity import DatabaseEntity
from module import Module
from study_time import StudyTime


class StudyProgram(DatabaseEntity):
    def __init__(self, program_id=None, program_name=None, current_gpa=0.0, total_ects=0, collected_ects=0,
                 monthly_module_load=0, study_time_id=None, gpa_goal=2.0):
        self.program_id = program_id
        self.program_name = program_name
        self.current_gpa = current_gpa
        self.total_ects = total_ects
        self.collected_ects = collected_ects
        self.monthly_module_load = monthly_module_load
        self.study_time_id = study_time_id
        self.gpa_goal = gpa_goal

    def save_to_db(self):
        Database.execute('''UPDATE StudyProgram SET program_name = ?, current_gpa = ?, total_ects = ?, collected_ects = ?, 
                                    monthly_module_load = ?, study_time_id = ? WHERE id = ?;''',
                         (self.program_name, self.current_gpa, self.total_ects, self.collected_ects,
                          self.monthly_module_load, self.study_time_id, self.program_id))
        print(f"Study Program mit ID {self.program_id} wurde erfolgreich gespeichert.")

    def get_study_time(self):
        study_time = StudyTime.from_db(self.study_time_id)
        if study_time:
            return study_time.start_date, study_time.end_date, study_time.standard_duration_months
        else:
            return None, None, None

    def get_module_progress(self):
        total_modules = len(Module.fetch_all())  # Alle Module abfragen
        completed_modules = len([m for m in Module.fetch_all() if m.status == "Done"])

        if total_modules == 0:
            return 0  # Verhindert Division durch null, falls keine Module vorhanden sind.

        return (completed_modules / total_modules) * 100

    def get_required_ects(self):
        return self.total_ects