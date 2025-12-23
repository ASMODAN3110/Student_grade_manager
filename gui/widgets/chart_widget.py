# -*- coding: utf-8 -*-
"""
Widget de graphique réutilisable
Intègre matplotlib dans CustomTkinter pour afficher des graphiques
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class ChartWidget(ctk.CTkFrame):
    """
    Widget de graphique avec matplotlib
    """
    
    def __init__(self, parent, title: str, subtitle: str = "", chart_type: str = "bar", **kwargs):
        """
        Initialise le widget de graphique
        
        Args:
            parent: Widget parent
            title (str): Titre du graphique
            subtitle (str): Sous-titre du graphique
            chart_type (str): Type de graphique ("bar" ou "line")
        """
        super().__init__(parent, **kwargs)
        
        self.title = title
        self.subtitle = subtitle
        self.chart_type = chart_type
        
        self.configure(fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Crée les widgets du graphique"""
        # Header avec titre et sous-titre
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=self.title,
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(anchor="w")
        
        if self.subtitle:
            subtitle_label = ctk.CTkLabel(
                header_frame,
                text=self.subtitle,
                font=ctk.CTkFont(size=12),
                text_color=("#808080", "#a0a0a0")
            )
            subtitle_label.pack(anchor="w", pady=(5, 0))
        
        # Figure matplotlib
        self.fig = Figure(figsize=(8, 4), facecolor='#1a1a1a')
        self.ax = self.fig.add_subplot(111, facecolor='#1a1a1a')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        
        # Canvas pour intégrer matplotlib
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().configure(bg='#1a1a1a')
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=(0, 20))
    
    def plot_bar_chart(self, labels: list, values: list, color: str = "#1F6AA5"):
        """
        Affiche un graphique en barres
        
        Args:
            labels (list): Labels pour l'axe X
            values (list): Valeurs pour l'axe Y
            color (str): Couleur des barres
        """
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        
        bars = self.ax.bar(labels, values, color=color)
        self.ax.set_ylabel('Nombre', color='white')
        
        # Ajouter les valeurs sur les barres
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}',
                        ha='center', va='bottom', color='white')
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def plot_line_chart(self, x_data: list, y_data: list, label: str = "", color: str = "#1F6AA5"):
        """
        Affiche un graphique en ligne
        
        Args:
            x_data (list): Données pour l'axe X
            y_data (list): Données pour l'axe Y
            label (str): Label de la ligne
            color (str): Couleur de la ligne
        """
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        self.ax.tick_params(colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['top'].set_color('white')
        self.ax.spines['right'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        
        self.ax.plot(x_data, y_data, marker='o', color=color, linewidth=2, label=label)
        self.ax.set_ylabel('Valeur', color='white')
        self.ax.legend(loc='upper left', facecolor='#1a1a1a', edgecolor='white', labelcolor='white')
        self.ax.grid(True, alpha=0.3, color='white')
        
        self.fig.tight_layout()
        self.canvas.draw()
    
    def clear(self):
        """Efface le graphique"""
        self.ax.clear()
        self.ax.set_facecolor('#1a1a1a')
        self.canvas.draw()

