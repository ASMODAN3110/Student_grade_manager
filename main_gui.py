# -*- coding: utf-8 -*-
"""
Point d'entrée pour l'interface graphique
"""

import sys
from gui.app import App


def main():
    """
    Fonction principale pour lancer l'interface graphique
    """
    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        print("\n\nInterruption par l'utilisateur. Au revoir !")
        sys.exit(0)
    except Exception as e:
        print(f"\nErreur fatale: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

