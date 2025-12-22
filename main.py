# -*- coding: utf-8 -*-
"""
Point d'entrée principal du système de gestion des notes scolaires
Gère l'authentification et lance l'application
"""

import sys
from services.file_manager import FileManager
from services.menu import Menu


def authenticate(file_manager: FileManager, max_attempts: int = 3) -> bool:
    """
    Gère l'authentification par mot de passe
    
    Args:
        file_manager (FileManager): Gestionnaire de fichiers pour lire la config
        max_attempts (int): Nombre maximum de tentatives autorisées
        
    Returns:
        bool: True si l'authentification réussit, False sinon
    """
    # Charger la configuration
    config = file_manager.load_config()
    password = config.get('password', 'password')  # Mot de passe par défaut
    
    print("=" * 60)
    print("    SYSTÈME DE GESTION DES NOTES SCOLAIRES")
    print("=" * 60)
    print("\nAuthentification requise")
    print(f"Vous avez {max_attempts} tentative(s) pour vous connecter\n")
    
    attempts = 0
    
    while attempts < max_attempts:
        try:
            user_password = input("Mot de passe: ").strip()
            
            if user_password == password:
                print("\n✓ Authentification réussie !")
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"\n✗ Mot de passe incorrect. Il vous reste {remaining} tentative(s).\n")
                else:
                    print("\n✗ Nombre maximum de tentatives atteint. Accès refusé.")
                    return False
        
        except KeyboardInterrupt:
            # Gérer l'interruption par Ctrl+C
            print("\n\nInterruption par l'utilisateur. Au revoir !")
            sys.exit(0)
        except Exception as e:
            print(f"\nErreur lors de l'authentification: {e}")
            attempts += 1
    
    return False


def main():
    """
    Fonction principale du programme
    """
    try:
        # Initialiser le gestionnaire de fichiers
        file_manager = FileManager()
        
        # Authentification
        if not authenticate(file_manager):
            print("\nAccès refusé. Le programme se termine.")
            sys.exit(1)
        
        # Initialiser le système de menus
        menu = Menu(file_manager)
        
        # Lancer le menu principal
        menu.handle_main_menu()
        
    except KeyboardInterrupt:
        # Gérer l'interruption par Ctrl+C
        print("\n\nInterruption par l'utilisateur. Au revoir !")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur fatale: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

