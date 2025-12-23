# -*- coding: utf-8 -*-
"""
Widget de carte de statistique réutilisable
Affiche une métrique avec icône, valeur et variation
"""

import customtkinter as ctk


class StatCard(ctk.CTkFrame):
    """
    Carte de statistique avec icône, valeur et sous-texte
    """
    
    def __init__(self, parent, title: str, value: str, subtitle: str = "", 
                 icon_color: str = "#1F6AA5", icon_text: str = "📊", **kwargs):
        """
        Initialise la carte de statistique
        
        Args:
            parent: Widget parent
            title (str): Titre de la carte (ex: "TOTAL STUDENTS")
            value (str): Valeur principale à afficher
            subtitle (str): Sous-texte avec variation (ex: "+12 this week")
            icon_color (str): Couleur de l'icône
            icon_text (str): Texte/emoji de l'icône
        """
        super().__init__(parent, **kwargs)
        
        self.title = title
        self.value = value
        self.subtitle = subtitle
        self.icon_color = icon_color
        
        self._create_widgets(icon_text)
    
    def _create_widgets(self, icon_text: str):
        """Crée les widgets de la carte"""
        # Container principal avec padding
        self.configure(fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        
        # Grid layout
        self.grid_columnconfigure(1, weight=1)
        
        # Icône à gauche
        icon_frame = ctk.CTkFrame(self, width=60, height=60, corner_radius=12, 
                                  fg_color=self.icon_color)
        icon_frame.grid(row=0, column=0, padx=(20, 15), pady=20, sticky="nsw")
        icon_frame.grid_propagate(False)
        
        icon_label = ctk.CTkLabel(icon_frame, text=icon_text, font=ctk.CTkFont(size=24))
        icon_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # Contenu à droite
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=0, column=1, padx=(0, 20), pady=20, sticky="ew")
        
        # Titre
        title_label = ctk.CTkLabel(
            content_frame, 
            text=self.title,
            font=ctk.CTkFont(size=12, weight="normal"),
            text_color=("#808080", "#a0a0a0")
        )
        title_label.pack(anchor="w", pady=(0, 5))
        
        # Valeur principale
        value_label = ctk.CTkLabel(
            content_frame,
            text=self.value,
            font=ctk.CTkFont(size=32, weight="bold")
        )
        value_label.pack(anchor="w", pady=(0, 5))
        
        # Sous-texte avec variation
        if self.subtitle:
            subtitle_label = ctk.CTkLabel(
                content_frame,
                text=self.subtitle,
                font=ctk.CTkFont(size=11),
                text_color=("#4CAF50", "#4CAF50")
            )
            subtitle_label.pack(anchor="w")
    
    def update_value(self, new_value: str, new_subtitle: str = ""):
        """Met à jour la valeur et le sous-texte"""
        self.value = new_value
        self.subtitle = new_subtitle
        # Recréer les widgets pour mettre à jour
        for widget in self.winfo_children():
            widget.destroy()
        self._create_widgets("📊")

