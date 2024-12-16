import tkinter as tk
from tkinter import ttk, messagebox
from study_dashboard_gui_service import StudyDashboardGUIService


class StudyDashboardGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Dashboard")
        self.service = StudyDashboardGUIService()

        # Fenstergröße
        window_width = 1280
        window_height = int(window_width * 9 / 16)
        self.root.geometry(f"{window_width}x{window_height}")

        # Scrollbare Oberfläche
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))

        self.show_dashboard()

    def show_dashboard(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        # Dashboard-Daten laden
        modules = self.service.get_all_modules()
        study_program = self.service.get_study_program(1)

        tk.Label(self.scrollable_frame, text="Dashboard", font=("Arial", 16)).pack(pady=10)

        # Studienzeit anzeigen
        study_time = self.service.get_study_time(study_program.study_time_id)
        if study_time and study_time.start_date and study_time.end_date:
            tk.Label(self.scrollable_frame,
                     text=f"Studienbeginn: {study_time.start_date} - Studienende: {study_time.end_date}").pack(pady=5)

        # Haupt-Frame für die Tabelle und das rechte Info-Panel
        main_frame = tk.Frame(self.scrollable_frame)
        main_frame.pack(fill=tk.X, pady=10)

        # Tabelle der Module
        table_frame = tk.Frame(main_frame)
        table_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        self.create_module_table(modules, table_frame)

        # Rechts neben der Tabelle: Vertikale Infos
        info_frame = tk.Frame(main_frame)
        info_frame.pack(side=tk.LEFT, padx=20, fill=tk.Y)

        if study_program:
            # Module nach Status
            open_modules = self.service.count_modules_by_status("Pending")
            in_progress_modules = self.service.count_modules_by_status("In Progress")
            completed_modules = self.service.count_modules_by_status("Done")

            tk.Label(info_frame, text=f"Offene Module: {open_modules}", font=("Arial", 12)).pack(pady=5)
            tk.Label(info_frame, text=f"Module in Bearbeitung: {in_progress_modules}", font=("Arial", 12)).pack(pady=5)
            tk.Label(info_frame, text=f"Abgeschlossene Module: {completed_modules}", font=("Arial", 12)).pack(pady=5)

            # Restmodule pro Monat
            monthly_module_load = self.service.calculate_monthly_module_load(study_program)
            tk.Label(info_frame, text=f"Restmodule pro Monat: {monthly_module_load:.2f}", font=("Arial", 12)).pack(pady=5)

            # Fortschritt
            progress = self.service.calculate_progress(study_program)
            tk.Label(info_frame, text=f"Fortschritt: {progress:.2f}%", font=("Arial", 12)).pack(pady=5)

        # Unterhalb der Tabelle: Horizontale Infos
        stats_frame = tk.Frame(self.scrollable_frame)
        stats_frame.pack(fill=tk.X, pady=20)

        if study_program:
            ects_info = self.service.get_ects_info(study_program)

            # Gesammelte ECTS
            tk.Label(stats_frame, text=f"Gesammelte ECTS: {ects_info['collected_ects']}", font=("Arial", 12)).pack(
                side=tk.LEFT, padx=10
            )

            # Nötige ECTS
            tk.Label(stats_frame, text=f"Nötige ECTS: {ects_info['required_ects']}", font=("Arial", 12)).pack(
                side=tk.LEFT, padx=10
            )

            # Durchschnitt
            tk.Label(stats_frame, text=f"Aktueller Durchschnitt: {study_program.current_gpa:.2f}", font=("Arial", 12)).pack(
                side=tk.LEFT, padx=10
            )

            # Gewünschter Durchschnitt
            tk.Label(stats_frame, text=f"Gewünschter Durchschnitt: {study_program.gpa_goal:.2f}", font=("Arial", 12)).pack(
                side=tk.LEFT, padx=10
            )

        # Buttons
        tk.Button(self.scrollable_frame, text="Daten bearbeiten", command=self.show_edit_data_form).pack(pady=5)
        tk.Button(self.scrollable_frame, text="Beenden", command=self.root.quit).pack(pady=5)

    def create_module_table(self, modules, parent_frame):
        """Erstellt die Tabelle für Module."""
        module_table = ttk.Treeview(parent_frame, columns=("Module", "ECTS", "Note", "Status"), show="headings")
        module_table.heading("Module", text="Modulname")
        module_table.heading("ECTS", text="ECTS")
        module_table.heading("Note", text="Note")
        module_table.heading("Status", text="Status")

        module_table.tag_configure("done", background="lightgreen")
        module_table.tag_configure("in_progress", background="orange")
        module_table.tag_configure("pending", background="lightgray")

        for module in modules:
            status_tag = module.status.lower().replace(" ", "_")
            module_table.insert("", tk.END, values=(module.module_name, module.ects, module.grade, module.status),
                                tags=(status_tag,))

        self.auto_resize_columns(module_table)
        module_table.pack(fill=tk.BOTH, expand=True)

    def auto_resize_columns(self, treeview):
        for col in treeview["columns"]:
            max_width = max(
                len(treeview.heading(col)["text"]),
                max(len(str(treeview.item(item, "values")[treeview["columns"].index(col)])) for item in treeview.get_children())
            )
            treeview.column(col, width=max_width * 10)

    def show_edit_data_form(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        tk.Label(self.scrollable_frame, text="Daten bearbeiten", font=("Arial", 16)).pack(pady=10)

        modules = self.service.get_all_modules()

        for module in modules:
            frame = tk.Frame(self.scrollable_frame)
            frame.pack(pady=5, fill=tk.X)

            tk.Label(frame, text=f"Modul: {module.module_name}").pack(side=tk.LEFT, padx=10)

            grade_entry = tk.Entry(frame)
            grade_entry.insert(0, module.grade)
            grade_entry.pack(side=tk.LEFT, padx=5)

            status_var = tk.StringVar()
            status_var.set(module.status)
            tk.OptionMenu(frame, status_var, "In Progress", "Done", "Pending").pack(side=tk.LEFT, padx=5)

            tk.Button(frame, text="Speichern",
                      command=lambda m=module, ge=grade_entry, sv=status_var: self.save_module_changes(m, ge, sv)).pack(
                side=tk.LEFT, padx=5)

        tk.Button(self.scrollable_frame, text="Zurück zum Dashboard", command=self.show_dashboard).pack(pady=10)

    def save_module_changes(self, module, grade_entry, status_var):
        new_grade = grade_entry.get()
        new_status = status_var.get()

        try:
            self.service.update_module(module.module_id, new_grade, new_status)
            messagebox.showinfo("Erfolg", f"Änderungen für {module.module_name} wurden gespeichert.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern der Änderungen: {e}")
