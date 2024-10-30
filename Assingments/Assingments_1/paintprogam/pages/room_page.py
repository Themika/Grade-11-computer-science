import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
import math

class RoomPage(ttk.Frame):
    def __init__(self, container, parent, num_rooms):
        super().__init__(container)
        self.parent = parent
        self.num_rooms = num_rooms
        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Enter the dimensions of each wall", font=("Helvetica", 16, "bold"))
        label.grid(row=0, column=0, columnspan=8, pady=10)
    
        try:
            num_rooms = self.num_rooms
        except ValueError:
            self.parent.rooms_error_label.config(text="Please enter a valid number of rooms (1-5).")
            return
    
        self.wall_entries = {}
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
            self.square_footage_labels[room].config(text=f"Square Footage: {total_square_footage}")
            self.update_total_square_footage()

        for room in range(1, num_rooms + 1):
            if room > 3:
                col_offset = 9
                if room == 4:
                    row_right = 1
    
            current_row = row_left if room <= 3 else row_right
    
            room_label = ttk.Label(self, text=f"Room {room}", font=("Helvetica", 14, "bold"))
            room_label.grid(row=current_row, column=col_offset, columnspan=4, pady=10)
            current_row += 1
    
            self.wall_entries[room] = []
            self.square_footage_labels[room] = ttk.Label(self, text="Square Footage: 0", font=("Helvetica", 12))
            self.square_footage_labels[room].grid(row=current_row, column=col_offset + 4, pady=5, padx=5, sticky=tk.W)
            
    
            for wall in range(1, 5):
                wall_length_label = ttk.Label(self, text=f"Wall {wall} Length:")
                wall_length_label.grid(row=current_row, column=col_offset, pady=5, padx=5, sticky=tk.W)
                wall_length_entry = ttk.Entry(self, bootstyle="info")
                wall_length_entry.grid(row=current_row, column=col_offset + 1, pady=5, padx=5)
                wall_length_entry.bind('<KeyRelease>', lambda e, entry=wall_length_entry, room=room: [validate_input(e, entry), update_square_footage(room)])
                self.wall_entries[room].append(wall_length_entry)
    
                wall_width_label = ttk.Label(self, text=f"Wall {wall} Width:")
                wall_width_label.grid(row=current_row, column=col_offset + 2, pady=5, padx=5, sticky=tk.W)
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
    
        self.total_square_footage_label = ttk.Label(self, text="Total Square Footage: 0", font=("Helvetica", 14, "bold"))
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
                messagebox.showerror("Error", "Please correct the highlighted fields. All dimensions must be positive numbers.")
    
        submit_button = ttk.Button(self, text="Submit Wall Dimensions", command=validate_all_inputs, bootstyle="success")
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
        self.total_square_footage_label.config(text=f"Total Square Footage: {total_square_footage} (Paint Cans Needed: {total_paint_cans})")
        self.parent.user_data.update({"total_square_footage": total_square_footage, "total_paint_cans": total_paint_cans})
