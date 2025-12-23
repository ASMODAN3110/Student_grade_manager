# -*- coding: utf-8 -*-
"""
Frame Consultation - Consultation des notes
"""

import customtkinter as ctk
from tkinter import messagebox
from services.statistics import Statistics


class ConsultationFrame(ctk.CTkScrollableFrame):
    """
    Frame pour la consultation des notes
    """
    
    def __init__(self, parent, main_window):
        """
        Initialise la frame de consultation
        
        Args:
            parent: Widget parent
            main_window: Fenêtre principale
        """
        super().__init__(parent, fg_color="transparent")
        
        self.main_window = main_window
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée les widgets de la frame"""
        # Titre
        title_label = ctk.CTkLabel(
            self,
            text="Consultation des Notes",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 30))
        
        # Onglets
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        # Onglet 1: Notes d'un étudiant
        self.tab1 = self.tabview.add("Notes d'un étudiant")
        self._create_student_grades_tab()
        
        # Onglet 2: Notes d'une classe
        self.tab2 = self.tabview.add("Notes d'une classe")
        self._create_class_grades_tab()
        
        # Onglet 3: Bulletin complet
        self.tab3 = self.tabview.add("Bulletin complet")
        self._create_bulletin_tab()
    
    def _create_student_grades_tab(self):
        """Crée l'onglet pour les notes d'un étudiant"""
        # Sélection étudiant
        select_frame = ctk.CTkFrame(self.tab1, fg_color="transparent")
        select_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(select_frame, text="Matricule:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.student_matricule_entry = ctk.CTkEntry(select_frame, width=200, height=40)
        self.student_matricule_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            select_frame,
            text="Afficher",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            command=self._show_student_grades
        ).pack(side="left")
        
        # Zone d'affichage
        self.student_grades_text = ctk.CTkTextbox(self.tab1, height=400)
        self.student_grades_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _create_class_grades_tab(self):
        """Crée l'onglet pour les notes d'une classe"""
        # Sélection
        select_frame = ctk.CTkFrame(self.tab2, fg_color="transparent")
        select_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(select_frame, text="Niveau:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.class_niveau_entry = ctk.CTkEntry(select_frame, width=150, height=40)
        self.class_niveau_entry.pack(side="left", padx=(0, 20))
        
        ctk.CTkLabel(select_frame, text="Matière:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.class_subject_combo = ctk.CTkComboBox(
            select_frame,
            values=[f"{s.code} - {s.nom}" for s in self.main_window.subjects],
            width=200
        )
        self.class_subject_combo.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            select_frame,
            text="Afficher",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            command=self._show_class_grades
        ).pack(side="left")
        
        # Zone d'affichage
        self.class_grades_text = ctk.CTkTextbox(self.tab2, height=400)
        self.class_grades_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _create_bulletin_tab(self):
        """Crée l'onglet pour le bulletin complet"""
        # Sélection étudiant
        select_frame = ctk.CTkFrame(self.tab3, fg_color="transparent")
        select_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(select_frame, text="Matricule:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.bulletin_matricule_entry = ctk.CTkEntry(select_frame, width=200, height=40)
        self.bulletin_matricule_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            select_frame,
            text="Afficher le bulletin",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            command=self._show_bulletin
        ).pack(side="left")
        
        # Zone d'affichage
        self.bulletin_text = ctk.CTkTextbox(self.tab3, height=400)
        self.bulletin_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _show_student_grades(self):
        """Affiche les notes d'un étudiant"""
        matricule = self.student_matricule_entry.get().strip()
        student = next((s for s in self.main_window.students if s.matricule == matricule), None)
        
        if not student:
            messagebox.showerror("Erreur", f"Aucun étudiant trouvé avec le matricule {matricule}")
            return
        
        student_grades = [g for g in self.main_window.grades if g.matricule_etudiant == matricule]
        
        self.student_grades_text.delete("1.0", "end")
        text = f"Étudiant: {student.prenom} {student.nom.upper()}\n"
        text += f"Matricule: {student.matricule}\n"
        text += f"Niveau: {student.niveau}\n\n"
        text += f"{len(student_grades)} note(s) trouvée(s):\n\n"
        
        for grade in student_grades:
            subject = next((s for s in self.main_window.subjects if s.code == grade.code_matiere), None)
            subject_name = subject.nom if subject else grade.code_matiere
            text += f"  - {subject_name}: {grade.note}/20 (Date: {grade.date})\n"
        
        if not student_grades:
            text += "  Aucune note enregistrée\n"
        
        self.student_grades_text.insert("1.0", text)
    
    def _show_class_grades(self):
        """Affiche les notes d'une classe pour une matière"""
        niveau = self.class_niveau_entry.get().strip()
        subject_str = self.class_subject_combo.get()
        
        if not subject_str:
            messagebox.showerror("Erreur", "Veuillez sélectionner une matière")
            return
        
        code_matiere = subject_str.split(" - ")[0]
        subject = next((s for s in self.main_window.subjects if s.code == code_matiere), None)
        
        if not subject:
            messagebox.showerror("Erreur", "Matière introuvable")
            return
        
        class_students = [s for s in self.main_window.students if s.niveau == niveau]
        
        self.class_grades_text.delete("1.0", "end")
        text = f"Matière: {subject.nom}\n"
        text += f"Classe: {niveau}\n\n"
        text += f"{len(class_students)} étudiant(s) dans la classe:\n\n"
        
        for student in class_students:
            grade = next((g for g in self.main_window.grades 
                         if g.matricule_etudiant == student.matricule and g.code_matiere == code_matiere), None)
            if grade:
                text += f"  - {student.prenom} {student.nom.upper()} ({student.matricule}): {grade.note}/20\n"
            else:
                text += f"  - {student.prenom} {student.nom.upper()} ({student.matricule}): Pas de note\n"
        
        self.class_grades_text.insert("1.0", text)
    
    def _show_bulletin(self):
        """Affiche le bulletin complet d'un étudiant"""
        matricule = self.bulletin_matricule_entry.get().strip()
        student = next((s for s in self.main_window.students if s.matricule == matricule), None)
        
        if not student:
            messagebox.showerror("Erreur", f"Aucun étudiant trouvé avec le matricule {matricule}")
            return
        
        student_grades = [g for g in self.main_window.grades if g.matricule_etudiant == matricule]
        level_subjects = [s for s in self.main_window.subjects if s.niveau == student.niveau]
        
        stats = Statistics(self.main_window.students, self.main_window.subjects, self.main_window.grades)
        moyenne = stats.calculate_student_average(matricule)
        rang = stats.calculate_student_rank(matricule)
        
        self.bulletin_text.delete("1.0", "end")
        text = "=" * 60 + "\n"
        text += "  BULLETIN DE NOTES\n"
        text += "=" * 60 + "\n\n"
        text += f"Étudiant: {student.prenom} {student.nom.upper()}\n"
        text += f"Matricule: {student.matricule}\n"
        text += f"Niveau: {student.niveau}\n\n"
        text += "=" * 60 + "\n"
        text += f"{'Matière':<30} {'Note':<10} {'Coef':<10} {'Points':<10}\n"
        text += "=" * 60 + "\n"
        
        total_points = 0.0
        total_coefficients = 0.0
        
        for subject in level_subjects:
            grade = next((g for g in student_grades if g.code_matiere == subject.code), None)
            if grade:
                points = grade.note * subject.coefficient
                total_points += points
                total_coefficients += subject.coefficient
                text += f"{subject.nom:<30} {grade.note:<10.2f} {subject.coefficient:<10.2f} {points:<10.2f}\n"
            else:
                text += f"{subject.nom:<30} {'-':<10} {subject.coefficient:<10.2f} {'-':<10}\n"
        
        text += "=" * 60 + "\n"
        if total_coefficients > 0:
            moyenne_calc = total_points / total_coefficients
            text += f"\nMoyenne générale: {moyenne_calc:.2f}/20\n"
            if rang:
                text += f"Rang dans la classe: {rang}{'er' if rang == 1 else 'ème'}\n"
        else:
            text += "\nAucune note enregistrée\n"
        
        text += "=" * 60 + "\n"
        
        self.bulletin_text.insert("1.0", text)
    
    def refresh(self):
        """Rafraîchit la frame"""
        # Mettre à jour les combobox
        self.class_subject_combo.configure(values=[f"{s.code} - {s.nom}" for s in self.main_window.subjects])

