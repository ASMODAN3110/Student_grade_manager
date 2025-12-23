# -*- coding: utf-8 -*-
"""
Frame Students - Gestion des étudiants
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.widgets.data_table import DataTable
from models.student import Student
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


class StudentsFrame(ctk.CTkScrollableFrame):
    """
    Frame pour la gestion des étudiants
    """
    
    def __init__(self, parent, main_window):
        """
        Initialise la frame des étudiants
        
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
            text="Gestion des Étudiants",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(side="left")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="➕ Ajouter un étudiant",
            font=ctk.CTkFont(size=14),
            fg_color="#1F6AA5",
            hover_color="#1a5a8a",
            command=self._show_add_dialog
        )
        add_btn.pack(side="right")
        
        # Tableau des étudiants
        columns = [("Matricule", 150), ("Nom", 200), ("Prénom", 200), ("Niveau", 150)]
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
            command=self._modify_student
        )
        modify_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Supprimer",
            font=ctk.CTkFont(size=14),
            fg_color="#F44336",
            hover_color="#d32f2f",
            command=self._delete_student
        )
        delete_btn.pack(side="left")
    
    def _load_table_data(self):
        """Charge les données dans le tableau"""
        data = []
        for student in self.main_window.students:
            data.append((
                student.matricule,
                student.nom,
                student.prenom,
                student.niveau
            ))
        self.table.set_data(data)
    
    def _show_add_dialog(self, student=None):
        """Affiche le dialogue d'ajout/modification"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter un étudiant" if not student else "Modifier un étudiant")
        dialog.geometry("550x550")  # Taille augmentée pour afficher tous les éléments
        dialog.transient(self)
        dialog.grab_set()
        
        # Container principal avec formulaire et boutons séparés
        main_container = ctk.CTkFrame(dialog, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Formulaire (zone scrollable si nécessaire)
        form_frame = ctk.CTkFrame(main_container)
        form_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Nom
        ctk.CTkLabel(form_frame, text="Nom:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        nom_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        nom_entry.pack(pady=(0, 15))
        if student:
            nom_entry.insert(0, student.nom)
        
        # Prénom
        ctk.CTkLabel(form_frame, text="Prénom:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        prenom_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        prenom_entry.pack(pady=(0, 15))
        if student:
            prenom_entry.insert(0, student.prenom)
        
        # Matricule
        ctk.CTkLabel(form_frame, text="Matricule:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        matricule_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        matricule_entry.pack(pady=(0, 15))
        if student:
            matricule_entry.insert(0, student.matricule)
            matricule_entry.configure(state="disabled")
        
        # Niveau
        ctk.CTkLabel(form_frame, text="Niveau/Classe:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        niveau_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        niveau_entry.pack(pady=(0, 25))
        if student:
            niveau_entry.insert(0, student.niveau)
        
        # Boutons (fixés en bas du container principal)
        buttons_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        buttons_frame.pack(side="bottom", fill="x", pady=(10, 0))
        
        def save():
            # #region agent log
            _debug_log("students_frame.py:save:entry", "save() called", {"is_modification": student is not None, "student_matricule": student.matricule if student else None}, "A")
            # #endregion
            
            nom = nom_entry.get().strip()
            prenom = prenom_entry.get().strip()
            niveau = niveau_entry.get().strip()
            
            # Si c'est une modification, utiliser le matricule de l'étudiant existant
            # Sinon, récupérer le matricule du champ
            if student:
                matricule = student.matricule  # Utiliser le matricule existant (non modifiable)
            else:
                matricule = matricule_entry.get().strip()
            
            # #region agent log
            _debug_log("students_frame.py:save:fields", "Fields extracted", {"nom": nom, "prenom": prenom, "matricule": matricule, "niveau": niveau}, "B")
            # #endregion
            
            if not all([nom, prenom, matricule, niveau]):
                # #region agent log
                _debug_log("students_frame.py:save:validation_failed", "Validation failed - empty fields", {"nom": nom, "prenom": prenom, "matricule": matricule, "niveau": niveau}, "B")
                # #endregion
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
                return
            
            # Vérifier l'unicité du matricule (seulement pour l'ajout)
            if not student:
                if any(s.matricule == matricule for s in self.main_window.students):
                    messagebox.showerror("Erreur", f"Le matricule {matricule} existe déjà")
                    return
                new_student = Student(nom, prenom, matricule, niveau)
                is_valid, error_msg = new_student.validate()
                if not is_valid:
                    # #region agent log
                    _debug_log("students_frame.py:save:validation_failed", "Student validation failed", {"error": error_msg}, "B")
                    # #endregion
                    messagebox.showerror("Erreur", error_msg)
                    return
                self.main_window.students.append(new_student)
            else:
                # Modification : mettre à jour les champs modifiables
                # #region agent log
                _debug_log("students_frame.py:save:before_modify", "Before modification", {"old_nom": student.nom, "old_prenom": student.prenom, "old_niveau": student.niveau}, "D")
                # #endregion
                
                student.nom = nom
                student.prenom = prenom
                student.niveau = niveau
                
                # #region agent log
                _debug_log("students_frame.py:save:after_modify", "After modification", {"new_nom": student.nom, "new_prenom": student.prenom, "new_niveau": student.niveau}, "D")
                # #endregion
                
                is_valid, error_msg = student.validate()
                if not is_valid:
                    # #region agent log
                    _debug_log("students_frame.py:save:validation_failed", "Student validation failed after modify", {"error": error_msg}, "B")
                    # #endregion
                    messagebox.showerror("Erreur", error_msg)
                    return
            
            # #region agent log
            _debug_log("students_frame.py:save:before_refresh", "Before refresh_data()", {"students_count": len(self.main_window.students)}, "C")
            # #endregion
            
            self.main_window.refresh_data()
            
            # #region agent log
            _debug_log("students_frame.py:save:after_refresh", "After refresh_data()", {"students_count": len(self.main_window.students)}, "C")
            # #endregion
            
            self._load_table_data()
            dialog.destroy()
            
            # #region agent log
            _debug_log("students_frame.py:save:exit", "save() completed successfully", {}, "A")
            # #endregion
        
        # Fonction de suppression depuis le dialogue
        def delete_from_dialog():
            if student and messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {student.prenom} {student.nom} ?"):
                # Supprimer aussi toutes ses notes
                self.main_window.grades = [g for g in self.main_window.grades if g.matricule_etudiant != student.matricule]
                self.main_window.students.remove(student)
                self.main_window.refresh_data()
                self._load_table_data()
                dialog.destroy()
        
        # Bouton Valider/Enregistrer (bouton principal, plus visible)
        btn_text = "✓ Valider" if student else "✓ Enregistrer"
        btn_color = "#4CAF50" if student else "#1F6AA5"  # Vert pour validation, bleu pour ajout
        save_btn = ctk.CTkButton(
            buttons_frame,
            text=btn_text,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=btn_color,
            hover_color="#45a049" if student else "#1a5a8a",
            width=150,
            height=40,
            command=lambda: (_debug_log("students_frame.py:button:click", "Save button clicked", {"btn_text": btn_text}, "A"), save())
        )
        save_btn.pack(side="right", padx=(10, 0))
        
        # Bouton Supprimer (seulement en mode modification)
        if student:
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="🗑️ Supprimer",
                font=ctk.CTkFont(size=14),
                fg_color="#F44336",
                hover_color="#d32f2f",
                command=delete_from_dialog
            )
            delete_btn.pack(side="right", padx=(0, 10))
        
        # Bouton Annuler
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            font=ctk.CTkFont(size=14),
            fg_color="#808080",
            hover_color="#606060",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right")
    
    def _modify_student(self):
        """Modifie un étudiant sélectionné"""
        selected = self.table.get_selected_item()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un étudiant")
            return
        
        matricule = selected[0]
        student = next((s for s in self.main_window.students if s.matricule == matricule), None)
        if student:
            self._show_add_dialog(student)
    
    def _delete_student(self):
        """Supprime un étudiant sélectionné"""
        selected = self.table.get_selected_item()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner un étudiant")
            return
        
        matricule = selected[0]
        student = next((s for s in self.main_window.students if s.matricule == matricule), None)
        
        if student:
            if messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {student.prenom} {student.nom} ?"):
                # Supprimer aussi toutes ses notes
                self.main_window.grades = [g for g in self.main_window.grades if g.matricule_etudiant != matricule]
                self.main_window.students.remove(student)
                self.main_window.refresh_data()
                self._load_table_data()
    
    def refresh(self):
        """Rafraîchit la frame"""
        self._load_table_data()
    
    def show_add_dialog(self):
        """Affiche le dialogue d'ajout (pour le bouton New Entry)"""
        self._show_add_dialog()

