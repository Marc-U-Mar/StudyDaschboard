import tkinter as tk
from tkinter import messagebox
from module import Module
from study_program import StudyProgram
from study_time import StudyTime


class StudyDashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Dashboard")

        # Start-Screen
        self.start_screen()

    def start_screen(self):
        """Zeigt den Startbildschirm mit der Option, die Daten zu aktualisieren und das Dashboard zu öffnen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Willkommen im Study Dashboard!", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Daten aktualisieren", command=self.update_data).pack(pady=5)
        tk.Button(self.root, text="Zum Dashboard", command=self.show_dashboard).pack(pady=5)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=5)

    def update_data(self):
        """Aktualisiert Module und Studienzeiten."""
        try:
            # Module aktualisieren
            modules = Module.fetch_all()
            for module in modules:
                module.set_grade_and_status()

            # Studienzeit aktualisieren
            study_times = StudyTime.fetch_all()
            if study_times:
                study_times[0].update_study_time()

            messagebox.showinfo("Erfolg", "Daten erfolgreich aktualisiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Beim Aktualisieren der Daten ist ein Fehler aufgetreten: {e}")

    def show_dashboard(self):
        """Zeigt das Haupt-Dashboard mit den aktuellen Daten an."""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Dashboard-Daten laden
        modules = Module.fetch_all()
        study_program = StudyProgram.from_db(1)

        tk.Label(self.root, text="Dashboard", font=("Arial", 16)).pack(pady=10)

        # Module anzeigen
        if modules:
            tk.Label(self.root, text="Module:", font=("Arial", 12)).pack(pady=5)
            for module in modules:
                tk.Label(self.root, text=f"{module.module_name} - {module.status} - Note: {module.grade}").pack()

        # Studienprogramm anzeigen
        if study_program:
            tk.Label(self.root, text=f"Studienprogramm: {study_program.program_name}", font=("Arial", 12)).pack(pady=5)
            tk.Label(self.root, text=f"GPA: {study_program.current_gpa:.2f}").pack()
            tk.Label(self.root, text=f"ECTS gesammelt: {study_program.collected_ects}/{study_program.total_ects}").pack()
            tk.Label(self.root, text=f"Monatlicher Modulaufwand: {study_program.monthly_module_load:.2f}").pack()

        tk.Button(self.root, text="Zurück zum Startbildschirm", command=self.start_screen).pack(pady=5)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudyDashboardGUI(root)
    root.mainloop()