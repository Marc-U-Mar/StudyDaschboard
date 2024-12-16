import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import Database
from module import Module
from study_program import StudyProgram
from study_time import StudyTime

class StudyDashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Dashboard")
        self.show_dashboard()

    def show_dashboard(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Dashboard-Daten laden
        modules = Module.fetch_all()
        study_program = StudyProgram.from_db(1)

        tk.Label(self.root, text="Dashboard", font=("Arial", 16)).pack(pady=10)


        # Studienzeit anzeigen
        if study_program:
            start_date, end_date, standard_duration_months = study_program.get_study_time()
            if start_date and end_date:
                tk.Label(self.root, text=f"Studienbeginn: {start_date} - Studienende: {end_date}").pack(pady=5)

                # Direktes Abrufen der StudyTime-Instanz
                study_time = StudyTime.from_db(study_program.study_time_id)
                if study_time:
                    remaining_months = study_time.calculate_remaining_months()  # Methode aus StudyTime-Klasse verwenden
                    tk.Label(self.root, text=f"Restzeit in Monaten: {remaining_months} Monate").pack(pady=5)

        # Oben: Studienbeginn, -ende und verbleibende Monate
        if study_program:
            start_date, end_date, _ = study_program.get_study_time()

            # Restzeit in Monaten berechnen und anzeigen
            study_time = StudyTime.from_db(study_program.study_time_id)
            if study_time:
                remaining_months = study_time.calculate_remaining_months()  # Berechnung über StudyTime

            header_frame = tk.Frame(self.root)
            header_frame.pack(fill=tk.X, pady=10)

            tk.Label(header_frame, text=f"Studienbeginn: {start_date} Studienende: {end_date} "
                                       f"Restzeit in Monaten: {remaining_months}", font=("Arial", 12)).pack(side=tk.LEFT)

        # Container für die Modultabelle und die Box nebeneinander
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.X, pady=10)

        # Zwei Drittel der Seite für die Modultabelle
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        module_table = ttk.Treeview(table_frame, columns=("Module", "ECTS", "Note", "Status"), show="headings")

        module_table.heading("Module", text="Modulname")
        module_table.heading("ECTS", text="ECTS")
        module_table.heading("Note", text="Note")
        module_table.heading("Status", text="Status")

        # Farbliche Markierungen für verschiedene Status
        module_table.tag_configure("done", background="lightgreen")  # Done = Grün
        module_table.tag_configure("in_progress", background="orange")  # In Progress = Orange
        module_table.tag_configure("pending", background="lightgray")  # Pending = Grau

        # Einfügen der Module in die Tabelle
        for module in modules:
            # Überprüfe den Status des Moduls und weise den entsprechenden Tag zu
            if module.status == "Done":
                status_tag = "done"
            elif module.status == "In Progress":
                status_tag = "in_progress"
            elif module.status == "Pending":
                status_tag = "pending"
            else:
                status_tag = ""  # Kein spezieller Status

            # Füge die Zeile in die Tabelle ein und weise den Tag zu
            module_table.insert("", tk.END, values=(module.module_name, module.ects, module.grade, module.status),
                                tags=(status_tag,))
        self.auto_resize_columns(module_table)

        module_table.pack(fill=tk.X)

        # Box rechts neben der Modultabelle
        info_frame = tk.Frame(main_frame)
        info_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)

        open_modules = len([m for m in modules if m.status == "Pending"])
        in_progress_modules = len([m for m in modules if m.status == "In Progress"])
        completed_modules = len([m for m in modules if m.status == "Done"])

        tk.Label(info_frame, text=f"Offene Module: {open_modules}", font=("Arial", 12)).pack(pady=5)
        tk.Label(info_frame, text=f"Module in Bearbeitung: {in_progress_modules}", font=("Arial", 12)).pack(pady=5)
        tk.Label(info_frame, text=f"Abgeschlossene Module: {completed_modules}", font=("Arial", 12)).pack(pady=5)

        monthly_module_load = study_program.monthly_module_load
        tk.Label(info_frame, text=f"Monatlicher Modulaufwand: {monthly_module_load:.2f} Module",font=("Arial", 12)).pack(pady=5)
        tk.Label(info_frame, text=f"Fortschritt: {study_program.get_module_progress():.2f}%", font=("Arial", 12)).pack(pady=5)

        # Durchschnitt, gewünschter Durchschnitt und ECTS-Anforderungen in einem separaten Container
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(fill=tk.X, pady=20)

        # Container für die Statistiken (links und rechts nebeneinander)
        stats_left_frame = tk.Frame(stats_frame)
        stats_left_frame.pack(side=tk.LEFT, padx=10)

        stats_right_frame = tk.Frame(stats_frame)
        stats_right_frame.pack(side=tk.LEFT, padx=10)

        # Linke Spalte (Durchschnitt und gewünschter Durchschnitt)
        tk.Label(stats_left_frame, text=f"Durchschnitt: {study_program.current_gpa:.2f}").pack(anchor="w")
        tk.Label(stats_left_frame, text=f"Gewünschter Durchschnitt: {study_program.current_gpa + 1.0:.2f}").pack(
            anchor="w")

        # Rechte Spalte (ECTS gesammelt und benötigte ECTS)
        required_ects = study_program.get_required_ects()
        tk.Label(stats_right_frame,
                 text=f"ECTS gesammelt: {study_program.collected_ects}/{study_program.total_ects}").pack(anchor="w")
        tk.Label(stats_right_frame, text=f"Benötigte ECTS: {required_ects}").pack(anchor="w")

        tk.Button(self.root, text="Menü", command=self.start_screen).pack(pady=5)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=5)

    def start_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Willkommen im Study Dashboard!", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.root, text="Daten aktualisieren", command=self.show_edit_data_form).pack(pady=5)
        tk.Button(self.root, text="Zum Dashboard", command=self.show_dashboard).pack(pady=5)
        tk.Button(self.root, text="Beenden", command=self.root.quit).pack(pady=5)

    def show_edit_data_form(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Module bearbeiten", font=("Arial", 16)).pack(pady=10)

        # Modul-Daten zur Bearbeitung laden
        modules = Module.fetch_all()

        # Formular zur Bearbeitung der Module
        for module in modules:
            # Formular für jedes Modul erstellen
            frame = tk.Frame(self.root)
            frame.pack(pady=5, fill=tk.X)

            tk.Label(frame, text=f"Modul: {module.module_name}").pack(side=tk.LEFT, padx=10)

            # Eingabefeld für Noten
            grade_label = tk.Label(frame, text="Note:")
            grade_label.pack(side=tk.LEFT)
            grade_entry = tk.Entry(frame)
            grade_entry.insert(0, module.grade)  # Vorbelegung mit der aktuellen Note
            grade_entry.pack(side=tk.LEFT, padx=5)

            # Eingabefeld für Status
            status_label = tk.Label(frame, text="Status:")
            status_label.pack(side=tk.LEFT)
            status_entry = tk.Entry(frame)
            status_entry.insert(0, module.status)  # Vorbelegung mit dem aktuellen Status
            status_entry.pack(side=tk.LEFT, padx=5)

        # Ein Button zum Speichern aller Änderungen
        save_button = tk.Button(self.root, text="Speichern", command=lambda: self.save_changes(module, grade_entry, status_entry))
        save_button.pack(pady=20)

        # Button, um zur Startseite zurückzukehren
        tk.Button(self.root, text="Zurück zum Dashboard", command=self.show_dashboard).pack(pady=10)

    def save_changes(self, module, grade_entry, status_entry):
        """Speichert die Änderungen für ein einzelnes Modul."""
        # Neue Werte aus den Eingabefeldern holen
        new_grade = grade_entry.get()
        new_status = status_entry.get()

        # Datenbank-Update durchführen
        query = """UPDATE Module
                   SET grade = ?, status = ?
                   WHERE id = ?"""
        params = (new_grade, new_status, module.module_id)

        try:
            # Wenn execute keine Ausnahme wirft, wurde das Update erfolgreich ausgeführt
            Database.execute(query, params)
            print(f"Modul {module.module_name} erfolgreich gespeichert.")
            messagebox.showinfo("Erfolg", f"Modul {module.module_name} wurde erfolgreich gespeichert.")
        except Exception as e:
            # Fehlerbehandlung, wenn beim Update ein Fehler auftritt
            print(f"Fehler beim Speichern von Modul {module.module_name}: {str(e)}")
            messagebox.showerror("Fehler",
                                 f"Beim Speichern von {module.module_name} ist ein Fehler aufgetreten: {str(e)}")

    def update_data(self):
        try:
            # Hier könnten allgemeine Datenaktualisierungen durchgeführt werden
            messagebox.showinfo("Erfolg", "Daten erfolgreich aktualisiert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Beim Aktualisieren der Daten ist ein Fehler aufgetreten: {e}")

    # Passt die Spaltenbreite basierend auf dem Inhalt und Überschrift an
    def auto_resize_columns(self, treeview):
        for col in treeview["columns"]:
            max_width = 0
            # Berücksichtige die Breite der Überschrift
            header_text = treeview.heading(col)["text"]
            max_width = max(max_width, len(header_text))

            # Finde das längste Element in der Spalte (Daten in den Zeilen)
            for item in treeview.get_children():
                text = treeview.item(item, "values")[treeview["columns"].index(col)]
                max_width = max(max_width, len(str(text)))

            # Setze die Spaltenbreite, multipliziere mit 10 für eine bessere Sichtbarkeit
            treeview.column(col, width=max_width * 10)