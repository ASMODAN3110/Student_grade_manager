# -*- coding: utf-8 -*-
"""
Composant Sidebar - Navigation latérale
"""

import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    """
    Sidebar de navigation avec menu items
    """
    
    def __init__(self, parent, main_window=None, on_item_selected=None, **kwargs):
        """
        Initialise la sidebar
        
        Args:
            parent: Widget parent
            main_window: Fenêtre principale (pour accéder à i18n)
            on_item_selected: Callback appelé quand un item est sélectionné (item_id)
        """
        super().__init__(parent, **kwargs)
        
        self.main_window = main_window
        self.on_item_selected = on_item_selected
        self.selected_item = "dashboard"
        
        self.configure(fg_color=("#1a1a1a", "#1a1a1a"), width=250, corner_radius=0)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée les widgets de la sidebar"""
        # Logo en haut
        logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(30, 40))
        
        i18n = self.main_window.app.i18n if self.main_window else None
        self.logo_label = ctk.CTkLabel(
            logo_frame,
            text=i18n.get('gui.sidebar.logo') if i18n else "📊 GradeMaster",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.pack()
        
        # Menu items - stocker les IDs pour la traduction
        self.menu_item_ids = [
            ("dashboard", "gui.sidebar.dashboard"),
            ("students", "gui.sidebar.students"),
            ("subjects", "gui.sidebar.subjects"),
            ("grades", "gui.sidebar.grades"),
            ("consultation", "gui.sidebar.consultation"),
            ("statistics", "gui.sidebar.statistics"),
        ]
        
        self.item_buttons = {}
        
        for item_id, i18n_key in self.menu_item_ids:
            text = i18n.get(i18n_key) if i18n else item_id.capitalize()
            btn = ctk.CTkButton(
                self,
                text=text,
                font=ctk.CTkFont(size=14),
                anchor="w",
                fg_color="transparent",
                hover_color=("#2b2b2b", "#2b2b2b"),
                command=lambda id=item_id: self._select_item(id)
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.item_buttons[item_id] = btn
        
        # Espaceur
        spacer = ctk.CTkFrame(self, fg_color="transparent", height=20)
        spacer.pack(fill="x")
        
        # Section Settings
        self.settings_label = ctk.CTkLabel(
            self,
            text=i18n.get('gui.sidebar.settings') if i18n else "SETTINGS",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#808080", "#808080")
        )
        self.settings_label.pack(anchor="w", padx=20, pady=(20, 10))
        
        self.settings_btn = ctk.CTkButton(
            self,
            text=i18n.get('gui.sidebar.settings_button') if i18n else "⚙️ Settings",
            font=ctk.CTkFont(size=14),
            anchor="w",
            fg_color="transparent",
            hover_color=("#2b2b2b", "#2b2b2b"),
            command=lambda: self._select_item("settings")
        )
        self.settings_btn.pack(fill="x", padx=10, pady=5)
        
        # Profil utilisateur en bas
        profile_frame = ctk.CTkFrame(self, fg_color=("#2b2b2b", "#2b2b2b"), corner_radius=10)
        profile_frame.pack(fill="x", padx=10, pady=(20, 20), side="bottom")
        
        self.profile_label = ctk.CTkLabel(
            profile_frame,
            text=i18n.get('gui.sidebar.profile') if i18n else "👤 Admin user\nadmin@school.edu",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.profile_label.pack(padx=15, pady=15)
        
        # Ne pas sélectionner automatiquement - laisser la fenêtre principale gérer l'affichage initial
        # Le dashboard sera sélectionné visuellement après la création de content_frame
    
    def _select_item(self, item_id: str):
        """Sélectionne un item du menu"""
        # Réinitialiser tous les boutons
        for btn_id, btn in self.item_buttons.items():
            btn.configure(fg_color="transparent")
        
        # Mettre en surbrillance l'item sélectionné
        if item_id in self.item_buttons:
            self.item_buttons[item_id].configure(fg_color=("#1F6AA5", "#1F6AA5"))
        
        self.selected_item = item_id
        
        # Appeler le callback
        if self.on_item_selected:
            self.on_item_selected(item_id)
    
    def _update_texts(self):
        """Met à jour les textes de la sidebar"""
        if not self.main_window:
            return
        
        i18n = self.main_window.app.i18n
        self.logo_label.configure(text=i18n.get('gui.sidebar.logo'))
        self.settings_label.configure(text=i18n.get('gui.sidebar.settings'))
        self.settings_btn.configure(text=i18n.get('gui.sidebar.settings_button'))
        self.profile_label.configure(text=i18n.get('gui.sidebar.profile'))
        
        # Mettre à jour les boutons du menu
        for item_id, i18n_key in self.menu_item_ids:
            if item_id in self.item_buttons:
                self.item_buttons[item_id].configure(text=i18n.get(i18n_key))

