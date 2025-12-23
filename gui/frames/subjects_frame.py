# -*- coding: utf-8 -*-
"""
Frame Subjects - Gestion des matières
"""

import customtkinter as ctk
from tkinter import messagebox
from gui.widgets.data_table import DataTable
from models.subject import Subject


class SubjectsFrame(ctk.CTkScrollableFrame):
    """
    Frame pour la gestion des matières
    """
    
    def __init__(self, parent, main_window):
        """
        Initialise la frame des matières
        
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
            text="Gestion des Matières",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title_label.pack(side="left")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="➕ Ajouter une matière",
            font=ctk.CTkFont(size=14),
            fg_color="#FF9800",
            hover_color="#f57c00",
            command=self._show_add_dialog
        )
        add_btn.pack(side="right")
        
        # Tableau des matières
        columns = [("Code", 150), ("Nom", 300), ("Coefficient", 150), ("Niveau", 150)]
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
            command=self._modify_subject
        )
        modify_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="🗑️ Supprimer",
            font=ctk.CTkFont(size=14),
            fg_color="#F44336",
            hover_color="#d32f2f",
            command=self._delete_subject
        )
        delete_btn.pack(side="left")
    
    def _load_table_data(self):
        """Charge les données dans le tableau"""
        data = []
        for subject in self.main_window.subjects:
            data.append((
                subject.code,
                subject.nom,
                str(subject.coefficient),
                subject.niveau
            ))
        self.table.set_data(data)
    
    def _show_add_dialog(self, subject=None):
        """Affiche le dialogue d'ajout/modification"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Ajouter une matière" if not subject else "Modifier une matière")
        dialog.geometry("500x450")
        dialog.transient(self)
        dialog.grab_set()
        
        # Formulaire
        form_frame = ctk.CTkFrame(dialog)
        form_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Nom
        ctk.CTkLabel(form_frame, text="Nom:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        nom_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        nom_entry.pack(pady=(0, 15))
        if subject:
            nom_entry.insert(0, subject.nom)
        
        # Code
        ctk.CTkLabel(form_frame, text="Code:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        code_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        code_entry.pack(pady=(0, 15))
        if subject:
            code_entry.insert(0, subject.code)
            code_entry.configure(state="disabled")
        
        # Coefficient
        ctk.CTkLabel(form_frame, text="Coefficient:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        coefficient_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        coefficient_entry.pack(pady=(0, 15))
        if subject:
            coefficient_entry.insert(0, str(subject.coefficient))
        
        # Niveau
        ctk.CTkLabel(form_frame, text="Niveau/Classe:", font=ctk.CTkFont(size=14)).pack(anchor="w", pady=(0, 5))
        niveau_entry = ctk.CTkEntry(form_frame, width=400, height=40)
        niveau_entry.pack(pady=(0, 25))
        if subject:
            niveau_entry.insert(0, subject.niveau)
        
        # Boutons
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        def save():
            nom = nom_entry.get().strip()
            code = code_entry.get().strip()
            try:
                coefficient = float(coefficient_entry.get().strip())
            except ValueError:
                messagebox.showerror("Erreur", "Le coefficient doit être un nombre")
                return
            niveau = niveau_entry.get().strip()
            
            if not all([nom, code, niveau]):
                messagebox.showerror("Erreur", "Tous les champs sont obligatoires")
                return
            
            # Vérifier l'unicité du code
            if not subject:
                if any(s.code == code for s in self.main_window.subjects):
                    messagebox.showerror("Erreur", f"Le code {code} existe déjà")
                    return
                new_subject = Subject(nom, code, coefficient, niveau)
                is_valid, error_msg = new_subject.validate()
                if not is_valid:
                    messagebox.showerror("Erreur", error_msg)
                    return
                self.main_window.subjects.append(new_subject)
            else:
                subject.nom = nom
                subject.coefficient = coefficient
                subject.niveau = niveau
                is_valid, error_msg = subject.validate()
                if not is_valid:
                    messagebox.showerror("Erreur", error_msg)
                    return
            
            self.main_window.refresh_data()
            self._load_table_data()
            dialog.destroy()
        
        save_btn = ctk.CTkButton(
            buttons_frame,
            text="Enregistrer",
            font=ctk.CTkFont(size=14),
            fg_color="#FF9800",
            command=save
        )
        save_btn.pack(side="right", padx=(10, 0))
        
        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Annuler",
            font=ctk.CTkFont(size=14),
            fg_color="#808080",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right")
    
    def _modify_subject(self):
        """Modifie une matière sélectionnée"""
        selected = self.table.get_selected_item()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une matière")
            return
        
        code = selected[0]
        subject = next((s for s in self.main_window.subjects if s.code == code), None)
        if subject:
            self._show_add_dialog(subject)
    
    def _delete_subject(self):
        """Supprime une matière sélectionnée"""
        selected = self.table.get_selected_item()
        if not selected:
            messagebox.showwarning("Attention", "Veuillez sélectionner une matière")
            return
        
        code = selected[0]
        subject = next((s for s in self.main_window.subjects if s.code == code), None)
        
        if subject:
            if messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer {subject.nom} ?"):
                # Supprimer aussi toutes ses notes
                self.main_window.grades = [g for g in self.main_window.grades if g.code_matiere != code]
                self.main_window.subjects.remove(subject)
                self.main_window.refresh_data()
                self._load_table_data()
    
    def refresh(self):
        """Rafraîchit la frame"""
        self._load_table_data()
    
    def show_add_dialog(self):
        """Affiche le dialogue d'ajout"""
        self._show_add_dialog()

