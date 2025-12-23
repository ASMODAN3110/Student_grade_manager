# -*- coding: utf-8 -*-
"""
Application principale CustomTkinter
Gère la configuration et l'initialisation de l'interface graphique
"""

import customtkinter as ctk
from services.file_manager import FileManager
from services.i18n import get_i18n


class App:
    """
    Classe principale de l'application GUI
    """
    
    def __init__(self):
        """Initialise l'application"""
        # Configuration CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialiser le gestionnaire de fichiers
        self.file_manager = FileManager()
        
        # Charger la configuration et initialiser le gestionnaire de traductions
        config = self.file_manager.load_config()
        self.i18n = get_i18n()
        language = config.get('language', 'fr')
        self.i18n.set_language(language)
        
        # État de l'application
        self.authenticated = False
        self.current_window = None
    
    def run(self):
        """Lance l'application"""
        # Importer ici pour éviter les imports circulaires
        from gui.windows.login_window import LoginWindow
        
        # Créer et afficher la fenêtre de login
        login_window = LoginWindow(self)
        login_window.mainloop()
    
    def show_main_window(self):
        """Affiche la fenêtre principale après authentification"""
        if self.current_window:
            self.current_window.destroy()
        
        from gui.windows.main_window import MainWindow
        
        self.current_window = MainWindow(self)
        self.current_window.mainloop()

