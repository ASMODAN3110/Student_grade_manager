# -*- coding: utf-8 -*-
"""
Frame Dashboard - Vue d'ensemble avec statistiques et graphiques
"""

import customtkinter as ctk
from gui.widgets.stat_card import StatCard
from gui.widgets.chart_widget import ChartWidget
from services.statistics import Statistics


class DashboardFrame(ctk.CTkScrollableFrame):
    """
    Frame du dashboard avec cartes de statistiques et graphiques
    """
    
    def __init__(self, parent, main_window):
        """
        Initialise le dashboard
        
        Args:
            parent: Widget parent
            main_window: Fenêtre principale (pour accéder aux données)
        """
        super().__init__(parent, fg_color="transparent")
        
        self.main_window = main_window
        
        self._create_widgets()
        self._update_statistics()
    
    def _create_widgets(self):
        """Crée les widgets du dashboard"""
        # Titre
        title_label = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(anchor="w", pady=(0, 30))
        
        # Cartes de statistiques
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", pady=(0, 30))
        
        # Grid pour les cartes
        stats_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")
        
        # Carte 1: Total Students
        self.students_card = StatCard(
            stats_frame,
            title="TOTAL STUDENTS",
            value="0",
            subtitle="",
            icon_color="#1F6AA5",
            icon_text="👥"
        )
        self.students_card.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Carte 2: Active Subjects
        self.subjects_card = StatCard(
            stats_frame,
            title="ACTIVE SUBJECTS",
            value="0",
            subtitle="",
            icon_color="#FF9800",
            icon_text="📚"
        )
        self.subjects_card.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Carte 3: Grades Pending
        self.grades_card = StatCard(
            stats_frame,
            title="GRADES PENDING",
            value="0",
            subtitle="",
            icon_color="#9C27B0",
            icon_text="✓"
        )
        self.grades_card.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Carte 4: Average GPA
        self.gpa_card = StatCard(
            stats_frame,
            title="AVERAGE GPA",
            value="0.00",
            subtitle="",
            icon_color="#4CAF50",
            icon_text="📊"
        )
        self.gpa_card.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        
        # Quick Actions
        actions_label = ctk.CTkLabel(
            self,
            text="Quick Actions",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        actions_label.pack(anchor="w", pady=(20, 15))
        
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", pady=(0, 30))
        
        actions_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")
        
        # Bouton Add New Student
        add_student_btn = ctk.CTkButton(
            actions_frame,
            text="➕\nAdd New Student",
            font=ctk.CTkFont(size=14),
            height=100,
            fg_color="#1F6AA5",
            hover_color="#1a5a8a",
            command=lambda: self.main_window._show_frame("students")
        )
        add_student_btn.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Bouton Enter Grades
        enter_grades_btn = ctk.CTkButton(
            actions_frame,
            text="✏️\nEnter Grades",
            font=ctk.CTkFont(size=14),
            height=100,
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=lambda: self.main_window._show_frame("grades")
        )
        enter_grades_btn.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Bouton Print Report
        print_report_btn = ctk.CTkButton(
            actions_frame,
            text="🖨️\nPrint Report Card",
            font=ctk.CTkFont(size=14),
            height=100,
            fg_color="#9C27B0",
            hover_color="#7b1fa2",
            command=lambda: self.main_window._show_frame("consultation")
        )
        print_report_btn.grid(row=0, column=2, padx=10, pady=10, sticky="ew")
        
        # Graphiques
        charts_frame = ctk.CTkFrame(self, fg_color="transparent")
        charts_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        charts_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")
        
        # Graphique 1: Enrollment by Grade
        self.enrollment_chart = ChartWidget(
            charts_frame,
            title="Enrollment by Grade",
            subtitle="Distribution for current term",
            chart_type="bar"
        )
        self.enrollment_chart.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Graphique 2: Average GPA Trend
        self.gpa_trend_chart = ChartWidget(
            charts_frame,
            title="Average GPA Trend",
            subtitle="Academic Year 2024-2025",
            chart_type="line"
        )
        self.gpa_trend_chart.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    def _update_statistics(self):
        """Met à jour les statistiques affichées"""
        # Mettre à jour les cartes
        total_students = len(self.main_window.students)
        total_subjects = len(self.main_window.subjects)
        total_grades = len(self.main_window.grades)
        
        # Calculer la moyenne globale
        stats = Statistics(self.main_window.students, self.main_window.subjects, self.main_window.grades)
        avg_gpa = stats.calculate_global_average()
        avg_gpa_str = f"{avg_gpa:.2f}" if avg_gpa else "0.00"
        
        # Mettre à jour les cartes
        self.students_card.update_value(str(total_students), f"Across {len(set(s.niveau for s in self.main_window.students))} classes")
        self.subjects_card.update_value(str(total_subjects), f"Across {len(set(s.niveau for s in self.main_window.subjects))} levels")
        self.grades_card.update_value(str(total_grades), "Total grades recorded")
        self.gpa_card.update_value(avg_gpa_str, "Overall average")
        
        # Mettre à jour les graphiques
        self._update_charts()
    
    def _update_charts(self):
        """Met à jour les graphiques"""
        # Graphique Enrollment by Grade
        levels = {}
        for student in self.main_window.students:
            level = student.niveau
            levels[level] = levels.get(level, 0) + 1
        
        if levels:
            labels = list(levels.keys())
            values = list(levels.values())
            self.enrollment_chart.plot_bar_chart(labels, values, color="#1F6AA5")
        
        # Graphique GPA Trend (simulation avec données disponibles)
        # Pour un vrai système, on aurait besoin de données historiques
        stats = Statistics(self.main_window.students, self.main_window.subjects, self.main_window.grades)
        
        # Calculer les moyennes par niveau
        level_averages = {}
        for level in set(s.niveau for s in self.main_window.students):
            avg = stats.calculate_class_average(level)
            if avg:
                level_averages[level] = avg
        
        if level_averages:
            labels = list(level_averages.keys())
            values = list(level_averages.values())
            self.gpa_trend_chart.plot_line_chart(labels, values, label="Average GPA", color="#4CAF50")
    
    def refresh(self):
        """Rafraîchit le dashboard"""
        self._update_statistics()

