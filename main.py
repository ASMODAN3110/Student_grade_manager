# -*- coding: utf-8 -*-
"""
Point d'entrée principal du système de gestion des notes scolaires
Gère l'authentification et lance l'application
"""

import sys
from services.file_manager import FileManager
from services.menu import Menu
from services.i18n import get_i18n


def authenticate(file_manager: FileManager, i18n, max_attempts: int = 3) -> bool:
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
    print(f"    {i18n.get('app.title')}")
    print("=" * 60)
    print(f"\n{i18n.get('auth.required')}")
    print(i18n.get('auth.attempts_remaining', max_attempts=max_attempts) + "\n")
    
    attempts = 0
    
    while attempts < max_attempts:
        try:
            user_password = input(i18n.get('auth.password_prompt')).strip()
            
            if user_password == password:
                print(f"\n{i18n.get('auth.success')}")
                return True
            else:
                attempts += 1
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"\n{i18n.get('auth.incorrect', remaining=remaining)}\n")
                else:
                    print(f"\n{i18n.get('auth.max_attempts')}")
                    return False
        
        except KeyboardInterrupt:
            # Gérer l'interruption par Ctrl+C
            print(f"\n\n{i18n.get('app.interrupt')}")
            sys.exit(0)
        except Exception as e:
            print(i18n.get('auth.error', error=str(e)))
            attempts += 1
    
    return False


def main():
    """
    Fonction principale du programme
    """
    try:
        # Initialiser le gestionnaire de fichiers
        file_manager = FileManager()
        
        # Charger la configuration et initialiser le gestionnaire de traductions
        config = file_manager.load_config()
        i18n = get_i18n()
        language = config.get('language', 'fr')
        i18n.set_language(language)
        
        # Demander le mode d'exécution
        print("=" * 60)
        print(f"    {i18n.get('app.title')}")
        print("=" * 60)
        print(f"\n{i18n.get('app.mode_selection')}")
        print(f"1. {i18n.get('app.mode_console')}")
        print(f"2. {i18n.get('app.mode_gui')}")
        
        choice = input(f"\n{i18n.get('app.mode_choice')}").strip()
        
        if choice == "2":
            # Lancer l'interface graphique
            from main_gui import main as gui_main
            gui_main()
            return
        
        # Mode console (par défaut)
        # Authentification
        if not authenticate(file_manager, i18n):
            print(f"\n{i18n.get('app.access_denied')}")
            sys.exit(1)
        
        # Initialiser le système de menus
        menu = Menu(file_manager, i18n)
        
        # Lancer le menu principal
        menu.handle_main_menu()
        
    except KeyboardInterrupt:
        # Gérer l'interruption par Ctrl+C
        i18n = get_i18n()
        print(f"\n\n{i18n.get('app.interrupt')}")
        sys.exit(0)
    except Exception as e:
        i18n = get_i18n()
        print(i18n.get('app.fatal_error', error=str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

