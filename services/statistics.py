# -*- coding: utf-8 -*-
"""
Module de calcul des statistiques académiques
Calcule les moyennes, classements, rangs et meilleurs étudiants
"""

from typing import List, Dict, Any, Tuple, Optional
from models.student import Student
from models.subject import Subject
from models.grade import Grade


class Statistics:
    """
    Classe pour calculer toutes les statistiques académiques
    """
    
    def __init__(self, students: List[Student], subjects: List[Subject], grades: List[Grade]):
        """
        Initialise le calculateur de statistiques
        
        Args:
            students (List[Student]): Liste des étudiants
            subjects (List[Subject]): Liste des matières
            grades (List[Grade]): Liste des notes
        """
        self.students = students
        self.subjects = subjects
        self.grades = grades
    
    def _get_student_by_matricule(self, matricule: str) -> Optional[Student]:
        """
        Trouve un étudiant par son matricule
        
        Args:
            matricule (str): Matricule de l'étudiant
            
        Returns:
            Optional[Student]: L'étudiant trouvé ou None
        """
        for student in self.students:
            if student.matricule == matricule:
                return student
        return None
    
    def _get_subject_by_code(self, code: str) -> Optional[Subject]:
        """
        Trouve une matière par son code
        
        Args:
            code (str): Code de la matière
            
        Returns:
            Optional[Subject]: La matière trouvée ou None
        """
        for subject in self.subjects:
            if subject.code == code:
                return subject
        return None
    
    def _get_grades_by_matricule(self, matricule: str) -> List[Grade]:
        """
        Récupère toutes les notes d'un étudiant
        
        Args:
            matricule (str): Matricule de l'étudiant
            
        Returns:
            List[Grade]: Liste des notes de l'étudiant
        """
        return [g for g in self.grades if g.matricule_etudiant == matricule]
    
    def _get_grades_by_code_matiere(self, code_matiere: str) -> List[Grade]:
        """
        Récupère toutes les notes d'une matière
        
        Args:
            code_matiere (str): Code de la matière
            
        Returns:
            List[Grade]: Liste des notes de la matière
        """
        return [g for g in self.grades if g.code_matiere == code_matiere]
    
    def _get_grades_by_niveau(self, niveau: str) -> List[Grade]:
        """
        Récupère toutes les notes d'un niveau/classe
        
        Args:
            niveau (str): Niveau/classe
            
        Returns:
            List[Grade]: Liste des notes du niveau
        """
        # Récupérer les matricules des étudiants du niveau
        matricules = [s.matricule for s in self.students if s.niveau == niveau]
        # Récupérer les notes de ces étudiants
        return [g for g in self.grades if g.matricule_etudiant in matricules]
    
    # ========== STATISTIQUES PAR ÉTUDIANT ==========
    
    def calculate_student_average(self, matricule: str) -> Optional[float]:
        """
        Calcule la moyenne générale d'un étudiant (pondérée par les coefficients)
        
        Args:
            matricule (str): Matricule de l'étudiant
            
        Returns:
            Optional[float]: Moyenne générale ou None si aucune note
        """
        student = self._get_student_by_matricule(matricule)
        if not student:
            return None
        
        student_grades = self._get_grades_by_matricule(matricule)
        if not student_grades:
            return None
        
        total_points = 0.0
        total_coefficients = 0.0
        
        for grade in student_grades:
            subject = self._get_subject_by_code(grade.code_matiere)
            if subject and subject.niveau == student.niveau:
                total_points += grade.note * subject.coefficient
                total_coefficients += subject.coefficient
        
        if total_coefficients == 0:
            return None
        
        return total_points / total_coefficients
    
    def calculate_student_rank(self, matricule: str) -> Optional[int]:
        """
        Calcule le rang d'un étudiant dans sa classe
        
        Args:
            matricule (str): Matricule de l'étudiant
            
        Returns:
            Optional[int]: Rang de l'étudiant (1 = premier) ou None
        """
        student = self._get_student_by_matricule(matricule)
        if not student:
            return None
        
        # Récupérer tous les étudiants du même niveau
        class_students = [s for s in self.students if s.niveau == student.niveau]
        
        # Calculer la moyenne de chaque étudiant
        averages = []
        for s in class_students:
            avg = self.calculate_student_average(s.matricule)
            if avg is not None:
                averages.append((s.matricule, avg))
        
        # Trier par moyenne décroissante
        averages.sort(key=lambda x: x[1], reverse=True)
        
        # Trouver le rang
        for rank, (mat, avg) in enumerate(averages, start=1):
            if mat == matricule:
                return rank
        
        return None
    
    # ========== STATISTIQUES PAR CLASSE ==========
    
    def calculate_class_average(self, niveau: str) -> Optional[float]:
        """
        Calcule la moyenne générale d'une classe
        
        Args:
            niveau (str): Niveau/classe
            
        Returns:
            Optional[float]: Moyenne générale de la classe ou None
        """
        class_students = [s for s in self.students if s.niveau == niveau]
        if not class_students:
            return None
        
        averages = []
        for student in class_students:
            avg = self.calculate_student_average(student.matricule)
            if avg is not None:
                averages.append(avg)
        
        if not averages:
            return None
        
        return sum(averages) / len(averages)
    
    def get_best_student_in_class(self, niveau: str) -> Optional[Tuple[Student, float]]:
        """
        Trouve le meilleur étudiant d'une classe
        
        Args:
            niveau (str): Niveau/classe
            
        Returns:
            Optional[Tuple[Student, float]]: (Étudiant, moyenne) ou None
        """
        class_students = [s for s in self.students if s.niveau == niveau]
        if not class_students:
            return None
        
        best_student = None
        best_average = -1.0
        
        for student in class_students:
            avg = self.calculate_student_average(student.matricule)
            if avg is not None and avg > best_average:
                best_average = avg
                best_student = student
        
        if best_student:
            return (best_student, best_average)
        return None
    
    def get_class_ranking(self, niveau: str) -> List[Tuple[Student, float, int]]:
        """
        Obtient le classement complet d'une classe
        
        Args:
            niveau (str): Niveau/classe
            
        Returns:
            List[Tuple[Student, float, int]]: Liste de (étudiant, moyenne, rang)
        """
        class_students = [s for s in self.students if s.niveau == niveau]
        
        # Calculer la moyenne de chaque étudiant
        student_averages = []
        for student in class_students:
            avg = self.calculate_student_average(student.matricule)
            if avg is not None:
                student_averages.append((student, avg))
        
        # Trier par moyenne décroissante
        student_averages.sort(key=lambda x: x[1], reverse=True)
        
        # Ajouter le rang
        ranking = []
        for rank, (student, avg) in enumerate(student_averages, start=1):
            ranking.append((student, avg, rank))
        
        return ranking
    
    # ========== STATISTIQUES PAR MATIÈRE ==========
    
    def calculate_subject_average(self, code_matiere: str) -> Optional[float]:
        """
        Calcule la moyenne générale d'une matière
        
        Args:
            code_matiere (str): Code de la matière
            
        Returns:
            Optional[float]: Moyenne générale de la matière ou None
        """
        subject_grades = self._get_grades_by_code_matiere(code_matiere)
        if not subject_grades:
            return None
        
        total = sum(g.note for g in subject_grades)
        return total / len(subject_grades)
    
    def get_best_student_in_subject(self, code_matiere: str) -> Optional[Tuple[Student, float]]:
        """
        Trouve le meilleur étudiant dans une matière
        
        Args:
            code_matiere (str): Code de la matière
            
        Returns:
            Optional[Tuple[Student, float]]: (Étudiant, note) ou None
        """
        subject_grades = self._get_grades_by_code_matiere(code_matiere)
        if not subject_grades:
            return None
        
        # Trouver la meilleure note
        best_grade = max(subject_grades, key=lambda g: g.note)
        best_student = self._get_student_by_matricule(best_grade.matricule_etudiant)
        
        if best_student:
            return (best_student, best_grade.note)
        return None
    
    # ========== STATISTIQUES GLOBALES ==========
    
    def calculate_global_average(self) -> Optional[float]:
        """
        Calcule la moyenne générale de tout l'établissement
        
        Returns:
            Optional[float]: Moyenne générale globale ou None
        """
        if not self.grades:
            return None
        
        total = sum(g.note for g in self.grades)
        return total / len(self.grades)
    
    def get_best_student_global(self) -> Optional[Tuple[Student, float]]:
        """
        Trouve le meilleur étudiant de tout l'établissement
        
        Returns:
            Optional[Tuple[Student, float]]: (Étudiant, moyenne) ou None
        """
        if not self.students:
            return None
        
        best_student = None
        best_average = -1.0
        
        for student in self.students:
            avg = self.calculate_student_average(student.matricule)
            if avg is not None and avg > best_average:
                best_average = avg
                best_student = student
        
        if best_student:
            return (best_student, best_average)
        return None

