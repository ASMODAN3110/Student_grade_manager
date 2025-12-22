# -*- coding: utf-8 -*-
"""
Module de gestion des menus console
Gère toute l'interface utilisateur et la navigation
"""

import os
from typing import List, Optional
from models.student import Student
from models.subject import Subject
from models.grade import Grade
from services.file_manager import FileManager
from services.statistics import Statistics


class Menu:
    """
    Classe pour gérer tous les menus et l'interface utilisateur
    """
    
    def __init__(self, file_manager: FileManager):
        """
        Initialise le système de menus
        
        Args:
            file_manager (FileManager): Gestionnaire de fichiers
        """
        self.file_manager = file_manager
        self.students: List[Student] = []
        self.subjects: List[Subject] = []
        self.grades: List[Grade] = []
        self._load_data()
    
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
        # Sauvegarder les étudiants
        students_data = [s.to_dict() for s in self.students]
        self.file_manager.save_students(students_data)
        
        # Sauvegarder les matières
        subjects_data = [s.to_dict() for s in self.subjects]
        self.file_manager.save_subjects(subjects_data)
        
        # Sauvegarder les notes
        grades_data = [g.to_dict() for g in self.grades]
        self.file_manager.save_grades(grades_data)
    
    def _clear_screen(self):
        """Efface l'écran de la console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def _press_enter(self):
        """Attend que l'utilisateur appuie sur Entrée"""
        input("\nAppuyez sur Entrée pour continuer...")
    
    def _get_input(self, prompt: str, default: str = "") -> str:
        """
        Demande une saisie à l'utilisateur
        
        Args:
            prompt (str): Message à afficher
            default (str): Valeur par défaut
            
        Returns:
            str: Saisie de l'utilisateur
        """
        if default:
            response = input(f"{prompt} [{default}]: ").strip()
            return response if response else default
        else:
            return input(f"{prompt}: ").strip()
    
    # ========== MENU PRINCIPAL ==========
    
    def show_main_menu(self):
        """Affiche le menu principal"""
        self._clear_screen()
        print("=" * 60)
        print("    SYSTÈME DE GESTION DES NOTES SCOLAIRES")
        print("=" * 60)
        print("\nMENU PRINCIPAL\n")
        print("1. Gestion des étudiants")
        print("2. Gestion des matières")
        print("3. Saisie des notes")
        print("4. Consultation des notes")
        print("5. Statistiques et analyses")
        print("6. Quitter")
        print("\n" + "=" * 60)
    
    def handle_main_menu(self):
        """Gère la navigation du menu principal"""
        while True:
            self.show_main_menu()
            choice = input("\nVotre choix: ").strip()
            
            if choice == '1':
                self.handle_students_menu()
            elif choice == '2':
                self.handle_subjects_menu()
            elif choice == '3':
                self.handle_grades_menu()
            elif choice == '4':
                self.handle_consultation_menu()
            elif choice == '5':
                self.handle_statistics_menu()
            elif choice == '6':
                print("\nAu revoir !")
                break
            else:
                print("\nChoix invalide !")
                self._press_enter()
    
    # ========== GESTION DES ÉTUDIANTS ==========
    
    def handle_students_menu(self):
        """Gère le menu de gestion des étudiants"""
        while True:
            self._clear_screen()
            print("=" * 60)
            print("    GESTION DES ÉTUDIANTS")
            print("=" * 60)
            print("\n1. Ajouter un étudiant")
            print("2. Modifier un étudiant")
            print("3. Supprimer un étudiant")
            print("4. Rechercher un étudiant")
            print("5. Lister les étudiants")
            print("6. Retour au menu principal")
            
            choice = input("\nVotre choix: ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.modify_student()
            elif choice == '3':
                self.delete_student()
            elif choice == '4':
                self.search_student()
            elif choice == '5':
                self.list_students()
            elif choice == '6':
                break
            else:
                print("\nChoix invalide !")
                self._press_enter()
    
    def add_student(self):
        """Ajoute un nouvel étudiant"""
        self._clear_screen()
        print("=" * 60)
        print("    AJOUT D'UN ÉTUDIANT")
        print("=" * 60)
        
        nom = self._get_input("Nom")
        prenom = self._get_input("Prénom")
        matricule = self._get_input("Matricule")
        niveau = self._get_input("Niveau/Classe")
        
        # Vérifier que le matricule est unique
        if any(s.matricule == matricule for s in self.students):
            print(f"\nErreur: Le matricule {matricule} existe déjà !")
            self._press_enter()
            return
        
        student = Student(nom, prenom, matricule, niveau)
        is_valid, error_msg = student.validate()
        
        if not is_valid:
            print(f"\nErreur: {error_msg}")
            self._press_enter()
            return
        
        self.students.append(student)
        self._save_data()
        print(f"\n✓ Étudiant ajouté avec succès: {student}")
        self._press_enter()
    
    def modify_student(self):
        """Modifie un étudiant existant"""
        self._clear_screen()
        print("=" * 60)
        print("    MODIFICATION D'UN ÉTUDIANT")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant à modifier")
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\nErreur: Aucun étudiant trouvé avec le matricule {matricule}")
            self._press_enter()
            return
        
        print(f"\nÉtudiant trouvé: {student}")
        print("\nLaissez vide pour conserver la valeur actuelle")
        
        nom = self._get_input("Nouveau nom", student.nom)
        prenom = self._get_input("Nouveau prénom", student.prenom)
        niveau = self._get_input("Nouveau niveau", student.niveau)
        
        student.nom = nom
        student.prenom = prenom
        student.niveau = niveau
        
        is_valid, error_msg = student.validate()
        if not is_valid:
            print(f"\nErreur: {error_msg}")
            self._press_enter()
            return
        
        self._save_data()
        print(f"\n✓ Étudiant modifié avec succès: {student}")
        self._press_enter()
    
    def delete_student(self):
        """Supprime un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print("    SUPPRESSION D'UN ÉTUDIANT")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant à supprimer")
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\nErreur: Aucun étudiant trouvé avec le matricule {matricule}")
            self._press_enter()
            return
        
        print(f"\nÉtudiant trouvé: {student}")
        confirm = input("\nÊtes-vous sûr de vouloir supprimer cet étudiant ? (o/n): ").strip().lower()
        
        if confirm == 'o':
            # Supprimer aussi toutes ses notes
            self.grades = [g for g in self.grades if g.matricule_etudiant != matricule]
            self.students.remove(student)
            self._save_data()
            print("\n✓ Étudiant et ses notes supprimés avec succès")
        else:
            print("\nSuppression annulée")
        
        self._press_enter()
    
    def search_student(self):
        """Recherche un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print("    RECHERCHE D'UN ÉTUDIANT")
        print("=" * 60)
        
        search_term = self._get_input("Matricule, nom ou prénom à rechercher").lower()
        
        results = []
        for student in self.students:
            if (search_term in student.matricule.lower() or
                search_term in student.nom.lower() or
                search_term in student.prenom.lower()):
                results.append(student)
        
        if results:
            print(f"\n{len(results)} résultat(s) trouvé(s):\n")
            for i, student in enumerate(results, 1):
                print(f"{i}. {student}")
        else:
            print("\nAucun résultat trouvé")
        
        self._press_enter()
    
    def list_students(self):
        """Liste les étudiants"""
        self._clear_screen()
        print("=" * 60)
        print("    LISTE DES ÉTUDIANTS")
        print("=" * 60)
        
        niveau = self._get_input("Niveau/Classe (laissez vide pour tous)")
        
        if niveau:
            filtered = [s for s in self.students if s.niveau == niveau]
        else:
            filtered = self.students
        
        if filtered:
            print(f"\n{len(filtered)} étudiant(s) trouvé(s):\n")
            for i, student in enumerate(filtered, 1):
                print(f"{i}. {student}")
        else:
            print("\nAucun étudiant trouvé")
        
        self._press_enter()
    
    def _find_student_by_matricule(self, matricule: str) -> Optional[Student]:
        """Trouve un étudiant par son matricule"""
        for student in self.students:
            if student.matricule == matricule:
                return student
        return None
    
    # ========== GESTION DES MATIÈRES ==========
    
    def handle_subjects_menu(self):
        """Gère le menu de gestion des matières"""
        while True:
            self._clear_screen()
            print("=" * 60)
            print("    GESTION DES MATIÈRES")
            print("=" * 60)
            print("\n1. Ajouter une matière")
            print("2. Modifier une matière")
            print("3. Supprimer une matière")
            print("4. Lister les matières")
            print("5. Retour au menu principal")
            
            choice = input("\nVotre choix: ").strip()
            
            if choice == '1':
                self.add_subject()
            elif choice == '2':
                self.modify_subject()
            elif choice == '3':
                self.delete_subject()
            elif choice == '4':
                self.list_subjects()
            elif choice == '5':
                break
            else:
                print("\nChoix invalide !")
                self._press_enter()
    
    def add_subject(self):
        """Ajoute une nouvelle matière"""
        self._clear_screen()
        print("=" * 60)
        print("    AJOUT D'UNE MATIÈRE")
        print("=" * 60)
        
        nom = self._get_input("Nom de la matière")
        code = self._get_input("Code de la matière")
        coefficient = self._get_input("Coefficient", "1.0")
        niveau = self._get_input("Niveau/Classe concerné")
        
        # Vérifier que le code est unique
        if any(s.code == code for s in self.subjects):
            print(f"\nErreur: Le code {code} existe déjà !")
            self._press_enter()
            return
        
        try:
            coef = float(coefficient)
        except ValueError:
            print("\nErreur: Le coefficient doit être un nombre")
            self._press_enter()
            return
        
        subject = Subject(nom, code, coef, niveau)
        is_valid, error_msg = subject.validate()
        
        if not is_valid:
            print(f"\nErreur: {error_msg}")
            self._press_enter()
            return
        
        self.subjects.append(subject)
        self._save_data()
        print(f"\n✓ Matière ajoutée avec succès: {subject}")
        self._press_enter()
    
    def modify_subject(self):
        """Modifie une matière existante"""
        self._clear_screen()
        print("=" * 60)
        print("    MODIFICATION D'UNE MATIÈRE")
        print("=" * 60)
        
        code = self._get_input("Code de la matière à modifier")
        subject = self._find_subject_by_code(code)
        
        if not subject:
            print(f"\nErreur: Aucune matière trouvée avec le code {code}")
            self._press_enter()
            return
        
        print(f"\nMatière trouvée: {subject}")
        print("\nLaissez vide pour conserver la valeur actuelle")
        
        nom = self._get_input("Nouveau nom", subject.nom)
        coefficient = self._get_input("Nouveau coefficient", str(subject.coefficient))
        niveau = self._get_input("Nouveau niveau", subject.niveau)
        
        try:
            coef = float(coefficient)
        except ValueError:
            print("\nErreur: Le coefficient doit être un nombre")
            self._press_enter()
            return
        
        subject.nom = nom
        subject.coefficient = coef
        subject.niveau = niveau
        
        is_valid, error_msg = subject.validate()
        if not is_valid:
            print(f"\nErreur: {error_msg}")
            self._press_enter()
            return
        
        self._save_data()
        print(f"\n✓ Matière modifiée avec succès: {subject}")
        self._press_enter()
    
    def delete_subject(self):
        """Supprime une matière"""
        self._clear_screen()
        print("=" * 60)
        print("    SUPPRESSION D'UNE MATIÈRE")
        print("=" * 60)
        
        code = self._get_input("Code de la matière à supprimer")
        subject = self._find_subject_by_code(code)
        
        if not subject:
            print(f"\nErreur: Aucune matière trouvée avec le code {code}")
            self._press_enter()
            return
        
        print(f"\nMatière trouvée: {subject}")
        confirm = input("\nÊtes-vous sûr de vouloir supprimer cette matière ? (o/n): ").strip().lower()
        
        if confirm == 'o':
            # Supprimer aussi toutes les notes de cette matière
            self.grades = [g for g in self.grades if g.code_matiere != code]
            self.subjects.remove(subject)
            self._save_data()
            print("\n✓ Matière et ses notes supprimées avec succès")
        else:
            print("\nSuppression annulée")
        
        self._press_enter()
    
    def list_subjects(self):
        """Liste les matières"""
        self._clear_screen()
        print("=" * 60)
        print("    LISTE DES MATIÈRES")
        print("=" * 60)
        
        niveau = self._get_input("Niveau/Classe (laissez vide pour tous)")
        
        if niveau:
            filtered = [s for s in self.subjects if s.niveau == niveau]
        else:
            filtered = self.subjects
        
        if filtered:
            print(f"\n{len(filtered)} matière(s) trouvée(s):\n")
            for i, subject in enumerate(filtered, 1):
                print(f"{i}. {subject}")
        else:
            print("\nAucune matière trouvée")
        
        self._press_enter()
    
    def _find_subject_by_code(self, code: str) -> Optional[Subject]:
        """Trouve une matière par son code"""
        for subject in self.subjects:
            if subject.code == code:
                return subject
        return None
    
    # ========== GESTION DES NOTES ==========
    
    def handle_grades_menu(self):
        """Gère le menu de saisie des notes"""
        while True:
            self._clear_screen()
            print("=" * 60)
            print("    SAISIE DES NOTES")
            print("=" * 60)
            print("\n1. Enregistrer une note")
            print("2. Modifier une note")
            print("3. Supprimer une note")
            print("4. Retour au menu principal")
            
            choice = input("\nVotre choix: ").strip()
            
            if choice == '1':
                self.add_grade()
            elif choice == '2':
                self.modify_grade()
            elif choice == '3':
                self.delete_grade()
            elif choice == '4':
                break
            else:
                print("\nChoix invalide !")
                self._press_enter()
    
    def add_grade(self):
        """Ajoute une nouvelle note"""
        self._clear_screen()
        print("=" * 60)
        print("    ENREGISTREMENT D'UNE NOTE")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant")
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\nErreur: Aucun étudiant trouvé avec le matricule {matricule}")
            self._press_enter()
            return
        
        code_matiere = self._get_input("Code de la matière")
        subject = self._find_subject_by_code(code_matiere)
        
        if not subject:
            print(f"\nErreur: Aucune matière trouvée avec le code {code_matiere}")
            self._press_enter()
            return
        
        # Vérifier qu'il n'y a pas déjà une note pour cet étudiant dans cette matière
        existing = [g for g in self.grades 
                   if g.matricule_etudiant == matricule and g.code_matiere == code_matiere]
        if existing:
            print(f"\nErreur: Une note existe déjà pour cet étudiant dans cette matière")
            print(f"Note existante: {existing[0].note}/20")
            self._press_enter()
            return
        
        note_str = self._get_input("Note (0-20)")
        
        try:
            note = float(note_str)
        except ValueError:
            print("\nErreur: La note doit être un nombre")
            self._press_enter()
            return
        
        grade = Grade(matricule, code_matiere, note)
        is_valid, error_msg = grade.validate()
        
        if not is_valid:
            print(f"\nErreur: {error_msg}")
            self._press_enter()
            return
        
        self.grades.append(grade)
        self._save_data()
        print(f"\n✓ Note enregistrée avec succès: {grade}")
        self._press_enter()
    
    def modify_grade(self):
        """Modifie une note existante"""
        self._clear_screen()
        print("=" * 60)
        print("    MODIFICATION D'UNE NOTE")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant")
        code_matiere = self._get_input("Code de la matière")
        
        grade = self._find_grade(matricule, code_matiere)
        
        if not grade:
            print(f"\nErreur: Aucune note trouvée pour cet étudiant dans cette matière")
            self._press_enter()
            return
        
        print(f"\nNote trouvée: {grade.note}/20")
        note_str = self._get_input("Nouvelle note (0-20)", str(grade.note))
        
        try:
            note = float(note_str)
        except ValueError:
            print("\nErreur: La note doit être un nombre")
            self._press_enter()
            return
        
        grade.note = note
        is_valid, error_msg = grade.validate()
        
        if not is_valid:
            print(f"\nErreur: {error_msg}")
            self._press_enter()
            return
        
        self._save_data()
        print(f"\n✓ Note modifiée avec succès: {grade}")
        self._press_enter()
    
    def delete_grade(self):
        """Supprime une note"""
        self._clear_screen()
        print("=" * 60)
        print("    SUPPRESSION D'UNE NOTE")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant")
        code_matiere = self._get_input("Code de la matière")
        
        grade = self._find_grade(matricule, code_matiere)
        
        if not grade:
            print(f"\nErreur: Aucune note trouvée pour cet étudiant dans cette matière")
            self._press_enter()
            return
        
        print(f"\nNote trouvée: {grade.note}/20")
        confirm = input("\nÊtes-vous sûr de vouloir supprimer cette note ? (o/n): ").strip().lower()
        
        if confirm == 'o':
            self.grades.remove(grade)
            self._save_data()
            print("\n✓ Note supprimée avec succès")
        else:
            print("\nSuppression annulée")
        
        self._press_enter()
    
    def _find_grade(self, matricule: str, code_matiere: str) -> Optional[Grade]:
        """Trouve une note par matricule et code matière"""
        for grade in self.grades:
            if grade.matricule_etudiant == matricule and grade.code_matiere == code_matiere:
                return grade
        return None
    
    # ========== CONSULTATION DES NOTES ==========
    
    def handle_consultation_menu(self):
        """Gère le menu de consultation des notes"""
        while True:
            self._clear_screen()
            print("=" * 60)
            print("    CONSULTATION DES NOTES")
            print("=" * 60)
            print("\n1. Notes d'un étudiant")
            print("2. Notes d'une classe pour une matière")
            print("3. Bulletin complet d'un étudiant")
            print("4. Retour au menu principal")
            
            choice = input("\nVotre choix: ").strip()
            
            if choice == '1':
                self.show_student_grades()
            elif choice == '2':
                self.show_class_grades_for_subject()
            elif choice == '3':
                self.show_student_bulletin()
            elif choice == '4':
                break
            else:
                print("\nChoix invalide !")
                self._press_enter()
    
    def show_student_grades(self):
        """Affiche les notes d'un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print("    NOTES D'UN ÉTUDIANT")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant")
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\nErreur: Aucun étudiant trouvé avec le matricule {matricule}")
            self._press_enter()
            return
        
        student_grades = [g for g in self.grades if g.matricule_etudiant == matricule]
        
        print(f"\nÉtudiant: {student}")
        print(f"\n{len(student_grades)} note(s) trouvée(s):\n")
        
        for grade in student_grades:
            subject = self._find_subject_by_code(grade.code_matiere)
            subject_name = subject.nom if subject else grade.code_matiere
            print(f"  - {subject_name}: {grade.note}/20 (Date: {grade.date})")
        
        if not student_grades:
            print("  Aucune note enregistrée")
        
        self._press_enter()
    
    def show_class_grades_for_subject(self):
        """Affiche les notes d'une classe pour une matière"""
        self._clear_screen()
        print("=" * 60)
        print("    NOTES D'UNE CLASSE POUR UNE MATIÈRE")
        print("=" * 60)
        
        niveau = self._get_input("Niveau/Classe")
        code_matiere = self._get_input("Code de la matière")
        
        subject = self._find_subject_by_code(code_matiere)
        if not subject:
            print(f"\nErreur: Aucune matière trouvée avec le code {code_matiere}")
            self._press_enter()
            return
        
        # Récupérer les étudiants de la classe
        class_students = [s for s in self.students if s.niveau == niveau]
        
        print(f"\nMatière: {subject.nom}")
        print(f"Classe: {niveau}")
        print(f"\n{len(class_students)} étudiant(s) dans la classe:\n")
        
        for student in class_students:
            grade = self._find_grade(student.matricule, code_matiere)
            if grade:
                print(f"  - {student.prenom} {student.nom.upper()} ({student.matricule}): {grade.note}/20")
            else:
                print(f"  - {student.prenom} {student.nom.upper()} ({student.matricule}): Pas de note")
        
        self._press_enter()
    
    def show_student_bulletin(self):
        """Affiche le bulletin complet d'un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print("    BULLETIN COMPLET D'UN ÉTUDIANT")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant")
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\nErreur: Aucun étudiant trouvé avec le matricule {matricule}")
            self._press_enter()
            return
        
        # Récupérer les notes de l'étudiant
        student_grades = [g for g in self.grades if g.matricule_etudiant == matricule]
        
        # Récupérer les matières du niveau de l'étudiant
        level_subjects = [s for s in self.subjects if s.niveau == student.niveau]
        
        # Calculer les statistiques
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne = stats.calculate_student_average(matricule)
        rang = stats.calculate_student_rank(matricule)
        
        print(f"\n{'='*60}")
        print(f"  BULLETIN DE NOTES")
        print(f"{'='*60}")
        print(f"\nÉtudiant: {student.prenom} {student.nom.upper()}")
        print(f"Matricule: {student.matricule}")
        print(f"Niveau: {student.niveau}")
        print(f"\n{'='*60}")
        print(f"{'Matière':<30} {'Note':<10} {'Coef':<10} {'Points':<10}")
        print(f"{'='*60}")
        
        total_points = 0.0
        total_coefficients = 0.0
        
        for subject in level_subjects:
            grade = self._find_grade(matricule, subject.code)
            if grade:
                points = grade.note * subject.coefficient
                total_points += points
                total_coefficients += subject.coefficient
                print(f"{subject.nom:<30} {grade.note:<10.2f} {subject.coefficient:<10.2f} {points:<10.2f}")
            else:
                print(f"{subject.nom:<30} {'-':<10} {subject.coefficient:<10.2f} {'-':<10}")
        
        print(f"{'='*60}")
        if total_coefficients > 0:
            moyenne_calc = total_points / total_coefficients
            print(f"\nMoyenne générale: {moyenne_calc:.2f}/20")
            if rang:
                print(f"Rang dans la classe: {rang}{'er' if rang == 1 else 'ème'}")
        else:
            print("\nAucune note enregistrée")
        
        print(f"{'='*60}")
        self._press_enter()
    
    # ========== STATISTIQUES ==========
    
    def handle_statistics_menu(self):
        """Gère le menu des statistiques"""
        while True:
            self._clear_screen()
            print("=" * 60)
            print("    STATISTIQUES ET ANALYSES")
            print("=" * 60)
            print("\n1. Statistiques par étudiant")
            print("2. Statistiques par classe")
            print("3. Statistiques par matière")
            print("4. Statistiques globales")
            print("5. Retour au menu principal")
            
            choice = input("\nVotre choix: ").strip()
            
            if choice == '1':
                self.show_student_statistics()
            elif choice == '2':
                self.show_class_statistics()
            elif choice == '3':
                self.show_subject_statistics()
            elif choice == '4':
                self.show_global_statistics()
            elif choice == '5':
                break
            else:
                print("\nChoix invalide !")
                self._press_enter()
    
    def show_student_statistics(self):
        """Affiche les statistiques d'un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print("    STATISTIQUES PAR ÉTUDIANT")
        print("=" * 60)
        
        matricule = self._get_input("Matricule de l'étudiant")
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\nErreur: Aucun étudiant trouvé avec le matricule {matricule}")
            self._press_enter()
            return
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne = stats.calculate_student_average(matricule)
        rang = stats.calculate_student_rank(matricule)
        
        print(f"\nÉtudiant: {student}")
        print(f"\nMoyenne générale: {moyenne:.2f}/20" if moyenne else "\nMoyenne générale: Aucune note")
        if rang:
            print(f"Rang dans la classe: {rang}{'er' if rang == 1 else 'ème'}")
        else:
            print("Rang dans la classe: Non calculable")
        
        self._press_enter()
    
    def show_class_statistics(self):
        """Affiche les statistiques d'une classe"""
        self._clear_screen()
        print("=" * 60)
        print("    STATISTIQUES PAR CLASSE")
        print("=" * 60)
        
        niveau = self._get_input("Niveau/Classe")
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne_classe = stats.calculate_class_average(niveau)
        meilleur = stats.get_best_student_in_class(niveau)
        classement = stats.get_class_ranking(niveau)
        
        print(f"\nClasse: {niveau}")
        print(f"\nMoyenne générale de la classe: {moyenne_classe:.2f}/20" if moyenne_classe else "\nMoyenne générale: Aucune note")
        
        if meilleur:
            student, avg = meilleur
            print(f"\nMeilleur étudiant: {student.prenom} {student.nom.upper()} ({student.matricule})")
            print(f"Moyenne: {avg:.2f}/20")
        
        if classement:
            print(f"\nClassement complet ({len(classement)} étudiant(s)):\n")
            print(f"{'Rang':<6} {'Étudiant':<40} {'Moyenne':<10}")
            print("-" * 60)
            for student, avg, rank in classement:
                print(f"{rank:<6} {str(student):<40} {avg:<10.2f}")
        
        self._press_enter()
    
    def show_subject_statistics(self):
        """Affiche les statistiques d'une matière"""
        self._clear_screen()
        print("=" * 60)
        print("    STATISTIQUES PAR MATIÈRE")
        print("=" * 60)
        
        code_matiere = self._get_input("Code de la matière")
        subject = self._find_subject_by_code(code_matiere)
        
        if not subject:
            print(f"\nErreur: Aucune matière trouvée avec le code {code_matiere}")
            self._press_enter()
            return
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne = stats.calculate_subject_average(code_matiere)
        meilleur = stats.get_best_student_in_subject(code_matiere)
        
        print(f"\nMatière: {subject.nom} ({subject.code})")
        print(f"\nMoyenne générale: {moyenne:.2f}/20" if moyenne else "\nMoyenne générale: Aucune note")
        
        if meilleur:
            student, note = meilleur
            print(f"\nMeilleur étudiant: {student.prenom} {student.nom.upper()} ({student.matricule})")
            print(f"Note: {note:.2f}/20")
        
        self._press_enter()
    
    def show_global_statistics(self):
        """Affiche les statistiques globales"""
        self._clear_screen()
        print("=" * 60)
        print("    STATISTIQUES GLOBALES")
        print("=" * 60)
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne_globale = stats.calculate_global_average()
        meilleur = stats.get_best_student_global()
        
        print(f"\nMoyenne générale de l'établissement: {moyenne_globale:.2f}/20" if moyenne_globale else "\nMoyenne générale: Aucune note")
        
        if meilleur:
            student, avg = meilleur
            print(f"\nMeilleur étudiant de l'établissement:")
            print(f"  {student.prenom} {student.nom.upper()} ({student.matricule})")
            print(f"  Niveau: {student.niveau}")
            print(f"  Moyenne: {avg:.2f}/20")
        
        print(f"\nNombre total d'étudiants: {len(self.students)}")
        print(f"Nombre total de matières: {len(self.subjects)}")
        print(f"Nombre total de notes: {len(self.grades)}")
        
        self._press_enter()

