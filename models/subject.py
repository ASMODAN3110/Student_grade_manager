# -*- coding: utf-8 -*-
"""
Module contenant la classe Subject pour représenter une matière
"""


class Subject:
    """
    Classe représentant une matière dans le système de gestion des notes
    
    Attributs:
        nom (str): Nom de la matière
        code (str): Code unique de la matière
        coefficient (float): Coefficient de la matière pour le calcul de la moyenne
        niveau (str): Niveau/classe concerné par cette matière
    """
    
    def __init__(self, nom, code, coefficient, niveau):
        """
        Constructeur de la classe Subject
        
        Args:
            nom (str): Nom de la matière
            code (str): Code unique
            coefficient (float): Coefficient (doit être > 0)
            niveau (str): Niveau/classe concerné
        """
        self.nom = nom.strip()
        self.code = code.strip()
        self.coefficient = float(coefficient)
        self.niveau = niveau.strip()
    
    def __str__(self):
        """
        Représentation en chaîne de caractères de la matière
        
        Returns:
            str: Format "Nom (Code) - Coef: X - Niveau"
        """
        return f"{self.nom} ({self.code}) - Coef: {self.coefficient} - {self.niveau}"
    
    def __repr__(self):
        """
        Représentation technique de la matière
        
        Returns:
            str: Représentation pour le débogage
        """
        return f"Subject(nom='{self.nom}', code='{self.code}', coefficient={self.coefficient}, niveau='{self.niveau}')"
    
    def to_dict(self):
        """
        Convertit l'objet Subject en dictionnaire pour la sauvegarde JSON
        
        Returns:
            dict: Dictionnaire contenant les attributs de la matière
        """
        return {
            'nom': self.nom,
            'code': self.code,
            'coefficient': self.coefficient,
            'niveau': self.niveau
        }
    
    @staticmethod
    def from_dict(data):
        """
        Crée un objet Subject à partir d'un dictionnaire
        
        Args:
            data (dict): Dictionnaire contenant les données de la matière
            
        Returns:
            Subject: Instance de Subject créée
        """
        return Subject(
            nom=data.get('nom', ''),
            code=data.get('code', ''),
            coefficient=data.get('coefficient', 1.0),
            niveau=data.get('niveau', '')
        )
    
    def validate(self):
        """
        Valide que tous les champs requis sont remplis et corrects
        
        Returns:
            tuple: (bool, str) - (True si valide, message d'erreur sinon)
        """
        if not self.nom:
            return False, "Le nom de la matière est obligatoire"
        if not self.code:
            return False, "Le code de la matière est obligatoire"
        if not self.niveau:
            return False, "Le niveau est obligatoire"
        if self.coefficient <= 0:
            return False, "Le coefficient doit être supérieur à 0"
        return True, ""

