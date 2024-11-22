import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

class LeaderboardPage(ttk.Frame):
    def __init__(self, parent, stats):
        super().__init__(parent)
        self.stats = stats
        self.create_widgets()

    def create_widgets(self):
        # Title
        title_label = ttk.Label(self, text="Leaderboard", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.pack(pady=20)

        # Table headers
        headers = ["Player", "Wins", "Losses", "Games Played"]
        for col, header in enumerate(headers):
            label = ttk.Label(self, text=header, font=("Helvetica", 16, "bold"), bootstyle="inverse-secondary")
            label.grid(row=0, column=col, padx=10, pady=10)

        # Table rows
        for row, (player, stats) in enumerate(self.stats.items(), start=1):
            ttk.Label(self, text=player, font=("Helvetica", 14), bootstyle="inverse-secondary").grid(row=row, column=0, padx=10, pady=5)
            ttk.Label(self, text=stats["wins"], font=("Helvetica", 14), bootstyle="inverse-secondary").grid(row=row, column=1, padx=10, pady=5)
            ttk.Label(self, text=stats["losses"], font=("Helvetica", 14), bootstyle="inverse-secondary").grid(row=row, column=2, padx=10, pady=5)
            ttk.Label(self, text=stats["games_played"], font=("Helvetica", 14), bootstyle="inverse-secondary").grid(row=row, column=3, padx=10, pady=5)

        # Back button
        ttk.Button(self, text="Back", command=self.go_back, bootstyle="danger").pack(pady=20)

    def go_back(self):
        self.master.show_main_ui()