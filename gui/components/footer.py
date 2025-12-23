# -*- coding: utf-8 -*-
"""
Composant Footer - Pied de page de l'application
"""

import customtkinter as ctk


class Footer(ctk.CTkFrame):
    """
    Footer avec copyright et version
    """
    
    def __init__(self, parent, **kwargs):
        """
        Initialise le footer
        
        Args:
            parent: Widget parent
        """
        super().__init__(parent, **kwargs)
        
        self.configure(fg_color=("#1a1a1a", "#1a1a1a"), height=50, corner_radius=0)
        self.pack_propagate(False)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée les widgets du footer"""
        # Container principal
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=10)
        
        # Copyright à droite
        copyright_label = ctk.CTkLabel(
            main_frame,
            text="© 2024 GradeMaster. Academic Management System v1.0",
            font=ctk.CTkFont(size=11),
            text_color=("#808080", "#808080")
        )
        copyright_label.pack(side="right")

