# -*- coding: utf-8 -*-
"""
Widget de tableau de données réutilisable
Affiche des données dans un tableau avec tri et recherche
"""

import customtkinter as ctk
from tkinter import ttk


class DataTable(ctk.CTkFrame):
    """
    Tableau de données avec recherche et tri
    """
    
    def __init__(self, parent, columns: list, data: list = None, **kwargs):
        """
        Initialise le tableau de données
        
        Args:
            parent: Widget parent
            columns (list): Liste des colonnes [(nom, largeur), ...]
            data (list): Données initiales (liste de tuples)
        """
        super().__init__(parent, **kwargs)
        
        self.columns = columns
        self.data = data or []
        self.filtered_data = self.data.copy()
        
        self.configure(fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée les widgets du tableau"""
        # Frame de recherche
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        search_label = ctk.CTkLabel(search_frame, text="Rechercher:", font=ctk.CTkFont(size=12))
        search_label.pack(side="left", padx=(0, 10))
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Tapez pour rechercher...")
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Frame pour le Treeview
        tree_frame = ctk.CTkFrame(self, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Treeview avec scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=[col[0] for col in self.columns],
            show="headings",
            yscrollcommand=scrollbar.set,
            style="Custom.Treeview"
        )
        scrollbar.config(command=self.tree.yview)
        
        # Configuration des colonnes
        for col_name, width in self.columns:
            self.tree.heading(col_name, text=col_name, command=lambda c=col_name: self._sort_column(c))
            self.tree.column(col_name, width=width, anchor="w")
        
        self.tree.pack(fill="both", expand=True)
        
        # Style pour le Treeview (thème sombre)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.Treeview",
                       background="#2b2b2b",
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0)
        style.configure("Custom.Treeview.Heading",
                       background="#1a1a1a",
                       foreground="white",
                       borderwidth=1)
        style.map("Custom.Treeview",
                 background=[("selected", "#1F6AA5")])
        
        # Charger les données
        self._load_data()
    
    def _load_data(self):
        """Charge les données dans le tableau"""
        # Effacer les données existantes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Ajouter les données filtrées
        for row in self.filtered_data:
            self.tree.insert("", "end", values=row)
    
    def _on_search(self, event=None):
        """Filtre les données selon la recherche"""
        search_term = self.search_entry.get().lower()
        
        if not search_term:
            self.filtered_data = self.data.copy()
        else:
            self.filtered_data = [
                row for row in self.data
                if any(str(cell).lower().find(search_term) != -1 for cell in row)
            ]
        
        self._load_data()
    
    def _sort_column(self, col):
        """Trie les données par colonne"""
        # Récupérer les données actuelles
        items = [(self.tree.set(item, col), item) for item in self.tree.get_children("")]
        
        # Trier
        try:
            items.sort(key=lambda t: float(t[0]) if t[0].replace('.', '').isdigit() else t[0])
        except:
            items.sort(key=lambda t: t[0])
        
        # Réorganiser les items
        for index, (val, item) in enumerate(items):
            self.tree.move(item, "", index)
    
    def set_data(self, data: list):
        """Met à jour les données du tableau"""
        self.data = data
        self.filtered_data = data.copy()
        self._load_data()
    
    def get_selected_item(self):
        """Retourne l'item sélectionné"""
        selection = self.tree.selection()
        if selection:
            return self.tree.item(selection[0])['values']
        return None
    
    def clear_selection(self):
        """Efface la sélection"""
        for item in self.tree.selection():
            self.tree.selection_remove(item)

