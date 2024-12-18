from module import Module
from study_program import StudyProgram
from study_time import StudyTime
from database import Database
from datetime import datetime

class StudyDashboardGUIService:
    def __init__(self):
        pass

    # --- Module ---
    def get_all_modules(self):
        return Module.fetch_all()

    def update_module(self, module_id, grade, status):
        query = '''UPDATE Module SET grade = ?, status = ? WHERE id = ?'''
        Database.execute(query, (grade, status, module_id))

    def count_modules_by_status(self, status):
        result = Database.fetch_one('SELECT COUNT(*) FROM Module WHERE status = ?', (status,))
        return result[0] if result else 0

    # --- Studienprogramm ---
    def get_study_program(self, program_id=1):
        return StudyProgram.from_db(program_id)

    def calculate_progress(self, study_program):
        if study_program.total_ects == 0:
            return 0
        return (study_program.collected_ects / study_program.total_ects) * 100

    def update_study_program_gpa(self, study_program):
        study_program.update_gpa()

    # --- Studienzeit ---
    def get_study_time(self, study_time_id):
         return StudyTime.from_db(study_time_id)

    def calculate_monthly_module_load(self, study_program):
        end_date = Database.fetch_one('SELECT end_date FROM StudyTime WHERE id = ?', (study_program.study_time_id,))
        if end_date:
            end_date = datetime.strptime(end_date[0], '%Y-%m-%d')
            remaining_months = (end_date.year - datetime.now().year) * 12 + (end_date.month - datetime.now().month)

            if remaining_months > 0:
                total_modules = self.count_modules_by_status("In Progress") + self.count_modules_by_status("Pending")
                return total_modules / remaining_months
        return 0

    def update_study_time(self, study_time_id, start_date, end_date):
        study_time = StudyTime.from_db(study_time_id)
        if study_time:
            study_time.start_date = start_date
            study_time.end_date = end_date
            study_time.save_to_db()

    def calculate_remaining_months(self, study_time_id):
        study_time = StudyTime.from_db(study_time_id)
        if study_time:
            return study_time.calculate_remaining_months()
        return 0

    # --- ECTS ---
    def update_collected_ects(self, study_program):
        result = Database.fetch_one('SELECT SUM(ects) FROM Module WHERE status = "Done";')
        study_program.collected_ects = result[0] or 0
        query = '''UPDATE StudyProgram SET collected_ects = ? WHERE id = ?'''
        Database.execute(query, (study_program.collected_ects, study_program.program_id))

    def get_ects_info(self, study_program):
        required_ects = study_program.total_ects - study_program.collected_ects
        return {
            "collected_ects": study_program.collected_ects,
            "required_ects": required_ects
        }