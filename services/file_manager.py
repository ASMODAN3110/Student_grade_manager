# -*- coding: utf-8 -*-
"""
Module de gestion des fichiers JSON pour le stockage des données
Gère la lecture, l'écriture et la sauvegarde des étudiants, matières et notes
"""

import json
import os
from typing import List, Dict, Any


class FileManager:
    """
    Classe pour gérer toutes les opérations de fichiers JSON
    Assure la persistance des données et la gestion des erreurs
    """
    
    def __init__(self, data_dir='data'):
        """
        Initialise le gestionnaire de fichiers
        
        Args:
            data_dir (str): Répertoire où sont stockés les fichiers JSON
        """
        self.data_dir = data_dir
        # S'assurer que le répertoire existe
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _read_json(self, filename: str) -> List[Dict[str, Any]]:
        """
        Lit un fichier JSON et retourne son contenu sous forme de liste
        
        Args:
            filename (str): Nom du fichier à lire
            
        Returns:
            List[Dict]: Liste des dictionnaires contenus dans le fichier
                       Retourne une liste vide si le fichier n'existe pas ou est vide
        """
        filepath = os.path.join(self.data_dir, filename)
        
        # Si le fichier n'existe pas, retourner une liste vide
        if not os.path.exists(filepath):
            return []
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # S'assurer que c'est une liste
                if isinstance(data, list):
                    return data
                else:
                    return []
        except json.JSONDecodeError:
            # Si le fichier est corrompu, retourner une liste vide
            print(f"Attention: Le fichier {filename} est corrompu. Il sera réinitialisé.")
            return []
        except Exception as e:
            print(f"Erreur lors de la lecture de {filename}: {e}")
            return []
    
    def _write_json(self, filename: str, data: List[Dict[str, Any]]) -> bool:
        """
        Écrit des données dans un fichier JSON de manière sécurisée
        
        Args:
            filename (str): Nom du fichier à écrire
            data (List[Dict]): Données à sauvegarder
            
        Returns:
            bool: True si l'écriture a réussi, False sinon
        """
        filepath = os.path.join(self.data_dir, filename)
        
        try:
            # Écrire dans un fichier temporaire d'abord (sauvegarde atomique)
            temp_filepath = filepath + '.tmp'
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            # Remplacer l'ancien fichier par le nouveau (opération atomique)
            if os.path.exists(filepath):
                os.replace(temp_filepath, filepath)
            else:
                os.rename(temp_filepath, filepath)
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'écriture de {filename}: {e}")
            # Nettoyer le fichier temporaire en cas d'erreur
            if os.path.exists(filepath + '.tmp'):
                try:
                    os.remove(filepath + '.tmp')
                except:
                    pass
            return False
    
    # ========== GESTION DES ÉTUDIANTS ==========
    
    def load_students(self) -> List[Dict[str, Any]]:
        """
        Charge la liste des étudiants depuis le fichier JSON
        
        Returns:
            List[Dict]: Liste des étudiants
        """
        return self._read_json('students.json')
    
    def save_students(self, students: List[Dict[str, Any]]) -> bool:
        """
        Sauvegarde la liste des étudiants dans le fichier JSON
        
        Args:
            students (List[Dict]): Liste des étudiants à sauvegarder
            
        Returns:
            bool: True si la sauvegarde a réussi
        """
        return self._write_json('students.json', students)
    
    # ========== GESTION DES MATIÈRES ==========
    
    def load_subjects(self) -> List[Dict[str, Any]]:
        """
        Charge la liste des matières depuis le fichier JSON
        
        Returns:
            List[Dict]: Liste des matières
        """
        return self._read_json('subjects.json')
    
    def save_subjects(self, subjects: List[Dict[str, Any]]) -> bool:
        """
        Sauvegarde la liste des matières dans le fichier JSON
        
        Args:
            subjects (List[Dict]): Liste des matières à sauvegarder
            
        Returns:
            bool: True si la sauvegarde a réussi
        """
        return self._write_json('subjects.json', subjects)
    
    # ========== GESTION DES NOTES ==========
    
    def load_grades(self) -> List[Dict[str, Any]]:
        """
        Charge la liste des notes depuis le fichier JSON
        
        Returns:
            List[Dict]: Liste des notes
        """
        return self._read_json('grades.json')
    
    def save_grades(self, grades: List[Dict[str, Any]]) -> bool:
        """
        Sauvegarde la liste des notes dans le fichier JSON
        
        Args:
            grades (List[Dict]): Liste des notes à sauvegarder
            
        Returns:
            bool: True si la sauvegarde a réussi
        """
        return self._write_json('grades.json', grades)
    
    # ========== GESTION DE LA CONFIGURATION ==========
    
    def load_config(self) -> Dict[str, Any]:
        """
        Charge la configuration depuis le fichier JSON
        
        Returns:
            Dict: Dictionnaire de configuration
        """
        filepath = os.path.join(self.data_dir, 'config.json')
        
        if not os.path.exists(filepath):
            # Retourner la configuration par défaut avec la langue
            return {'password': 'password', 'language': 'fr'}
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # S'assurer que la langue est définie (par défaut 'fr')
                if 'language' not in config:
                    config['language'] = 'fr'
                return config
        except Exception as e:
            print(f"Erreur lors de la lecture de config.json: {e}")
            return {'password': 'password', 'language': 'fr'}
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """
        Sauvegarde la configuration dans le fichier JSON
        
        Args:
            config (Dict): Dictionnaire de configuration à sauvegarder
            
        Returns:
            bool: True si la sauvegarde a réussi
        """
        filepath = os.path.join(self.data_dir, 'config.json')
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erreur lors de l'écriture de config.json: {e}")
            return False
    
    def save_language(self, language: str) -> bool:
        """
        Sauvegarde la langue dans le fichier de configuration
        
        Args:
            language (str): Code de la langue ('fr' ou 'en')
            
        Returns:
            bool: True si la sauvegarde a réussi
        """
        config = self.load_config()
        config['language'] = language
        return self.save_config(config)

