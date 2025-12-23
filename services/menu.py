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
from services.i18n import TranslationManager


class Menu:
    """
    Classe pour gérer tous les menus et l'interface utilisateur
    """
    
    def __init__(self, file_manager: FileManager, i18n: TranslationManager):
        """
        Initialise le système de menus
        
        Args:
            file_manager (FileManager): Gestionnaire de fichiers
            i18n (TranslationManager): Gestionnaire de traductions
        """
        self.file_manager = file_manager
        self.i18n = i18n
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
        input(f"\n{self.i18n.get('common.press_enter')}")
    
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
        print(f"    {self.i18n.get('app.title')}")
        print("=" * 60)
        print(f"\n{self.i18n.get('menu.main.title')}\n")
        print(f"1. {self.i18n.get('menu.main.option_1')}")
        print(f"2. {self.i18n.get('menu.main.option_2')}")
        print(f"3. {self.i18n.get('menu.main.option_3')}")
        print(f"4. {self.i18n.get('menu.main.option_4')}")
        print(f"5. {self.i18n.get('menu.main.option_5')}")
        print(f"6. {self.i18n.get('menu.main.option_6')}")
        print(f"7. {self.i18n.get('menu.main.option_7')}")
        print("\n" + "=" * 60)
    
    def handle_main_menu(self):
        """Gère la navigation du menu principal"""
        while True:
            self.show_main_menu()
            choice = input(f"\n{self.i18n.get('menu.main.choice')}").strip()
            
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
                print(f"\n{self.i18n.get('app.goodbye')}")
                break
            elif choice == '7':
                self.handle_language_menu()
            else:
                print(f"\n{self.i18n.get('menu.main.invalid')}")
                self._press_enter()
    
    # ========== CHANGEMENT DE LANGUE ==========
    
    def handle_language_menu(self):
        """Gère le menu de changement de langue"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('menu.language.title')}")
        print("=" * 60)
        
        current_lang = self.i18n.get_current_language()
        lang_name = "Français" if current_lang == "fr" else "English"
        print(f"\n{self.i18n.get('menu.language.current', lang=lang_name)}")
        print(f"\n1. {self.i18n.get('menu.language.option_1')}")
        print(f"2. {self.i18n.get('menu.language.option_2')}")
        print(f"3. {self.i18n.get('menu.language.option_3')}")
        
        choice = input(f"\n{self.i18n.get('menu.language.choice')}").strip()
        
        if choice == '1':
            self.i18n.set_language('fr')
            self.file_manager.save_language('fr')
            print(f"\n{self.i18n.get('menu.language.changed')}")
            self._press_enter()
        elif choice == '2':
            self.i18n.set_language('en')
            self.file_manager.save_language('en')
            print(f"\n{self.i18n.get('menu.language.changed')}")
            self._press_enter()
        elif choice == '3':
            return
        else:
            print(f"\n{self.i18n.get('menu.main.invalid')}")
            self._press_enter()
    
    # ========== GESTION DES ÉTUDIANTS ==========
    
    def handle_students_menu(self):
        """Gère le menu de gestion des étudiants"""
        while True:
            self._clear_screen()
            print("=" * 60)
            print(f"    {self.i18n.get('menu.students.title')}")
            print("=" * 60)
            print(f"\n1. {self.i18n.get('menu.students.option_1')}")
            print(f"2. {self.i18n.get('menu.students.option_2')}")
            print(f"3. {self.i18n.get('menu.students.option_3')}")
            print(f"4. {self.i18n.get('menu.students.option_4')}")
            print(f"5. {self.i18n.get('menu.students.option_5')}")
            print(f"6. {self.i18n.get('menu.students.option_6')}")
            
            choice = input(f"\n{self.i18n.get('menu.main.choice')}").strip()
            
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
                print(f"\n{self.i18n.get('menu.main.invalid')}")
                self._press_enter()
    
    def add_student(self):
        """Ajoute un nouvel étudiant"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('students.add.title')}")
        print("=" * 60)
        
        nom = self._get_input(self.i18n.get('students.add.name'))
        prenom = self._get_input(self.i18n.get('students.add.firstname'))
        matricule = self._get_input(self.i18n.get('students.add.matricule'))
        niveau = self._get_input(self.i18n.get('students.add.level'))
        
        # Vérifier que le matricule est unique
        if any(s.matricule == matricule for s in self.students):
            print(f"\n{self.i18n.get('students.add.matricule_exists', matricule=matricule)}")
            self._press_enter()
            return
        
        student = Student(nom, prenom, matricule, niveau)
        is_valid, error_msg = student.validate()
        
        if not is_valid:
            print(f"\n{self.i18n.get('students.add.validation_error', error=error_msg)}")
            self._press_enter()
            return
        
        self.students.append(student)
        self._save_data()
        print(f"\n{self.i18n.get('students.add.success', student=str(student))}")
        self._press_enter()
    
    def modify_student(self):
        """Modifie un étudiant existant"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('students.modify.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('students.modify.matricule_prompt'))
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\n{self.i18n.get('students.modify.not_found', matricule=matricule)}")
            self._press_enter()
            return
        
        print(f"\n{self.i18n.get('students.modify.found', student=str(student))}")
        print(f"\n{self.i18n.get('students.modify.keep_current')}")
        
        nom = self._get_input(self.i18n.get('students.modify.new_name'), student.nom)
        prenom = self._get_input(self.i18n.get('students.modify.new_firstname'), student.prenom)
        niveau = self._get_input(self.i18n.get('students.modify.new_level'), student.niveau)
        
        student.nom = nom
        student.prenom = prenom
        student.niveau = niveau
        
        is_valid, error_msg = student.validate()
        if not is_valid:
            print(f"\n{self.i18n.get('students.modify.validation_error', error=error_msg)}")
            self._press_enter()
            return
        
        self._save_data()
        print(f"\n{self.i18n.get('students.modify.success', student=str(student))}")
        self._press_enter()
    
    def delete_student(self):
        """Supprime un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('students.delete.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('students.delete.matricule_prompt'))
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\n{self.i18n.get('students.delete.not_found', matricule=matricule)}")
            self._press_enter()
            return
        
        print(f"\n{self.i18n.get('students.delete.found', student=str(student))}")
        confirm = input(f"\n{self.i18n.get('students.delete.confirm')}").strip().lower()
        
        if confirm == 'o' or confirm == 'y':
            # Supprimer aussi toutes ses notes
            self.grades = [g for g in self.grades if g.matricule_etudiant != matricule]
            self.students.remove(student)
            self._save_data()
            print(f"\n{self.i18n.get('students.delete.success')}")
        else:
            print(f"\n{self.i18n.get('students.delete.cancelled')}")
        
        self._press_enter()
    
    def search_student(self):
        """Recherche un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('students.search.title')}")
        print("=" * 60)
        
        search_term = self._get_input(self.i18n.get('students.search.prompt')).lower()
        
        results = []
        for student in self.students:
            if (search_term in student.matricule.lower() or
                search_term in student.nom.lower() or
                search_term in student.prenom.lower()):
                results.append(student)
        
        if results:
            print(f"\n{self.i18n.get('students.search.results', count=len(results))}\n")
            for i, student in enumerate(results, 1):
                print(f"{i}. {student}")
        else:
            print(f"\n{self.i18n.get('students.search.no_results')}")
        
        self._press_enter()
    
    def list_students(self):
        """Liste les étudiants"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('students.list.title')}")
        print("=" * 60)
        
        niveau = self._get_input(self.i18n.get('students.list.level_prompt'))
        
        if niveau:
            filtered = [s for s in self.students if s.niveau == niveau]
        else:
            filtered = self.students
        
        if filtered:
            print(f"\n{self.i18n.get('students.list.results', count=len(filtered))}\n")
            for i, student in enumerate(filtered, 1):
                print(f"{i}. {student}")
        else:
            print(f"\n{self.i18n.get('students.list.no_results')}")
        
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
            print(f"    {self.i18n.get('menu.subjects.title')}")
            print("=" * 60)
            print(f"\n1. {self.i18n.get('menu.subjects.option_1')}")
            print(f"2. {self.i18n.get('menu.subjects.option_2')}")
            print(f"3. {self.i18n.get('menu.subjects.option_3')}")
            print(f"4. {self.i18n.get('menu.subjects.option_4')}")
            print(f"5. {self.i18n.get('menu.subjects.option_5')}")
            
            choice = input(f"\n{self.i18n.get('menu.main.choice')}").strip()
            
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
                print(f"\n{self.i18n.get('menu.main.invalid')}")
                self._press_enter()
    
    def add_subject(self):
        """Ajoute une nouvelle matière"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('subjects.add.title')}")
        print("=" * 60)
        
        nom = self._get_input(self.i18n.get('subjects.add.name'))
        code = self._get_input(self.i18n.get('subjects.add.code'))
        coefficient = self._get_input(self.i18n.get('subjects.add.coefficient'), "1.0")
        niveau = self._get_input(self.i18n.get('subjects.add.level'))
        
        # Vérifier que le code est unique
        if any(s.code == code for s in self.subjects):
            print(f"\n{self.i18n.get('subjects.add.code_exists', code=code)}")
            self._press_enter()
            return
        
        try:
            coef = float(coefficient)
        except ValueError:
            print(f"\n{self.i18n.get('subjects.add.coef_not_number')}")
            self._press_enter()
            return
        
        subject = Subject(nom, code, coef, niveau)
        is_valid, error_msg = subject.validate()
        
        if not is_valid:
            print(f"\n{self.i18n.get('subjects.add.validation_error', error=error_msg)}")
            self._press_enter()
            return
        
        self.subjects.append(subject)
        self._save_data()
        print(f"\n{self.i18n.get('subjects.add.success', subject=str(subject))}")
        self._press_enter()
    
    def modify_subject(self):
        """Modifie une matière existante"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('subjects.modify.title')}")
        print("=" * 60)
        
        code = self._get_input(self.i18n.get('subjects.modify.code_prompt'))
        subject = self._find_subject_by_code(code)
        
        if not subject:
            print(f"\n{self.i18n.get('subjects.modify.not_found', code=code)}")
            self._press_enter()
            return
        
        print(f"\n{self.i18n.get('subjects.modify.found', subject=str(subject))}")
        print(f"\n{self.i18n.get('subjects.modify.keep_current')}")
        
        nom = self._get_input(self.i18n.get('subjects.modify.new_name'), subject.nom)
        coefficient = self._get_input(self.i18n.get('subjects.modify.new_coefficient'), str(subject.coefficient))
        niveau = self._get_input(self.i18n.get('subjects.modify.new_level'), subject.niveau)
        
        try:
            coef = float(coefficient)
        except ValueError:
            print(f"\n{self.i18n.get('subjects.modify.coef_not_number')}")
            self._press_enter()
            return
        
        subject.nom = nom
        subject.coefficient = coef
        subject.niveau = niveau
        
        is_valid, error_msg = subject.validate()
        if not is_valid:
            print(f"\n{self.i18n.get('subjects.modify.validation_error', error=error_msg)}")
            self._press_enter()
            return
        
        self._save_data()
        print(f"\n{self.i18n.get('subjects.modify.success', subject=str(subject))}")
        self._press_enter()
    
    def delete_subject(self):
        """Supprime une matière"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('subjects.delete.title')}")
        print("=" * 60)
        
        code = self._get_input(self.i18n.get('subjects.delete.code_prompt'))
        subject = self._find_subject_by_code(code)
        
        if not subject:
            print(f"\n{self.i18n.get('subjects.delete.not_found', code=code)}")
            self._press_enter()
            return
        
        print(f"\n{self.i18n.get('subjects.delete.found', subject=str(subject))}")
        confirm = input(f"\n{self.i18n.get('subjects.delete.confirm')}").strip().lower()
        
        if confirm == 'o' or confirm == 'y':
            # Supprimer aussi toutes les notes de cette matière
            self.grades = [g for g in self.grades if g.code_matiere != code]
            self.subjects.remove(subject)
            self._save_data()
            print(f"\n{self.i18n.get('subjects.delete.success')}")
        else:
            print(f"\n{self.i18n.get('subjects.delete.cancelled')}")
        
        self._press_enter()
    
    def list_subjects(self):
        """Liste les matières"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('subjects.list.title')}")
        print("=" * 60)
        
        niveau = self._get_input(self.i18n.get('subjects.list.level_prompt'))
        
        if niveau:
            filtered = [s for s in self.subjects if s.niveau == niveau]
        else:
            filtered = self.subjects
        
        if filtered:
            print(f"\n{self.i18n.get('subjects.list.results', count=len(filtered))}\n")
            for i, subject in enumerate(filtered, 1):
                print(f"{i}. {subject}")
        else:
            print(f"\n{self.i18n.get('subjects.list.no_results')}")
        
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
            print(f"    {self.i18n.get('menu.grades.title')}")
            print("=" * 60)
            print(f"\n1. {self.i18n.get('menu.grades.option_1')}")
            print(f"2. {self.i18n.get('menu.grades.option_2')}")
            print(f"3. {self.i18n.get('menu.grades.option_3')}")
            print(f"4. {self.i18n.get('menu.grades.option_4')}")
            
            choice = input(f"\n{self.i18n.get('menu.main.choice')}").strip()
            
            if choice == '1':
                self.add_grade()
            elif choice == '2':
                self.modify_grade()
            elif choice == '3':
                self.delete_grade()
            elif choice == '4':
                break
            else:
                print(f"\n{self.i18n.get('menu.main.invalid')}")
                self._press_enter()
    
    def add_grade(self):
        """Ajoute une nouvelle note"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('grades.add.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('grades.add.matricule'))
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\n{self.i18n.get('grades.add.student_not_found', matricule=matricule)}")
            self._press_enter()
            return
        
        code_matiere = self._get_input(self.i18n.get('grades.add.code'))
        subject = self._find_subject_by_code(code_matiere)
        
        if not subject:
            print(f"\n{self.i18n.get('grades.add.subject_not_found', code=code_matiere)}")
            self._press_enter()
            return
        
        # Vérifier qu'il n'y a pas déjà une note pour cet étudiant dans cette matière
        existing = [g for g in self.grades 
                   if g.matricule_etudiant == matricule and g.code_matiere == code_matiere]
        if existing:
            print(f"\n{self.i18n.get('grades.add.already_exists')}")
            print(self.i18n.get('grades.add.existing_note', note=existing[0].note))
            self._press_enter()
            return
        
        note_str = self._get_input(self.i18n.get('grades.add.note'))
        
        try:
            note = float(note_str)
        except ValueError:
            print(f"\n{self.i18n.get('grades.add.not_number')}")
            self._press_enter()
            return
        
        grade = Grade(matricule, code_matiere, note)
        is_valid, error_msg = grade.validate()
        
        if not is_valid:
            print(f"\n{self.i18n.get('grades.add.validation_error', error=error_msg)}")
            self._press_enter()
            return
        
        self.grades.append(grade)
        self._save_data()
        print(f"\n{self.i18n.get('grades.add.success', grade=str(grade))}")
        self._press_enter()
    
    def modify_grade(self):
        """Modifie une note existante"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('grades.modify.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('grades.modify.matricule'))
        code_matiere = self._get_input(self.i18n.get('grades.modify.code'))
        
        grade = self._find_grade(matricule, code_matiere)
        
        if not grade:
            print(f"\n{self.i18n.get('grades.modify.not_found')}")
            self._press_enter()
            return
        
        print(self.i18n.get('grades.modify.found', note=grade.note))
        note_str = self._get_input(self.i18n.get('grades.modify.new_note'), str(grade.note))
        
        try:
            note = float(note_str)
        except ValueError:
            print(f"\n{self.i18n.get('grades.modify.not_number')}")
            self._press_enter()
            return
        
        grade.note = note
        is_valid, error_msg = grade.validate()
        
        if not is_valid:
            print(f"\n{self.i18n.get('grades.modify.validation_error', error=error_msg)}")
            self._press_enter()
            return
        
        self._save_data()
        print(f"\n{self.i18n.get('grades.modify.success', grade=str(grade))}")
        self._press_enter()
    
    def delete_grade(self):
        """Supprime une note"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('grades.delete.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('grades.delete.matricule'))
        code_matiere = self._get_input(self.i18n.get('grades.delete.code'))
        
        grade = self._find_grade(matricule, code_matiere)
        
        if not grade:
            print(f"\n{self.i18n.get('grades.delete.not_found')}")
            self._press_enter()
            return
        
        print(self.i18n.get('grades.delete.found', note=grade.note))
        confirm = input(f"\n{self.i18n.get('grades.delete.confirm')}").strip().lower()
        
        if confirm == 'o' or confirm == 'y':
            self.grades.remove(grade)
            self._save_data()
            print(f"\n{self.i18n.get('grades.delete.success')}")
        else:
            print(f"\n{self.i18n.get('grades.delete.cancelled')}")
        
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
            print(f"    {self.i18n.get('menu.consultation.title')}")
            print("=" * 60)
            print(f"\n1. {self.i18n.get('menu.consultation.option_1')}")
            print(f"2. {self.i18n.get('menu.consultation.option_2')}")
            print(f"3. {self.i18n.get('menu.consultation.option_3')}")
            print(f"4. {self.i18n.get('menu.consultation.option_4')}")
            
            choice = input(f"\n{self.i18n.get('menu.main.choice')}").strip()
            
            if choice == '1':
                self.show_student_grades()
            elif choice == '2':
                self.show_class_grades_for_subject()
            elif choice == '3':
                self.show_student_bulletin()
            elif choice == '4':
                break
            else:
                print(f"\n{self.i18n.get('menu.main.invalid')}")
                self._press_enter()
    
    def show_student_grades(self):
        """Affiche les notes d'un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('consultation.student_grades.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('consultation.student_grades.matricule'))
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\n{self.i18n.get('consultation.student_grades.not_found', matricule=matricule)}")
            self._press_enter()
            return
        
        student_grades = [g for g in self.grades if g.matricule_etudiant == matricule]
        
        print(f"\n{self.i18n.get('consultation.student_grades.student_info', student=str(student))}")
        print(f"\n{self.i18n.get('consultation.student_grades.count', count=len(student_grades))}\n")
        
        for grade in student_grades:
            subject = self._find_subject_by_code(grade.code_matiere)
            subject_name = subject.nom if subject else grade.code_matiere
            print(self.i18n.get('consultation.student_grades.format', subject=subject_name, note=grade.note, date=grade.date))
        
        if not student_grades:
            print(f"  {self.i18n.get('consultation.student_grades.no_grades')}")
        
        self._press_enter()
    
    def show_class_grades_for_subject(self):
        """Affiche les notes d'une classe pour une matière"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('consultation.class_grades.title')}")
        print("=" * 60)
        
        niveau = self._get_input(self.i18n.get('consultation.class_grades.level'))
        code_matiere = self._get_input(self.i18n.get('consultation.class_grades.code'))
        
        subject = self._find_subject_by_code(code_matiere)
        if not subject:
            print(f"\n{self.i18n.get('consultation.class_grades.subject_not_found', code=code_matiere)}")
            self._press_enter()
            return
        
        # Récupérer les étudiants de la classe
        class_students = [s for s in self.students if s.niveau == niveau]
        
        print(f"\n{self.i18n.get('consultation.class_grades.subject_info', subject=subject.nom)}")
        print(self.i18n.get('consultation.class_grades.class_info', level=niveau))
        print(f"\n{self.i18n.get('consultation.class_grades.count', count=len(class_students))}\n")
        
        for student in class_students:
            grade = self._find_grade(student.matricule, code_matiere)
            name = f"{student.prenom} {student.nom.upper()}"
            if grade:
                print(self.i18n.get('consultation.class_grades.format', name=name, matricule=student.matricule, note=grade.note))
            else:
                print(self.i18n.get('consultation.class_grades.format', name=name, matricule=student.matricule, note=self.i18n.get('consultation.class_grades.no_note')))
        
        self._press_enter()
    
    def show_student_bulletin(self):
        """Affiche le bulletin complet d'un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('consultation.bulletin.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('consultation.bulletin.matricule'))
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\n{self.i18n.get('consultation.bulletin.not_found', matricule=matricule)}")
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
        print(f"  {self.i18n.get('consultation.bulletin.header')}")
        print(f"{'='*60}")
        name = f"{student.prenom} {student.nom.upper()}"
        print(f"\n{self.i18n.get('consultation.bulletin.student', name=name)}")
        print(self.i18n.get('consultation.bulletin.matricule_label', matricule=student.matricule))
        print(self.i18n.get('consultation.bulletin.level_label', level=student.niveau))
        print(f"\n{'='*60}")
        subject_col = self.i18n.get('consultation.bulletin.columns.subject')
        note_col = self.i18n.get('consultation.bulletin.columns.note')
        coef_col = self.i18n.get('consultation.bulletin.columns.coef')
        points_col = self.i18n.get('consultation.bulletin.columns.points')
        print(f"{subject_col:<30} {note_col:<10} {coef_col:<10} {points_col:<10}")
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
            print(f"\n{self.i18n.get('consultation.bulletin.average', average=moyenne_calc)}")
            if rang:
                suffix = self.i18n.get('consultation.bulletin.rank_1') if rang == 1 else self.i18n.get('consultation.bulletin.rank_other')
                print(self.i18n.get('consultation.bulletin.rank', rank=rang, suffix=suffix))
        else:
            print(f"\n{self.i18n.get('consultation.bulletin.no_grades')}")
        
        print(f"{'='*60}")
        self._press_enter()
    
    # ========== STATISTIQUES ==========
    
    def handle_statistics_menu(self):
        """Gère le menu des statistiques"""
        while True:
            self._clear_screen()
            print("=" * 60)
            print(f"    {self.i18n.get('menu.statistics.title')}")
            print("=" * 60)
            print(f"\n1. {self.i18n.get('menu.statistics.option_1')}")
            print(f"2. {self.i18n.get('menu.statistics.option_2')}")
            print(f"3. {self.i18n.get('menu.statistics.option_3')}")
            print(f"4. {self.i18n.get('menu.statistics.option_4')}")
            print(f"5. {self.i18n.get('menu.statistics.option_5')}")
            
            choice = input(f"\n{self.i18n.get('menu.main.choice')}").strip()
            
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
                print(f"\n{self.i18n.get('menu.main.invalid')}")
                self._press_enter()
    
    def show_student_statistics(self):
        """Affiche les statistiques d'un étudiant"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('statistics.student.title')}")
        print("=" * 60)
        
        matricule = self._get_input(self.i18n.get('statistics.student.matricule'))
        student = self._find_student_by_matricule(matricule)
        
        if not student:
            print(f"\n{self.i18n.get('statistics.student.not_found', matricule=matricule)}")
            self._press_enter()
            return
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne = stats.calculate_student_average(matricule)
        rang = stats.calculate_student_rank(matricule)
        
        print(f"\n{self.i18n.get('statistics.student.student_info', student=str(student))}")
        if moyenne:
            print(f"\n{self.i18n.get('statistics.student.average', average=moyenne)}")
        else:
            print(f"\n{self.i18n.get('statistics.student.no_average')}")
        if rang:
            suffix = self.i18n.get('statistics.student.rank_1') if rang == 1 else self.i18n.get('statistics.student.rank_other')
            print(self.i18n.get('statistics.student.rank', rank=rang, suffix=suffix))
        else:
            print(f"\n{self.i18n.get('statistics.student.no_rank')}")
        
        self._press_enter()
    
    def show_class_statistics(self):
        """Affiche les statistiques d'une classe"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('statistics.class.title')}")
        print("=" * 60)
        
        niveau = self._get_input(self.i18n.get('statistics.class.level'))
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne_classe = stats.calculate_class_average(niveau)
        meilleur = stats.get_best_student_in_class(niveau)
        classement = stats.get_class_ranking(niveau)
        
        print(f"\n{self.i18n.get('statistics.class.class_info', level=niveau)}")
        if moyenne_classe:
            print(f"\n{self.i18n.get('statistics.class.average', average=moyenne_classe)}")
        else:
            print(f"\n{self.i18n.get('statistics.class.no_average')}")
        
        if meilleur:
            student, avg = meilleur
            name = f"{student.prenom} {student.nom.upper()}"
            print(f"\n{self.i18n.get('statistics.class.best_student', name=name, matricule=student.matricule)}")
            print(self.i18n.get('statistics.class.best_average', average=avg))
        
        if classement:
            print(f"\n{self.i18n.get('statistics.class.ranking_title', count=len(classement))}\n")
            rank_col = self.i18n.get('statistics.class.ranking_columns.rank')
            student_col = self.i18n.get('statistics.class.ranking_columns.student')
            avg_col = self.i18n.get('statistics.class.ranking_columns.average')
            print(f"{rank_col:<6} {student_col:<40} {avg_col:<10}")
            print("-" * 60)
            for student, avg, rank in classement:
                print(f"{rank:<6} {str(student):<40} {avg:<10.2f}")
        
        self._press_enter()
    
    def show_subject_statistics(self):
        """Affiche les statistiques d'une matière"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('statistics.subject.title')}")
        print("=" * 60)
        
        code_matiere = self._get_input(self.i18n.get('statistics.subject.code'))
        subject = self._find_subject_by_code(code_matiere)
        
        if not subject:
            print(f"\n{self.i18n.get('statistics.subject.subject_not_found', code=code_matiere)}")
            self._press_enter()
            return
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne = stats.calculate_subject_average(code_matiere)
        meilleur = stats.get_best_student_in_subject(code_matiere)
        
        print(f"\n{self.i18n.get('statistics.subject.subject_info', name=subject.nom, code=subject.code)}")
        if moyenne:
            print(f"\n{self.i18n.get('statistics.subject.average', average=moyenne)}")
        else:
            print(f"\n{self.i18n.get('statistics.subject.no_average')}")
        
        if meilleur:
            student, note = meilleur
            name = f"{student.prenom} {student.nom.upper()}"
            print(f"\n{self.i18n.get('statistics.subject.best_student', name=name, matricule=student.matricule)}")
            print(self.i18n.get('statistics.subject.best_note', note=note))
        
        self._press_enter()
    
    def show_global_statistics(self):
        """Affiche les statistiques globales"""
        self._clear_screen()
        print("=" * 60)
        print(f"    {self.i18n.get('statistics.global.title')}")
        print("=" * 60)
        
        stats = Statistics(self.students, self.subjects, self.grades)
        moyenne_globale = stats.calculate_global_average()
        meilleur = stats.get_best_student_global()
        
        if moyenne_globale:
            print(f"\n{self.i18n.get('statistics.global.average', average=moyenne_globale)}")
        else:
            print(f"\n{self.i18n.get('statistics.global.no_average')}")
        
        if meilleur:
            student, avg = meilleur
            name = f"{student.prenom} {student.nom.upper()}"
            print(f"\n{self.i18n.get('statistics.global.best_student_title')}")
            print(self.i18n.get('statistics.global.best_student', name=name, matricule=student.matricule))
            print(self.i18n.get('statistics.global.best_level', level=student.niveau))
            print(self.i18n.get('statistics.global.best_average', average=avg))
        
        print(f"\n{self.i18n.get('statistics.global.total_students', count=len(self.students))}")
        print(self.i18n.get('statistics.global.total_subjects', count=len(self.subjects)))
        print(self.i18n.get('statistics.global.total_grades', count=len(self.grades)))
        
        self._press_enter()

