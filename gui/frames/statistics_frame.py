# -*- coding: utf-8 -*-
"""
Frame Statistics - Statistiques et analyses
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.widgets.chart_widget import ChartWidget
from services.statistics import Statistics


class StatisticsFrame(ctk.CTkScrollableFrame):
    """
    Frame pour les statistiques et analyses
    """
    
    def __init__(self, parent, main_window):
        """
        Initialise la frame des statistiques
        
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
            text="Statistiques et Analyses",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 30))
        
        # Onglets
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True)
        
        # Onglet 1: Par étudiant
        self.tab1 = self.tabview.add("Par étudiant")
        self._create_student_stats_tab()
        
        # Onglet 2: Par classe
        self.tab2 = self.tabview.add("Par classe")
        self._create_class_stats_tab()
        
        # Onglet 3: Par matière
        self.tab3 = self.tabview.add("Par matière")
        self._create_subject_stats_tab()
        
        # Onglet 4: Globales
        self.tab4 = self.tabview.add("Globales")
        self._create_global_stats_tab()
    
    def _create_student_stats_tab(self):
        """Crée l'onglet statistiques par étudiant"""
        select_frame = ctk.CTkFrame(self.tab1, fg_color="transparent")
        select_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(select_frame, text="Matricule:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.student_stats_entry = ctk.CTkEntry(select_frame, width=200, height=40)
        self.student_stats_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            select_frame,
            text="Afficher",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            command=self._show_student_stats
        ).pack(side="left")
        
        self.student_stats_text = ctk.CTkTextbox(self.tab1, height=300)
        self.student_stats_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _create_class_stats_tab(self):
        """Crée l'onglet statistiques par classe"""
        select_frame = ctk.CTkFrame(self.tab2, fg_color="transparent")
        select_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(select_frame, text="Niveau:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.class_stats_entry = ctk.CTkEntry(select_frame, width=200, height=40)
        self.class_stats_entry.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            select_frame,
            text="Afficher",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            command=self._show_class_stats
        ).pack(side="left")
        
        self.class_stats_text = ctk.CTkTextbox(self.tab2, height=300)
        self.class_stats_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Graphique de classement
        self.class_chart = ChartWidget(
            self.tab2,
            title="Classement de la classe",
            subtitle="Moyennes des étudiants",
            chart_type="bar"
        )
        self.class_chart.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _create_subject_stats_tab(self):
        """Crée l'onglet statistiques par matière"""
        select_frame = ctk.CTkFrame(self.tab3, fg_color="transparent")
        select_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(select_frame, text="Code matière:", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.subject_stats_combo = ctk.CTkComboBox(
            select_frame,
            values=[f"{s.code} - {s.nom}" for s in self.main_window.subjects],
            width=200
        )
        self.subject_stats_combo.pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            select_frame,
            text="Afficher",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            command=self._show_subject_stats
        ).pack(side="left")
        
        self.subject_stats_text = ctk.CTkTextbox(self.tab3, height=300)
        self.subject_stats_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _create_global_stats_tab(self):
        """Crée l'onglet statistiques globales"""
        ctk.CTkButton(
            self.tab4,
            text="Afficher les statistiques globales",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            command=self._show_global_stats
        ).pack(pady=20)
        
        self.global_stats_text = ctk.CTkTextbox(self.tab4, height=400)
        self.global_stats_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def _show_student_stats(self):
        """Affiche les statistiques d'un étudiant"""
        matricule = self.student_stats_entry.get().strip()
        student = next((s for s in self.main_window.students if s.matricule == matricule), None)
        
        if not student:
            messagebox.showerror("Erreur", f"Aucun étudiant trouvé avec le matricule {matricule}")
            return
        
        stats = Statistics(self.main_window.students, self.main_window.subjects, self.main_window.grades)
        moyenne = stats.calculate_student_average(matricule)
        rang = stats.calculate_student_rank(matricule)
        
        self.student_stats_text.delete("1.0", "end")
        text = f"Étudiant: {student.prenom} {student.nom.upper()}\n"
        text += f"Matricule: {student.matricule}\n"
        text += f"Niveau: {student.niveau}\n\n"
        text += f"Moyenne générale: {moyenne:.2f}/20\n" if moyenne else "Moyenne générale: Aucune note\n"
        if rang:
            text += f"Rang dans la classe: {rang}{'er' if rang == 1 else 'ème'}\n"
        else:
            text += "Rang dans la classe: Non calculable\n"
        
        self.student_stats_text.insert("1.0", text)
    
    def _show_class_stats(self):
        """Affiche les statistiques d'une classe"""
        niveau = self.class_stats_entry.get().strip()
        
        stats = Statistics(self.main_window.students, self.main_window.subjects, self.main_window.grades)
        moyenne_classe = stats.calculate_class_average(niveau)
        meilleur = stats.get_best_student_in_class(niveau)
        classement = stats.get_class_ranking(niveau)
        
        self.class_stats_text.delete("1.0", "end")
        text = f"Classe: {niveau}\n\n"
        text += f"Moyenne générale de la classe: {moyenne_classe:.2f}/20\n" if moyenne_classe else "Moyenne générale: Aucune note\n"
        
        if meilleur:
            student, avg = meilleur
            text += f"\nMeilleur étudiant: {student.prenom} {student.nom.upper()} ({student.matricule})\n"
            text += f"Moyenne: {avg:.2f}/20\n"
        
        if classement:
            text += f"\nClassement complet ({len(classement)} étudiant(s)):\n\n"
            text += f"{'Rang':<6} {'Étudiant':<40} {'Moyenne':<10}\n"
            text += "-" * 60 + "\n"
            for student, avg, rank in classement:
                text += f"{rank:<6} {str(student):<40} {avg:<10.2f}\n"
        
        self.class_stats_text.insert("1.0", text)
        
        # Mettre à jour le graphique
        if classement:
            labels = [f"{s.prenom} {s.nom[:10]}" for s, _, _ in classement]
            values = [avg for _, avg, _ in classement]
            self.class_chart.plot_bar_chart(labels, values, color="#1F6AA5")
    
    def _show_subject_stats(self):
        """Affiche les statistiques d'une matière"""
        subject_str = self.subject_stats_combo.get()
        if not subject_str:
            messagebox.showerror("Erreur", "Veuillez sélectionner une matière")
            return
        
        code_matiere = subject_str.split(" - ")[0]
        subject = next((s for s in self.main_window.subjects if s.code == code_matiere), None)
        
        if not subject:
            messagebox.showerror("Erreur", "Matière introuvable")
            return
        
        stats = Statistics(self.main_window.students, self.main_window.subjects, self.main_window.grades)
        moyenne = stats.calculate_subject_average(code_matiere)
        meilleur = stats.get_best_student_in_subject(code_matiere)
        
        self.subject_stats_text.delete("1.0", "end")
        text = f"Matière: {subject.nom} ({subject.code})\n\n"
        text += f"Moyenne générale: {moyenne:.2f}/20\n" if moyenne else "Moyenne générale: Aucune note\n"
        
        if meilleur:
            student, note = meilleur
            text += f"\nMeilleur étudiant: {student.prenom} {student.nom.upper()} ({student.matricule})\n"
            text += f"Note: {note:.2f}/20\n"
        
        self.subject_stats_text.insert("1.0", text)
    
    def _show_global_stats(self):
        """Affiche les statistiques globales"""
        stats = Statistics(self.main_window.students, self.main_window.subjects, self.main_window.grades)
        moyenne_globale = stats.calculate_global_average()
        meilleur = stats.get_best_student_global()
        
        self.global_stats_text.delete("1.0", "end")
        text = "STATISTIQUES GLOBALES\n"
        text += "=" * 60 + "\n\n"
        text += f"Moyenne générale de l'établissement: {moyenne_globale:.2f}/20\n" if moyenne_globale else "Moyenne générale: Aucune note\n"
        
        if meilleur:
            student, avg = meilleur
            text += f"\nMeilleur étudiant de l'établissement:\n"
            text += f"  {student.prenom} {student.nom.upper()} ({student.matricule})\n"
            text += f"  Niveau: {student.niveau}\n"
            text += f"  Moyenne: {avg:.2f}/20\n"
        
        text += f"\nNombre total d'étudiants: {len(self.main_window.students)}\n"
        text += f"Nombre total de matières: {len(self.main_window.subjects)}\n"
        text += f"Nombre total de notes: {len(self.main_window.grades)}\n"
        
        self.global_stats_text.insert("1.0", text)
    
    def refresh(self):
        """Rafraîchit la frame"""
        self.subject_stats_combo.configure(values=[f"{s.code} - {s.nom}" for s in self.main_window.subjects])

