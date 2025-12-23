# -*- coding: utf-8 -*-
"""
Module de gestion des traductions (i18n)
Gère le chargement et l'accès aux traductions multilingues
"""

import json
import os
from typing import Dict, Any, Optional


class TranslationManager:
    """
    Gestionnaire de traductions avec pattern singleton
    Charge les traductions depuis des fichiers JSON et fournit un accès centralisé
    """
    
    _instance = None
    _translations: Dict[str, Dict[str, Any]] = {}
    _current_language: str = "fr"
    _locales_dir: str = "locales"
    
    def __new__(cls):
        """Implémentation du pattern singleton"""
        if cls._instance is None:
            cls._instance = super(TranslationManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialise le gestionnaire de traductions"""
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # Charger les traductions si le répertoire existe
            if os.path.exists(self._locales_dir):
                self._load_translations()
    
    def _load_translations(self):
        """
        Charge tous les fichiers de traduction depuis le répertoire locales/
        """
        for lang in ["fr", "en"]:
            filepath = os.path.join(self._locales_dir, f"{lang}.json")
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        self._translations[lang] = json.load(f)
                except Exception as e:
                    print(f"Erreur lors du chargement de {filepath}: {e}")
                    self._translations[lang] = {}
            else:
                self._translations[lang] = {}
    
    def set_language(self, lang: str):
        """
        Change la langue actuelle
        
        Args:
            lang (str): Code de la langue ("fr" ou "en")
        """
        if lang in self._translations:
            self._current_language = lang
        else:
            print(f"Langue '{lang}' non disponible. Utilisation de 'fr' par défaut.")
            self._current_language = "fr"
    
    def get_current_language(self) -> str:
        """
        Retourne la langue actuelle
        
        Returns:
            str: Code de la langue actuelle
        """
        return self._current_language
    
    def get(self, key: str, default: Optional[str] = None, **kwargs) -> str:
        """
        Récupère une traduction par sa clé
        
        Args:
            key (str): Clé de traduction (peut être hiérarchique avec des points, ex: "auth.title")
            default (str, optional): Valeur par défaut si la clé n'est pas trouvée
            **kwargs: Paramètres à remplacer dans la traduction (format {param})
            
        Returns:
            str: Texte traduit ou la clé si non trouvée
        """
        # Récupérer les traductions de la langue actuelle
        translations = self._translations.get(self._current_language, {})
        
        # Naviguer dans la structure hiérarchique
        keys = key.split(".")
        value = translations
        
        try:
            for k in keys:
                value = value[k]
            
            # Si on a trouvé une valeur, remplacer les paramètres si nécessaire
            if isinstance(value, str) and kwargs:
                try:
                    return value.format(**kwargs)
                except KeyError:
                    # Si un paramètre est manquant, retourner la valeur sans formatage
                    return value
            
            return str(value) if value is not None else (default or key)
            
        except (KeyError, TypeError):
            # Si la clé n'existe pas, essayer le fallback en français
            if self._current_language != "fr" and "fr" in self._translations:
                translations_fr = self._translations["fr"]
                value = translations_fr
                try:
                    for k in keys:
                        value = value[k]
                    if isinstance(value, str) and kwargs:
                        try:
                            return value.format(**kwargs)
                        except KeyError:
                            return value
                    return str(value) if value is not None else (default or key)
                except (KeyError, TypeError):
                    pass
            
            # Si toujours pas trouvé, retourner la valeur par défaut ou la clé
            return default if default is not None else key
    
    def reload(self):
        """
        Recharge les traductions depuis les fichiers
        Utile après modification des fichiers de traduction
        """
        self._translations = {}
        self._load_translations()


# Instance globale pour faciliter l'accès
_i18n_instance = None

def get_i18n() -> TranslationManager:
    """
    Retourne l'instance globale du gestionnaire de traductions
    
    Returns:
        TranslationManager: Instance du gestionnaire de traductions
    """
    global _i18n_instance
    if _i18n_instance is None:
        _i18n_instance = TranslationManager()
    return _i18n_instance

