import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import math

translations = {
    "English": {
        "enter_dimensions": "Enter the dimensions of each wall",
        "room_error": "Please enter a valid number of rooms (1-5).",
        "square_footage": "Square Footage: {0}",
        "total_square_footage": "Total Square Footage: {0} (Paint Cans Needed: {1})",
        "submit_wall_dimensions": "Submit Wall Dimensions",
        "error": "Error",
        "correct_fields": "Please correct the highlighted fields. All dimensions must be positive numbers.",
        "room_label": "Room {0}",
        "wall_length": "Wall {0} Length:",
        "wall_width": "Wall {0} Width:"
    },
    "French": {
        "enter_dimensions": "Entrez les dimensions de chaque mur",
        "room_error": "Veuillez entrer un nombre de pièces valide (1-5).",
        "square_footage": "Superficie: {0}",
        "total_square_footage": "Superficie totale: {0} (Boîtes de peinture nécessaires: {1})",
        "submit_wall_dimensions": "Soumettre les dimensions des murs",
        "error": "Erreur",
        "correct_fields": "Veuillez corriger les champs en surbrillance. Toutes les dimensions doivent être des nombres positifs.",
        "room_label": "Pièce {0}",
        "wall_length": "Longueur du mur {0} :",
        "wall_width": "Largeur du mur {0} :"
    }
}

class RoomPage(ttk.Frame):
    def __init__(self, container, parent, num_rooms):
        super().__init__(container)
        self.parent = parent
        self.num_rooms = num_rooms
        self.language = parent.current_language
        self.create_widgets()

    def create_widgets(self):
        self.label = ttk.Label(self, text=translations[self.language]["enter_dimensions"], font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=8, pady=10)
    
        try:
            num_rooms = self.num_rooms
        except ValueError:
            self.parent.rooms_error_label.config(text=translations[self.language]["room_error"])
            return
    
        self.wall_entries = {}
        self.wall_length_labels = {}
        self.wall_width_labels = {}
        self.square_footage_labels = {}
    
        row_left = 1
        row_right = 1
        col_offset = 0
    
        def validate_input(event, entry):
            value = entry.get().strip()
            try:
                num = float(value)
                if num <= 0:
                    entry.configure(bootstyle="danger")
                    return False
                entry.configure(bootstyle="info")
                return True
            except ValueError:
                entry.configure(bootstyle="danger")
                return False
    
        def update_square_footage(room):
            total_square_footage = 0
            for i in range(0, len(self.wall_entries[room]), 2):
                length_entry = self.wall_entries[room][i]
                width_entry = self.wall_entries[room][i + 1]
                try:
                    length = float(length_entry.get().strip())
                    width = float(width_entry.get().strip())
                    total_square_footage += length * width
                except ValueError:
                    continue
            self.square_footage_labels[room].config(text=translations[self.language]["square_footage"].format(total_square_footage))
            self.update_total_square_footage()

        for room in range(1, num_rooms + 1):
            if room > 3:
                col_offset = 9
                if room == 4:
                    row_right = 1
    
            current_row = row_left if room <= 3 else row_right
    
            room_label = ttk.Label(self, text=translations[self.language]["room_label"].format(room), font=("Helvetica", 14, "bold"))
            room_label.grid(row=current_row, column=col_offset, columnspan=4, pady=10)
            current_row += 1
    
            self.wall_entries[room] = []
            self.wall_length_labels[room] = []
            self.wall_width_labels[room] = []
            self.square_footage_labels[room] = ttk.Label(self, text=translations[self.language]["square_footage"].format(0), font=("Helvetica", 12))
            self.square_footage_labels[room].grid(row=current_row, column=col_offset + 4, pady=5, padx=5, sticky=tk.W)
            
    
            for wall in range(1, 5):
                wall_length_label = ttk.Label(self, text=translations[self.language]["wall_length"].format(wall))
                wall_length_label.grid(row=current_row, column=col_offset, pady=5, padx=5, sticky=tk.W)
                self.wall_length_labels[room].append(wall_length_label)
                wall_length_entry = ttk.Entry(self, bootstyle="info")
                wall_length_entry.grid(row=current_row, column=col_offset + 1, pady=5, padx=5)
                wall_length_entry.bind('<KeyRelease>', lambda e, entry=wall_length_entry, room=room: [validate_input(e, entry), update_square_footage(room)])
                self.wall_entries[room].append(wall_length_entry)
    
                wall_width_label = ttk.Label(self, text=translations[self.language]["wall_width"].format(wall))
                wall_width_label.grid(row=current_row, column=col_offset + 2, pady=5, padx=5, sticky=tk.W)
                self.wall_width_labels[room].append(wall_width_label)
                wall_width_entry = ttk.Entry(self, bootstyle="info")
                wall_width_entry.grid(row=current_row, column=col_offset + 3, pady=5, padx=5)
                wall_width_entry.bind('<KeyRelease>', lambda e, entry=wall_width_entry, room=room: [validate_input(e, entry), update_square_footage(room)])
                self.wall_entries[room].append(wall_width_entry)
    
                current_row += 1
    
            if room <= 3:
                row_left = current_row
            else:
                row_right = current_row
    
        submit_row = max(row_left, row_right)
    
        self.total_square_footage_label = ttk.Label(self, text=translations[self.language]["total_square_footage"].format(0, 0), font=("Helvetica", 14, "bold"))
        self.total_square_footage_label.grid(row=submit_row, column=0, columnspan=8, pady=10)
    
        def validate_all_inputs():
            all_valid = True
            for room_entries in self.wall_entries.values():
                for entry in room_entries:
                    if not validate_input(None, entry):
                        all_valid = False
            if all_valid:
                self.parent.on_submit_walls(self.wall_entries)
                self.parent.create_paint_options_page()  # Open the PaintOptionsPage
            else:
                messagebox.showerror(translations[self.language]["error"], translations[self.language]["correct_fields"])
    
        submit_button = ttk.Button(self, text=translations[self.language]["submit_wall_dimensions"], command=validate_all_inputs, bootstyle="success")
        submit_button.grid(row=submit_row + 1, column=0, columnspan=8, pady=10)

    def update_total_square_footage(self):
        total_square_footage = 0
        for room in self.wall_entries:
            for i in range(0, len(self.wall_entries[room]), 2):
                length_entry = self.wall_entries[room][i]
                width_entry = self.wall_entries[room][i + 1]
                try:
                    length = float(length_entry.get().strip())
                    width = float(width_entry.get().strip())
                    total_square_footage += length * width
                except ValueError:
                    continue
        total_paint_cans = math.ceil(total_square_footage / 400)
        self.total_square_footage_label.config(text=translations[self.language]["total_square_footage"].format(total_square_footage, total_paint_cans))
        self.parent.user_data.update({"total_square_footage": total_square_footage, "total_paint_cans": total_paint_cans})

    def update_language(self, language):
        self.language = language
        self.label.config(text=translations[language]["enter_dimensions"])
        for room in range(1, self.num_rooms + 1):
            self.square_footage_labels[room].config(text=translations[language]["square_footage"].format(0))
        self.total_square_footage_label.config(text=translations[language]["total_square_footage"].format(0, 0))
        for room in range(1, self.num_rooms + 1):
            for i in range(4):
                self.wall_length_labels[room][i].config(text=translations[language]["wall_length"].format(i + 1))
                self.wall_width_labels[room][i].config(text=translations[language]["wall_width"].format(i + 1))