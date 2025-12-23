# -*- coding: utf-8 -*-
"""
Fenêtre d'authentification moderne
Design inspiré d'un login professionnel avec deux colonnes
"""

import customtkinter as ctk
import sys
from services.file_manager import FileManager


class LoginWindow(ctk.CTk):
    """
    Fenêtre de login avec design moderne
    """
    
    def __init__(self, app):
        """
        Initialise la fenêtre de login
        
        Args:
            app: Instance de l'application principale
        """
        super().__init__()
        
        self.app = app
        self.file_manager = FileManager()
        self.attempts = 0
        self.max_attempts = 3
        
        # Configuration de la fenêtre
        self.title("GradeMaster - Login")
        self.geometry("1000x600")
        self.resizable(False, False)
        
        # Centrer la fenêtre
        self._center_window()
        
        # Charger le mot de passe
        config = self.file_manager.load_config()
        self.password = config.get('password', 'password')
        
        self._create_widgets()
    
    def _center_window(self):
        """Centre la fenêtre sur l'écran"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_widgets(self):
        """Crée les widgets de la fenêtre de login"""
        # Container principal
        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True)
        
        # Colonne gauche - Image de fond avec message
        left_frame = ctk.CTkFrame(main_container, fg_color="#1F6AA5", corner_radius=0)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Contenu de la colonne gauche
        left_content = ctk.CTkFrame(left_frame, fg_color="transparent")
        left_content.place(relx=0.5, rely=0.5, anchor="center")
        
        # Icône de graduation
        icon_label = ctk.CTkLabel(
            left_content,
            text="🎓",
            font=ctk.CTkFont(size=80)
        )
        icon_label.pack(pady=(0, 30))
        
        # Message d'accueil
        self.welcome_text = ctk.CTkLabel(
            left_content,
            text=self.app.i18n.get('auth.academic_excellence'),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white",
            justify="center"
        )
        self.welcome_text.pack(pady=(0, 20))
        
        self.subtitle_text = ctk.CTkLabel(
            left_content,
            text=self.app.i18n.get('auth.academic_subtitle'),
            font=ctk.CTkFont(size=14),
            text_color="white",
            justify="center"
        )
        self.subtitle_text.pack()
        
        # Colonne droite - Formulaire de connexion
        right_frame = ctk.CTkFrame(main_container, fg_color=("#2b2b2b", "#1a1a1a"))
        right_frame.pack(side="right", fill="both", expand=True, padx=0)
        
        # Container du formulaire
        form_container = ctk.CTkFrame(right_frame, fg_color="transparent")
        form_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo en haut
        logo_label = ctk.CTkLabel(
            form_container,
            text="📊 GradeMaster Admin",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        logo_label.pack(pady=(0, 40))
        
        # Titre
        self.title_label = ctk.CTkLabel(
            form_container,
            text=self.app.i18n.get('auth.welcome_back'),
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.title_label.pack(pady=(0, 10))
        
        self.subtitle_label = ctk.CTkLabel(
            form_container,
            text=self.app.i18n.get('auth.enter_details'),
            font=ctk.CTkFont(size=14),
            text_color=("#808080", "#a0a0a0")
        )
        self.subtitle_label.pack(pady=(0, 40))
        
        # Champ Username/Faculty ID
        self.username_label = ctk.CTkLabel(
            form_container,
            text=self.app.i18n.get('auth.username_label'),
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.username_label.pack(fill="x", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            form_container,
            placeholder_text=self.app.i18n.get('auth.username_placeholder'),
            width=400,
            height=50,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(pady=(0, 20))
        
        # Champ Password
        password_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 5))
        
        self.password_label = ctk.CTkLabel(
            password_frame,
            text=self.app.i18n.get('auth.password_label'),
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.password_label.pack(side="left")
        
        self.forgot_link = ctk.CTkLabel(
            password_frame,
            text=self.app.i18n.get('auth.forgot_password'),
            font=ctk.CTkFont(size=12),
            text_color="#1F6AA5",
            cursor="hand2"
        )
        self.forgot_link.pack(side="right")
        
        self.password_entry = ctk.CTkEntry(
            form_container,
            placeholder_text=self.app.i18n.get('auth.password_placeholder'),
            width=400,
            height=50,
            font=ctk.CTkFont(size=14),
            show="*"
        )
        self.password_entry.pack(pady=(0, 30))
        self.password_entry.bind("<Return>", lambda e: self._login())
        
        # Message d'erreur
        self.error_label = ctk.CTkLabel(
            form_container,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.error_label.pack(pady=(0, 20))
        
        # Bouton Sign In
        self.signin_btn = ctk.CTkButton(
            form_container,
            text=self.app.i18n.get('auth.sign_in'),
            width=400,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1F6AA5",
            hover_color="#1a5a8a",
            command=self._login
        )
        self.signin_btn.pack(pady=(0, 20))
        
        # Lien Contact Administration
        contact_frame = ctk.CTkFrame(form_container, fg_color="transparent")
        contact_frame.pack()
        
        self.contact_label = ctk.CTkLabel(
            contact_frame,
            text=self.app.i18n.get('auth.no_account'),
            font=ctk.CTkFont(size=12),
            text_color=("#808080", "#a0a0a0")
        )
        self.contact_label.pack(side="left", padx=(0, 5))
        
        self.contact_link = ctk.CTkLabel(
            contact_frame,
            text=self.app.i18n.get('auth.contact_admin'),
            font=ctk.CTkFont(size=12),
            text_color="#1F6AA5",
            cursor="hand2"
        )
        self.contact_link.pack(side="left")
        
        # Footer
        footer_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=30, pady=20)
        
        self.secure_label = ctk.CTkLabel(
            footer_frame,
            text=self.app.i18n.get('auth.secure_portal'),
            font=ctk.CTkFont(size=11),
            text_color=("#808080", "#808080")
        )
        self.secure_label.pack(side="left")
        
        self.copyright_label = ctk.CTkLabel(
            footer_frame,
            text=self.app.i18n.get('auth.copyright'),
            font=ctk.CTkFont(size=10),
            text_color=("#808080", "#808080")
        )
        self.copyright_label.pack(side="right")
    
    def _login(self):
        """Gère la connexion"""
        password = self.password_entry.get()
        
        if password == self.password:
            # Authentification réussie
            self.app.authenticated = True
            # Fermer la fenêtre de login
            self.quit()
            self.destroy()
            # Afficher la fenêtre principale
            self.app.show_main_window()
        else:
            # Authentification échouée
            self.attempts += 1
            remaining = self.max_attempts - self.attempts
            
            if remaining > 0:
                self.error_label.configure(
                    text=self.app.i18n.get('auth.incorrect', remaining=remaining)
                )
            else:
                self.error_label.configure(
                    text=self.app.i18n.get('auth.max_attempts')
                )
                self.after(2000, lambda: (self.quit(), sys.exit()))

