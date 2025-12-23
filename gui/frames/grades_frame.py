# -*- coding: utf-8 -*-
"""
Frame Grades - Saisie des notes
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.widgets.data_table import DataTable
from models.grade import Grade
from datetime import datetime


class GradesFrame(ctk.CTkScrollableFrame):
    """
    Frame pour la saisie des notes
    """
    
    def __init__(self, parent, main_window):
        """
        Initialise la frame des notes
        
        Args:
            parent: Widget parent
            main_window: Fenêtre principale
        """
        super().__init__(parent, fg_color="transparent")
        
        self.main_window = main_window
        
        self._create_widgets()
        self._load_table_data()
    
    def _create_widgets(self):
        """Crée les widgets de la frame"""
        # Header avec titre et bouton
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="Saisie des Notes",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(side="left")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="➕ Enregistrer une note",
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            hover_color="#45a049",
            command=lambda: self.note_entry.focus()
        )
        add_btn.pack(side="right")
        
        # Formulaire de saisie
        form_frame = ctk.CTkFrame(self, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        form_frame.pack(fill="x", pady=(0, 20))
        
        form_inner = ctk.CTkFrame(form_frame, fg_color="transparent")
        form_inner.pack(fill="x", padx=20, pady=20)
        
        # Étudiant
        ctk.CTkLabel(form_inner, text="Étudiant:", font=ctk.CTkFont(size=14)).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=10)
        self.student_combo = ctk.CTkComboBox(
            form_inner,
            values=[f"{s.matricule} - {s.prenom} {s.nom}" for s in self.main_window.students],
            width=300
        )
        self.student_combo.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Matière
        ctk.CTkLabel(form_inner, text="Matière:", font=ctk.CTkFont(size=14)).grid(row=0, column=2, sticky="w", padx=(20, 10), pady=10)
        self.subject_combo = ctk.CTkComboBox(
            form_inner,
            values=[f"{s.code} - {s.nom}" for s in self.main_window.subjects],
            width=300
        )
        self.subject_combo.grid(row=0, column=3, padx=10, pady=10, sticky="ew")
        
        form_inner.grid_columnconfigure((1, 3), weight=1)
        
        # Note
        note_frame = ctk.CTkFrame(form_inner, fg_color="transparent")
        note_frame.grid(row=1, column=0, columnspan=4, sticky="ew", pady=10)
        
        ctk.CTkLabel(note_frame, text="Note (0-20):", font=ctk.CTkFont(size=14)).pack(side="left", padx=(0, 10))
        self.note_entry = ctk.CTkEntry(note_frame, width=150, height=40)
        self.note_entry.pack(side="left", padx=(0, 20))
        
        save_btn = ctk.CTkButton(
            note_frame,
            text="Enregistrer",
            font=ctk.CTkFont(size=14),
            fg_color="#4CAF50",
            command=self._save_grade
        )
        save_btn.pack(side="left")
        
        # Tableau des notes
        columns = [("Étudiant", 200), ("Matière", 200), ("Note", 100), ("Date", 150)]
        self.table = DataTable(self, columns=columns)
        self.table.pack(fill="both", expand=True, pady=(0, 20))
        
        # Boutons d'action
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x")
        
        modify_btn = ctk.CTkButton(
            actions_frame,
            text="✏️ Modifier",
            font=ctk.CTkFont(size=14),
            fg_color="#FF9800",
            hover_color="#f57c00",
            command=self._modify_grade
        )
        modify_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Supprimer",
            font=ctk.CTkFont(size=14),
            fg_color="#F44336",
            hover_color="#d32f2f",
            command=self._delete_grade
        )
        delete_btn.pack(side="left")
    
    def _load_table_data(self):
        """Charge les données dans le tableau"""
        data = []
        for grade in self.main_window.grades:
            # Trouver l'étudiant
            student = next((s for s in self.main_window.students if s.matricule == grade.matricule_etudiant), None)
            student_name = f"{student.prenom} {student.nom}" if student else grade.matricule_etudiant
            
            # Trouver la matière
            subject = next((s for s in self.main_window.subjects if s.code == grade.code_matiere), None)
            subject_name = subject.nom if subject else grade.code_matiere
            
            data.append((
                student_name,
                subject_name,
                f"{grade.note:.2f}/20",
                grade.date
            ))
        self.table.set_data(data)
    
    def _save_grade(self):
        """Enregistre une note"""
        student_str = self.student_combo.get()
        subject_str = self.subject_combo.get()
        note_str = self.note_entry.get().strip()
        
        if not all([student_str, subject_str, note_str]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs")
            return
        
        # Extraire le matricule et le code
        matricule = student_str.split(" - ")[0]
        code_matiere = subject_str.split(" - ")[0]
        
        try:
            note = float(note_str)
            if note < 0 or note > 20:
                messagebox.showerror("Erreur", "La note doit être comprise entre 0 et 20")
                return
        except ValueError:
            messagebox.showerror("Erreur", "La note doit être un nombre")
            return
        
        # Vérifier qu'il n'y a pas déjà une note
        existing = next((g for g in self.main_window.grades 
                        if g.matricule_etudiant == matricule and g.code_matiere == code_matiere), None)
        
        if existing:
            if messagebox.askyesno("Note existante", "Une note existe déjà. Voulez-vous la modifier ?"):
                existing.note = note
            else:
                return
        else:
            new_grade = Grade(matricule, code_matiere, note)
            is_valid, error_msg = new_grade.validate()
            if not is_valid:
                messagebox.showerror("Erreur", error_msg)
                return
            self.main_window.grades.append(new_grade)
        
        self.main_window.refresh_data()
        self._load_table_data()
        self.note_entry.delete(0, "end")
    
    def _modify_grade(self):
        """Modifie une note sélectionnée"""
        selected = self.table.get_selected_item()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une note")
            return
        
        # Trouver la note
        student_name = selected[0]
        subject_name = selected[1]
        
        student = next((s for s in self.main_window.students 
                       if f"{s.prenom} {s.nom}" == student_name), None)
        subject = next((s for s in self.main_window.subjects if s.nom == subject_name), None)
        
        if student and subject:
            grade = next((g for g in self.main_window.grades 
                         if g.matricule_etudiant == student.matricule and g.code_matiere == subject.code), None)
            if grade:
                # Afficher le dialogue de modification
                dialog = ctk.CTkToplevel(self)
                dialog.title("Modifier une note")
                dialog.geometry("400x200")
                dialog.transient(self)
                dialog.grab_set()
                
                form_frame = ctk.CTkFrame(dialog)
                form_frame.pack(fill="both", expand=True, padx=30, pady=30)
                
                ctk.CTkLabel(form_frame, text="Nouvelle note (0-20):", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 10))
                note_entry = ctk.CTkEntry(form_frame, width=300, height=40)
                note_entry.insert(0, str(grade.note))
                note_entry.pack(pady=(0, 20))
                
                def save():
                    try:
                        new_note = float(note_entry.get().strip())
                        if new_note < 0 or new_note > 20:
                            messagebox.showerror("Erreur", "La note doit être comprise entre 0 et 20")
                            return
                        grade.note = new_note
                        self.main_window.refresh_data()
                        self._load_table_data()
                        dialog.destroy()
                    except ValueError:
                        messagebox.showerror("Erreur", "La note doit être un nombre")
                
                buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
                buttons_frame.pack(fill="x")
                
                ctk.CTkButton(buttons_frame, text="Enregistrer", fg_color="#4CAF50", command=save).pack(side="right", padx=(10, 0))
                ctk.CTkButton(buttons_frame, text="Annuler", fg_color="#808080", command=dialog.destroy).pack(side="right")
    
    def _delete_grade(self):
        """Supprime une note sélectionnée"""
        selected = self.table.get_selected_item()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une note")
            return
        
        student_name = selected[0]
        subject_name = selected[1]
        
        student = next((s for s in self.main_window.students 
                       if f"{s.prenom} {s.nom}" == student_name), None)
        subject = next((s for s in self.main_window.subjects if s.nom == subject_name), None)
        
        if student and subject:
            grade = next((g for g in self.main_window.grades 
                         if g.matricule_etudiant == student.matricule and g.code_matiere == subject.code), None)
            if grade:
                if messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer cette note ?"):
                    self.main_window.grades.remove(grade)
                    self.main_window.refresh_data()
                    self._load_table_data()
    
    def refresh(self):
        """Rafraîchit la frame"""
        # Mettre à jour les combobox
        self.student_combo.configure(values=[f"{s.matricule} - {s.prenom} {s.nom}" for s in self.main_window.students])
        self.subject_combo.configure(values=[f"{s.code} - {s.nom}" for s in self.main_window.subjects])
        self._load_table_data()
    
    def show_add_dialog(self):
        """Affiche le dialogue d'ajout"""
        # Le formulaire est déjà visible dans la frame
        pass

