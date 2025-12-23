# -*- coding: utf-8 -*-
"""
Fenêtre principale de l'application
Contient la sidebar, le header, le footer et la zone de contenu
"""

import customtkinter as ctk
from typing import List
from models.student import Student
from models.subject import Subject
from models.grade import Grade
from gui.components.sidebar import Sidebar
from gui.components.header import Header
from gui.components.footer import Footer
import json
import os

# #region agent log
DEBUG_LOG_PATH = r"d:\Ecole\UCAC ICAM\PROJETS IMPORTANTS\student_grade_manager\.cursor\debug.log"
def _debug_log(location, message, data, hypothesis_id=None):
    try:
        with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as f:
            log_entry = {
                "sessionId": "debug-session",
                "runId": "run1",
                "hypothesisId": hypothesis_id,
                "location": location,
                "message": message,
                "data": data,
                "timestamp": os.path.getmtime(DEBUG_LOG_PATH) * 1000 if os.path.exists(DEBUG_LOG_PATH) else 0
            }
            f.write(json.dumps(log_entry) + "\n")
    except: pass
# #endregion


class MainWindow(ctk.CTk):
    """
    Fenêtre principale avec layout complet
    """
    
    def __init__(self, app):
        """
        Initialise la fenêtre principale
        
        Args:
            app: Instance de l'application principale
        """
        super().__init__()
        
        self.app = app
        self.file_manager = app.file_manager
        
        # Données chargées
        self.students: List[Student] = []
        self.subjects: List[Subject] = []
        self.grades: List[Grade] = []
        
        # Frames disponibles
        self.frames = {}
        self.current_frame = None
        
        # Configuration de la fenêtre
        self.title("GradeMaster - Academic Management System")
        self.geometry("1400x900")
        self._center_window()
        
        # Charger les données
        self._load_data()
        
        # Créer l'interface
        self._create_widgets()
        
        # Sélectionner visuellement le dashboard dans la sidebar (sans déclencher le callback)
        if "dashboard" in self.sidebar.item_buttons:
            self.sidebar.item_buttons["dashboard"].configure(fg_color=("#1F6AA5", "#1F6AA5"))
        self.sidebar.selected_item = "dashboard"
        
        # Afficher le dashboard par défaut (après que tous les widgets soient créés)
        self._show_frame("dashboard")
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _load_data(self):
        """Charge toutes les données depuis les fichiers JSON"""
        # Charger les étudiants
        students_data = self.file_manager.load_students()
        self.students = [Student.from_dict(s) for s in students_data]
        
        # Charger les matières
        subjects_data = self.file_manager.load_subjects()
        self.subjects = [Subject.from_dict(s) for s in subjects_data]
        
        # Charger les notes
        grades_data = self.file_manager.load_grades()
        self.grades = [Grade.from_dict(g) for g in grades_data]
    
    def _save_data(self):
        """Sauvegarde toutes les données dans les fichiers JSON"""
        # #region agent log
        _debug_log("main_window.py:_save_data:entry", "_save_data() called", {"students_count": len(self.students)}, "C")
        # #endregion
        
        # Sauvegarder les étudiants
        students_data = [s.to_dict() for s in self.students]
        
        # #region agent log
        _debug_log("main_window.py:_save_data:before_save", "Before save_students()", {"students_data_count": len(students_data), "first_student": students_data[0] if students_data else None}, "C")
        # #endregion
        
        result = self.file_manager.save_students(students_data)
        
        # #region agent log
        _debug_log("main_window.py:_save_data:after_save", "After save_students()", {"save_result": result}, "C")
        # #endregion
        
        # Sauvegarder les matières
        subjects_data = [s.to_dict() for s in self.subjects]
        self.file_manager.save_subjects(subjects_data)
        
        # Sauvegarder les notes
        grades_data = [g.to_dict() for g in self.grades]
        self.file_manager.save_grades(grades_data)
        
        # #region agent log
        _debug_log("main_window.py:_save_data:exit", "_save_data() completed", {}, "C")
        # #endregion
    
    def _create_widgets(self):
        """Crée les widgets de la fenêtre principale"""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Sidebar à gauche
        self.sidebar = Sidebar(
            main_container,
            main_window=self,
            on_item_selected=self._on_sidebar_item_selected
        )
        self.sidebar.pack(side="left", fill="y")
        
        # Container pour le contenu principal
        content_container = ctk.CTkFrame(main_container, fg_color="transparent")
        content_container.pack(side="right", fill="both", expand=True)
        
        # Header en haut
        self.header = Header(
            content_container,
            main_window=self,
            on_import_data=self._on_import_data,
            on_new_entry=self._on_new_entry
        )
        self.header.pack(fill="x")
        
        # Zone de contenu (frames)
        self.content_frame = ctk.CTkFrame(content_container, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Footer en bas
        self.footer = Footer(content_container)
        self.footer.pack(fill="x", side="bottom")
    
    def _on_sidebar_item_selected(self, item_id: str):
        """Gère la sélection d'un item dans la sidebar"""
        self._show_frame(item_id)
    
    def _show_frame(self, frame_name: str):
        """Affiche une frame spécifique"""
        # Cacher la frame actuelle
        if self.current_frame:
            self.current_frame.pack_forget()
        
        # Créer la frame si elle n'existe pas
        if frame_name not in self.frames:
            self._create_frame(frame_name)
        
        # Afficher la nouvelle frame
        if frame_name in self.frames:
            self.current_frame = self.frames[frame_name]
            self.current_frame.pack(fill="both", expand=True)
    
    def _create_frame(self, frame_name: str):
        """Crée une frame selon son nom"""
        if frame_name == "dashboard":
            from gui.frames.dashboard_frame import DashboardFrame
            self.frames[frame_name] = DashboardFrame(self.content_frame, self)
        elif frame_name == "students":
            from gui.frames.students_frame import StudentsFrame
            self.frames[frame_name] = StudentsFrame(self.content_frame, self)
        elif frame_name == "subjects":
            from gui.frames.subjects_frame import SubjectsFrame
            self.frames[frame_name] = SubjectsFrame(self.content_frame, self)
        elif frame_name == "grades":
            from gui.frames.grades_frame import GradesFrame
            self.frames[frame_name] = GradesFrame(self.content_frame, self)
        elif frame_name == "consultation":
            from gui.frames.consultation_frame import ConsultationFrame
            self.frames[frame_name] = ConsultationFrame(self.content_frame, self)
        elif frame_name == "statistics":
            from gui.frames.statistics_frame import StatisticsFrame
            self.frames[frame_name] = StatisticsFrame(self.content_frame, self)
    
    def _on_import_data(self):
        """Gère l'action Import Data"""
        # Recharger les données
        self._load_data()
        # Rafraîchir la frame actuelle
        if self.current_frame and hasattr(self.current_frame, 'refresh'):
            self.current_frame.refresh()
    
    def _on_new_entry(self):
        """Gère l'action New Entry"""
        # Basculer vers la frame appropriée selon le contexte
        if self.current_frame:
            if hasattr(self.current_frame, 'show_add_dialog'):
                self.current_frame.show_add_dialog()
    
    def refresh_data(self):
        """Rafraîchit les données et sauvegarde"""
        self._save_data()
        self._load_data()
        # Rafraîchir toutes les frames
        for frame in self.frames.values():
            if hasattr(frame, 'refresh'):
                frame.refresh()
    
    def _update_all_texts(self):
        """Met à jour tous les textes de l'interface lors du changement de langue"""
        # Mettre à jour le header
        if hasattr(self, 'header') and hasattr(self.header, '_update_texts'):
            self.header._update_texts()
        
        # Mettre à jour la sidebar
        if hasattr(self, 'sidebar') and hasattr(self.sidebar, '_update_texts'):
            self.sidebar._update_texts()
        
        # Mettre à jour toutes les frames
        for frame in self.frames.values():
            if hasattr(frame, '_update_texts'):
                frame._update_texts()

