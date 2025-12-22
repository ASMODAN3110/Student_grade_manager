# -*- coding: utf-8 -*-
"""
Module contenant la classe Student pour représenter un étudiant
"""


class Student:
    """
    Classe représentant un étudiant dans le système de gestion des notes
    
    Attributs:
        nom (str): Nom de famille de l'étudiant
        prenom (str): Prénom de l'étudiant
        matricule (str): Matricule unique de l'étudiant
        niveau (str): Niveau/classe de l'étudiant (ex: L1, L2, L3)
    """
    
    def __init__(self, nom, prenom, matricule, niveau):
        """
        Constructeur de la classe Student
        
        Args:
            nom (str): Nom de famille
            prenom (str): Prénom
            matricule (str): Matricule unique
            niveau (str): Niveau/classe
        """
        self.nom = nom.strip()
        self.prenom = prenom.strip()
        self.matricule = matricule.strip()
        self.niveau = niveau.strip()
    
    def __str__(self):
        """
        Représentation en chaîne de caractères de l'étudiant
        
        Returns:
            str: Format "Prénom NOM (Matricule) - Niveau"
        """
        return f"{self.prenom} {self.nom.upper()} ({self.matricule}) - {self.niveau}"
    
    def __repr__(self):
        """
        Représentation technique de l'étudiant
        
        Returns:
            str: Représentation pour le débogage
        """
        return f"Student(nom='{self.nom}', prenom='{self.prenom}', matricule='{self.matricule}', niveau='{self.niveau}')"
    
    def to_dict(self):
        """
        Convertit l'objet Student en dictionnaire pour la sauvegarde JSON
        
        Returns:
            dict: Dictionnaire contenant les attributs de l'étudiant
        """
        return {
            'nom': self.nom,
            'prenom': self.prenom,
            'matricule': self.matricule,
            'niveau': self.niveau
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crée un objet Student à partir d'un dictionnaire
        
        Args:
            data (dict): Dictionnaire contenant les données de l'étudiant
            
        Returns:
            Student: Instance de Student créée
        """
        return Student(
            nom=data.get('nom', ''),
            prenom=data.get('prenom', ''),
            matricule=data.get('matricule', ''),
            niveau=data.get('niveau', '')
        )
    
    def validate(self):
        """
        Valide que tous les champs requis sont remplis
        
        Returns:
            tuple: (bool, str) - (True si valide, message d'erreur sinon)
        """
        if not self.nom:
            return False, "Le nom est obligatoire"
        if not self.prenom:
            return False, "Le prénom est obligatoire"
        if not self.matricule:
            return False, "Le matricule est obligatoire"
        if not self.niveau:
            return False, "Le niveau est obligatoire"
        return True, ""

