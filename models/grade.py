# -*- coding: utf-8 -*-
"""
Module contenant la classe Grade pour représenter une note
"""

from datetime import datetime


class Grade:
    """
    Classe représentant une note dans le système de gestion des notes
    
    Attributs:
        matricule_etudiant (str): Matricule de l'étudiant
        code_matiere (str): Code de la matière
        note (float): Note obtenue (entre 0 et 20)
        date (str): Date de saisie de la note (format YYYY-MM-DD)
    """
    
    def __init__(self, matricule_etudiant, code_matiere, note, date=None):
        """
        Constructeur de la classe Grade
        
        Args:
            matricule_etudiant (str): Matricule de l'étudiant
            code_matiere (str): Code de la matière
            note (float): Note obtenue (doit être entre 0 et 20)
            date (str, optional): Date de saisie. Si None, utilise la date actuelle
        """
        self.matricule_etudiant = matricule_etudiant.strip()
        self.code_matiere = code_matiere.strip()
        self.note = float(note)
        
        # Si aucune date n'est fournie, utiliser la date actuelle
        if date is None:
            self.date = datetime.now().strftime('%Y-%m-%d')
        else:
            self.date = date
    
    def __str__(self):
        """
        Représentation en chaîne de caractères de la note
        
        Returns:
            str: Format "Note: X/20 - Matricule: XXX - Matière: XXX"
        """
        return f"Note: {self.note}/20 - Matricule: {self.matricule_etudiant} - Matière: {self.code_matiere}"
    
    def __repr__(self):
        """
        Représentation technique de la note
        
        Returns:
            str: Représentation pour le débogage
        """
        return f"Grade(matricule='{self.matricule_etudiant}', code_matiere='{self.code_matiere}', note={self.note}, date='{self.date}')"
    
    def to_dict(self):
        """
        Convertit l'objet Grade en dictionnaire pour la sauvegarde JSON
        
        Returns:
            dict: Dictionnaire contenant les attributs de la note
        """
        return {
            'matricule_etudiant': self.matricule_etudiant,
            'code_matiere': self.code_matiere,
            'note': self.note,
            'date': self.date
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crée un objet Grade à partir d'un dictionnaire
        
        Args:
            data (dict): Dictionnaire contenant les données de la note
            
        Returns:
            Grade: Instance de Grade créée
        """
        return Grade(
            matricule_etudiant=data.get('matricule_etudiant', ''),
            code_matiere=data.get('code_matiere', ''),
            note=data.get('note', 0.0),
            date=data.get('date', None)
        )
    
    def validate(self):
        """
        Valide que la note est dans la plage autorisée (0-20)
        
        Returns:
            tuple: (bool, str) - (True si valide, message d'erreur sinon)
        """
        if not self.matricule_etudiant:
            return False, "Le matricule de l'étudiant est obligatoire"
        if not self.code_matiere:
            return False, "Le code de la matière est obligatoire"
        if self.note < 0 or self.note > 20:
            return False, "La note doit être comprise entre 0 et 20"
        return True, ""

