# -*- coding: utf-8 -*-
"""
Composant Header - En-tête de l'application
"""

import customtkinter as ctk
from datetime import datetime


class Header(ctk.CTkFrame):
    """
    Header avec logo, salutation et actions rapides
    """
    
    def __init__(self, parent, main_window=None, on_import_data=None, on_new_entry=None, **kwargs):
        """
        Initialise le header
        
        Args:
            parent: Widget parent
            main_window: Fenêtre principale (pour accéder à i18n)
            on_import_data: Callback pour le bouton Import Data
            on_new_entry: Callback pour le bouton New Entry
        """
        super().__init__(parent, **kwargs)
        
        self.main_window = main_window
        self.on_import_data = on_import_data
        self.on_new_entry = on_new_entry
        
        self.configure(fg_color=("#1a1a1a", "#1a1a1a"), height=120, corner_radius=0)
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée les widgets du header"""
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Partie gauche - Logo et salutation
        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y")
        
        # Logo et nom
        logo_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        logo_frame.pack(anchor="w", pady=(0, 10))
        
        self.logo_label = ctk.CTkLabel(
            logo_frame,
            text=self.main_window.app.i18n.get('gui.header.logo') if self.main_window else "🛡️ GradeMaster Admin",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(side="left", padx=(0, 20))
        
        # Salutation
        greeting = self._get_greeting()
        self.greeting_label = ctk.CTkLabel(
            left_frame,
            text=greeting,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.greeting_label.pack(anchor="w", pady=(0, 5))
        
        # Message de synchronisation
        self.sync_label = ctk.CTkLabel(
            left_frame,
            text=self.main_window.app.i18n.get('gui.header.sync_message') if self.main_window else "Here is today's overview. Data last synced: Just now.",
            font=ctk.CTkFont(size=12),
            text_color=("#808080", "#a0a0a0")
        )
        self.sync_label.pack(anchor="w")
        
        # Partie droite - Boutons d'action
        right_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y")
        
        # Sélecteur de langue
        if self.main_window:
            lang_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
            lang_frame.pack(side="right", padx=(10, 0))
            
            self.lang_combo = ctk.CTkComboBox(
                lang_frame,
                values=["🇫🇷 Français", "🇬🇧 English"],
                width=150,
                command=self._on_language_change
            )
            current_lang = self.main_window.app.i18n.get_current_language()
            self.lang_combo.set("🇫🇷 Français" if current_lang == "fr" else "🇬🇧 English")
            self.lang_combo.pack()
        
        # Bouton Import Data
        self.import_btn = ctk.CTkButton(
            right_frame,
            text=self.main_window.app.i18n.get('gui.header.import_data') if self.main_window else "☁️ Import Data",
            font=ctk.CTkFont(size=14),
            fg_color=("#2b2b2b", "#2b2b2b"),
            hover_color=("#3b3b3b", "#3b3b3b"),
            command=self.on_import_data or (lambda: None)
        )
        self.import_btn.pack(side="right", padx=(10, 0))
        
        # Bouton New Entry
        self.new_entry_btn = ctk.CTkButton(
            right_frame,
            text=self.main_window.app.i18n.get('gui.header.new_entry') if self.main_window else "➕ New Entry",
            font=ctk.CTkFont(size=14),
            fg_color=("#1F6AA5", "#1F6AA5"),
            hover_color=("#1a5a8a", "#1a5a8a"),
            command=self.on_new_entry or (lambda: None)
        )
        self.new_entry_btn.pack(side="right")
    
    def _get_greeting(self) -> str:
        """Retourne la salutation selon l'heure"""
        if not self.main_window:
            return "Good morning, Admin"
        
        hour = datetime.now().hour
        if hour < 12:
            return self.main_window.app.i18n.get('gui.header.greeting_morning')
        elif hour < 18:
            return self.main_window.app.i18n.get('gui.header.greeting_afternoon')
        else:
            return self.main_window.app.i18n.get('gui.header.greeting_evening')
    
    def _on_language_change(self, choice):
        """Gère le changement de langue"""
        if not self.main_window:
            return
        
        lang = "fr" if "Français" in choice else "en"
        self.main_window.app.i18n.set_language(lang)
        self.main_window.app.file_manager.save_language(lang)
        
        # Mettre à jour tous les textes
        self._update_texts()
        if hasattr(self.main_window, '_update_all_texts'):
            self.main_window._update_all_texts()
    
    def _update_texts(self):
        """Met à jour les textes du header"""
        if not self.main_window:
            return
        
        i18n = self.main_window.app.i18n
        self.logo_label.configure(text=i18n.get('gui.header.logo'))
        self.greeting_label.configure(text=self._get_greeting())
        self.sync_label.configure(text=i18n.get('gui.header.sync_message'))
        self.import_btn.configure(text=i18n.get('gui.header.import_data'))
        self.new_entry_btn.configure(text=i18n.get('gui.header.new_entry'))
    
    def update_sync_time(self):
        """Met à jour le temps de synchronisation"""
        # Cette méthode peut être appelée pour mettre à jour le message
        pass

