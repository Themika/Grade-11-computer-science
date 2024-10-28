import math
import smtplib
import re
import os
import requests

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk  # Import tkinter as tk
from tkinter import colorchooser  # Import colorchooser for color selection
from tkinter import messagebox

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime
from random import randint
"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program is a simple program that will allow a user to choose from various interior paint options. Then give you an invoice on the cost
of painting the room, providing you with multiple payment options.

Functions used
Enumerate()
//https://www.w3schools.com/python/ref_func_enumerate.asp
isInstance()
//https://www.w3schools.com/python/ref_func_isinstance.asp
Regex 
//https://www.w3schools.com/python/python_regex.asp
Custom String Propoerties
//https://docs.python.org/3/library/string.html
Email
//https://docs.python.org/3/library/smtplib.html
//https://www.youtube.com/watch?v=JRCJ6RtE3xU
"""

#TODO
# Add sound effect 
# Add a progress bar
# Add a feature to save the invoice as a PDF and meber ids

def lighter_color(self, color):
    """Return a lighter shade of the given color."""
    rgb = self.hex_to_rgb(color)
    lighter_rgb = tuple(min(255, int(c * 1.2)) for c in rgb)  # Lighten by 20%
    return self.rgb_to_hex(lighter_rgb)
def hex_to_rgb(self, hex_color):
    """Convert HEX color to RGB."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
def rgb_to_hex(self, rgb):
    """Convert RGB to HEX color."""
    return "#{:02x}{:02x}{:02x}".format(*rgb)
class PaintProgramUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        self.title("Paint Program UI")
        self.geometry("800x600")  # Increased the window size to accommodate both sections
        
        self.pages = {}
        self.create_widgets()
        self.color_var = tk.StringVar(value="Red")
        self.water_resistance_var = tk.StringVar(value="Low")
        self.finish_type_var = tk.StringVar(value="Matte")
        load_dotenv()
    def create_widgets(self):
        # Create a notebook (tabbed interface)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=TRUE)
        
        # Create pages
        self.pages['Main'] = ttk.Frame(self.notebook)
        self.pages['Settings'] = ttk.Frame(self.notebook)
        
        # Add pages to notebook
        self.notebook.add(self.pages['Main'], text='Home')
        self.notebook.add(self.pages['Settings'], text='Settings')
        
        # Add widgets to Home page
        self.create_home_page()
        
        # Add widgets to Settings page
        self.create_settings_page()

    def create_home_page(self):
        home_frame = self.pages['Main']
        
        # Add a label
        label = ttk.Label(home_frame, text="Welcome to the Paint Program!", font=("Helvetica", 16, "bold"))
        label.pack(pady=10)
        
        # Add a text entry for name
        name_label = ttk.Label(home_frame, text="Name:")
        name_label.pack(pady=5)
        self.name_entry = ttk.Entry(home_frame, bootstyle="info")
        self.name_entry.pack(pady=5)
        self.name_error_label = ttk.Label(home_frame, text="", foreground="red")
        self.name_error_label.pack(pady=5)
        
        # Add a text entry for number of rooms
        rooms_label = ttk.Label(home_frame, text="Number of Rooms:")
        rooms_label.pack(pady=5)
        self.rooms_entry = ttk.Entry(home_frame, bootstyle="info")
        self.rooms_entry.pack(pady=5)
        self.rooms_error_label = ttk.Label(home_frame, text="", foreground="red")
        self.rooms_error_label.pack(pady=5)
        
        # Add a text entry for email address
        email_label = ttk.Label(home_frame, text="Email Address:")
        email_label.pack(pady=5)
        self.email_entry = ttk.Entry(home_frame, bootstyle="info")
        self.email_entry.pack(pady=5)
        self.email_error_label = ttk.Label(home_frame, text="", foreground="red")
        self.email_error_label.pack(pady=5)
        
        # Add a text entry for age
        age_label = ttk.Label(home_frame, text="Age:")
        age_label.pack(pady=5)
        self.age_entry = ttk.Entry(home_frame, bootstyle="info")
        self.age_entry.pack(pady=5)
        self.age_error_label = ttk.Label(home_frame, text="", foreground="red")
        self.age_error_label.pack(pady=5)
        
        # Add a checkbox for membership
        self.member_var = ttk.BooleanVar()
        member_check = ttk.Checkbutton(home_frame, text="Member", variable=self.member_var, bootstyle="success-round-toggle")
        member_check.pack(pady=5)
        
        # Add a button
        button = ttk.Button(home_frame, text="Submit", command=self.on_button_click, bootstyle="success")
        button.pack(pady=10)  

    def create_settings_page(self):
        settings_frame = self.pages['Settings']
        
    
        # Add member-specific content
        self.member_content_frame = ttk.Frame(settings_frame)
        self.member_content_frame.pack(pady=10)
        self.update_member_content()
    
    
    def contact_support(self):
        # Implement the logic to contact support
        support_message = self.support_entry.get().strip()
        if support_message:
            messagebox.showinfo("Support", f"Support request sent: {support_message}")
        else:
            messagebox.showwarning("Support", "Please enter a message for support.")
    def create_room_page(self):
        if 'Rooms' in self.pages:
            room_frame = self.pages['Rooms']
            for widget in room_frame.winfo_children():
                widget.destroy()
        else:
            room_frame = ttk.Frame(self)
            self.pages['Rooms'] = room_frame
            notebook = self.nametowidget(self.winfo_children()[0])
            notebook.add(room_frame, text='Rooms')
    
        # Add a label
        label = ttk.Label(room_frame, text="Enter the dimensions of each wall", font=("Helvetica", 16, "bold"))
        label.grid(row=0, column=0, columnspan=8, pady=10)
    
        # Get the number of rooms
        try:
            num_rooms = int(self.rooms_entry.get().strip())
        except ValueError:
            self.rooms_error_label.config(text="Please enter a valid number of rooms (1-5).")
            return
    
        self.wall_entries = {}
        self.square_footage_labels = {}
    
        row_left = 1
        row_right = 1
        col_offset = 0
    
        def validate_input(event, entry):
            """Validate input and change background color accordingly"""
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
    
        for room in range(1, num_rooms + 1):
            if room > 3:
                col_offset = 9  # Move to the right side for rooms 4 and above with a horizontal offset of 5
                if room == 4:
                    row_right = 1  # Reset row for the right side
    
            current_row = row_left if room <= 3 else row_right
    
            room_label = ttk.Label(room_frame, text=f"Room {room}", font=("Helvetica", 14, "bold"))
            room_label.grid(row=current_row, column=col_offset, columnspan=4, pady=10)
            current_row += 1
    
            self.wall_entries[room] = []
            self.square_footage_labels[room] = ttk.Label(room_frame, text="Square Footage: 0", font=("Helvetica", 12))
            self.square_footage_labels[room].grid(row=current_row, column=col_offset + 4, pady=5, padx=5, sticky=tk.W)
    
            for wall in range(1, 5):
                wall_length_label = ttk.Label(room_frame, text=f"Wall {wall} Length:")
                wall_length_label.grid(row=current_row, column=col_offset, pady=5, padx=5, sticky=tk.W)
                wall_length_entry = ttk.Entry(room_frame, bootstyle="info")
                wall_length_entry.grid(row=current_row, column=col_offset + 1, pady=5, padx=5)
                # Bind validation to entry
                wall_length_entry.bind('<KeyRelease>', lambda e, entry=wall_length_entry: validate_input(e, entry))
                self.wall_entries[room].append(wall_length_entry)
    
                wall_width_label = ttk.Label(room_frame, text=f"Wall {wall} Width:")
                wall_width_label.grid(row=current_row, column=col_offset + 2, pady=5, padx=5, sticky=tk.W)
                wall_width_entry = ttk.Entry(room_frame, bootstyle="info")
                wall_width_entry.grid(row=current_row, column=col_offset + 3, pady=5, padx=5)
                # Bind validation to entry
                wall_width_entry.bind('<KeyRelease>', lambda e, entry=wall_width_entry: validate_input(e, entry))
                self.wall_entries[room].append(wall_width_entry)
    
                current_row += 1
    
            if room <= 3:
                row_left = current_row
            else:
                row_right = current_row
    
        # Determine the row for the submit button
        submit_row = max(row_left, row_right)
    
        # Add a button to submit wall dimensions
        submit_button = ttk.Button(room_frame, text="Submit Wall Dimensions", command=self.on_submit_walls, bootstyle="success")
        submit_button.grid(row=submit_row, column=0, columnspan=8, pady=10)

        def validate_all_inputs():
            """Validate all inputs before submission"""
            all_valid = True
            for room_entries in self.wall_entries.values():
                for entry in room_entries:
                    if not validate_input(None, entry):
                        all_valid = False
            if all_valid:
                self.on_submit_walls()
            else:
                messagebox.showerror("Error", "Please correct the highlighted fields. All dimensions must be positive numbers.")

        # Add a button to submit wall dimensions
        submit_button = ttk.Button(room_frame, text="Submit Wall Dimensions", 
                                command=validate_all_inputs, bootstyle="success")
        submit_button.grid(row=submit_row, column=0, columnspan=8, pady=10)
    def on_submit_walls(self):
        """Validate wall dimensions and highlight invalid entries."""
        valid = True
        for room, entries in self.wall_entries.items():
            for entry in entries:
                entry_value = entry.get().strip()
                if not entry_value.isdigit():
                    entry.config(bootstyle="danger")
                    valid = False
                else:
                    entry.config(bootstyle="info")
    def update_member_content(self):
        # Clear previous member-specific content
        for widget in self.member_content_frame.winfo_children():
            widget.destroy()

        if self.member_var.get():
            member_label = ttk.Label(self.member_content_frame, text="Member Exclusive Content", font=("Helvetica", 14, "bold"))
            member_label.pack(pady=5)

            # Member-exclusive feature 1: Special Discount Code Entry
            discount_label = ttk.Label(self.member_content_frame, text="Enter Discount Code:")
            discount_label.pack(pady=5)
            self.discount_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.discount_entry.pack(pady=5)
            discount_button = ttk.Button(self.member_content_frame, text="Apply Discount", command=self.validate_discount_code, bootstyle="success")
            discount_button.pack(pady=5)

            # Member-exclusive feature 2: Premium Support Contact Form
            support_label = ttk.Label(self.member_content_frame, text="Premium Support Contact:")
            support_label.pack(pady=5)
            self.support_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.support_entry.pack(pady=5)
            support_button = ttk.Button(self.member_content_frame, text="Contact Support", command=self.contact_support, bootstyle="success")
            support_button.pack(pady=5)

            # Member-exclusive feature 3: Discount Combobox
            self.discount_var = tk.StringVar(value="5%")
            discount_options = ["5%", "75%"]
            discount_combobox = ttk.Combobox(self.member_content_frame, values=discount_options, textvariable=self.discount_var, bootstyle="info", state="readonly")
            discount_combobox.pack(pady=5)
            discount_combobox.bind("<<ComboboxSelected>>", self.apply_discount)
    def validate_discount_code(self):
        discount_code = self.discount_entry.get().strip()
        if discount_code == "MRBAWA":
            self.discount_var.set("75%")
            self.apply_discount()
            messagebox.showinfo("Discount", "75% discount applied successfully!")
        else:
            self.discount_var.set("5%")
            self.apply_discount()
            messagebox.showinfo("Discount", "5% member discount applied.")
    def apply_discount(self, event=None):
        discount = self.discount_var.get()
        if discount == "75%":
            self.cost_after_tax = self.cost_before_tax * 0.25
        elif discount == "5%":
            self.cost_after_tax = self.cost_before_tax * 0.95
        self.cost_label_after_tax.config(text=f"Cost After Tax: ${round(self.cost_after_tax, 2)}")

    def add_chatbot_tab(self):
        """Add the ChatBot tab to the notebook."""
        chat_bot_ui = ChatBotUI(self.notebook)
        self.notebook.add(chat_bot_ui, text='ChatBot')
    def create_paint_options_page(self):
        paint_options_frame = ttk.Frame(self)
        self.pages['PaintOptions'] = paint_options_frame
        notebook = self.nametowidget(self.winfo_children()[0])
        notebook.add(paint_options_frame, text='Paint Options')
        # Add a label
        label = ttk.Label(paint_options_frame, text="Select Your Paint", font=("Helvetica", 16, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)
    
        # Paint options
        self.paints = {
            "Custom Paint": 250,
            "Luxury Paint": 200,
            "Designer Paint": 150,
            "Premium Paint": 105,
            "Low Odor Paint": 90,
            "Regular Paint": 75,
            "Value Paint": 40,
        }
    
        self.paint_choice_var = tk.StringVar(value="Custom Paint")
        self.paint_choice_var.trace("w", self.on_paint_selection_change)
    
        row = 1
        for paint, price in self.paints.items():
            ttk.Radiobutton(paint_options_frame, text=f"{paint}: ${price} per gallon", variable=self.paint_choice_var, value=paint).grid(row=row, column=0, sticky=tk.W, pady=5, padx=50)
            row += 1
    
        # Add a button to confirm paint selection
        confirm_button = ttk.Button(paint_options_frame, text="Confirm Paint Selection", command=self.on_confirm_paint, bootstyle="success")
        confirm_button.grid(row=row, column=0, columnspan=2, pady=10)
    def validate_input(self, value, pattern, error_label, error_message):
        if not re.match(pattern, value):
            error_label.config(text=error_message)
            return False
        else:
            error_label.config(text="")
            return True
    def on_button_click(self):
        name = self.name_entry.get().strip()
        rooms = self.rooms_entry.get().strip()
        email = self.email_entry.get().strip()
        age = self.age_entry.get().strip()
        member = self.member_var.get()

        valid = True
        
        # Validate name
        if not self.validate_input(name, r"^[A-Za-z]+$", self.name_error_label, "Please enter a valid name (letters only)."):
            valid = False
        
        # Validate number of rooms
        if not self.validate_input(rooms, r"^[1-5]$", self.rooms_error_label, "Please enter a valid number of rooms (1-5)."):
            valid = False
        
        # Validate email
        if not self.validate_input(email, r"[^@]+@[^@]+\.[^@]+", self.email_error_label, "Please enter a valid email address."):
            valid = False
        
        # Validate age
        if not self.validate_input(age, r"^[1-9][0-9]*$", self.age_error_label, "Please enter a valid age (positive number)."):
            valid = False
        
        if valid:
            print(f"Name: {name}")
            print(f"Number of Rooms: {rooms}")
            print(f"Email Address: {email}")
            print(f"Age: {age}")
            print(f"Member: {member}")
            self.create_room_page()
            self.update_member_content()
            if member:
                self.add_chatbot_tab()
    def on_submit_walls(self):
        wall_dimensions = {}
        total_square_footage = 0
        for room, entries in self.wall_entries.items():
            wall_dimensions[room] = []
            room_square_footage = 0
            for i in range(0, len(entries), 2):
                length = entries[i].get().strip()
                width = entries[i+1].get().strip()
                if length.isdigit() and width.isdigit():
                    length = int(length)
                    width = int(width)
                    wall_dimensions[room].append((length, width))
                    room_square_footage += length * width
                else:
                    print(f"Invalid dimensions for Room {room}, Wall {i//2 + 1}")
                    return
            self.square_footage_labels[room].config(text=f"Square Footage: {room_square_footage}")
            total_square_footage += room_square_footage
        
        # Calculate the number of paint cans needed
        self.paint_cans_needed = math.ceil(total_square_footage / 400)
        
        # Display the total square footage and paint cans needed
        total_label = ttk.Label(self.pages['Rooms'], text=f"Total Square Footage: {total_square_footage}", font=("Helvetica", 12, "bold"))
        total_label.grid(row=len(self.wall_entries) * 6 + 1, column=0, columnspan=4, pady=10)
        
        paint_cans_label = ttk.Label(self.pages['Rooms'], text=f"Paint Cans Needed: {self.paint_cans_needed}", font=("Helvetica", 12, "bold"))
        paint_cans_label.grid(row=len(self.wall_entries) * 6 + 2, column=0, columnspan=4, pady=10)
        
        print(f"Total Square Footage: {total_square_footage}")
        print(f"Paint Cans Needed: {self.paint_cans_needed}")
        print("Wall dimensions:", wall_dimensions)
        
        # Open the paint options page
        self.create_paint_options_page()  
    def on_paint_selection_change(self, *args):
        selected_paint = self.paint_choice_var.get()
        if selected_paint != "Custom Paint" and hasattr(self, 'custom_paint_frame'):
            self.custom_paint_frame.grid_remove()
        elif selected_paint == "Custom Paint" and hasattr(self, 'custom_paint_frame'):
            self.custom_paint_frame.grid()
    def on_confirm_paint(self):
        selected_paint = self.paint_choice_var.get()
        paint_price = self.paints[selected_paint]
        self.paint_cans_needed = int(self.pages['Rooms'].grid_slaves(row=len(self.wall_entries) * 6 + 2, column=0)[0].cget("text").split(":")[1].strip())
        
        # Calculate cost before and after tax
        cost_before_tax = self.paint_cans_needed * paint_price
        cost_after_tax = cost_before_tax * 1.13  # Assuming a tax rate of 13%
        
        # Display the costs
        cost_label_before_tax = ttk.Label(self.pages['PaintOptions'], text=f"Cost Before Tax: ${round(cost_before_tax, 2)}", font=("Helvetica", 12, "bold"))
        cost_label_before_tax.grid(row=len(self.paints) + 2, column=0, columnspan=2, pady=10, padx=50)
        
        cost_label_after_tax = ttk.Label(self.pages['PaintOptions'], text=f"Cost After Tax: ${round(cost_after_tax, 2)}", font=("Helvetica", 12, "bold"))
        cost_label_after_tax.grid(row=len(self.paints) + 3, column=0, columnspan=2, pady=10, padx=50)
        
        print(f"Selected Paint: {selected_paint}")
        print(f"Cost Before Tax: ${round(cost_before_tax, 2)}")
        print(f"Cost After Tax: ${round(cost_after_tax, 2)}")
        
        self.create_custom_paint_panel(selected_paint)
        
        # Pass the costs to the payment page
        self.create_payment_page(cost_before_tax, cost_after_tax)
    def create_custom_paint_panel(self, selected_paint):
        if hasattr(self, 'custom_paint_frame'):
            self.custom_paint_frame.grid_remove()
    
        self.custom_paint_frame = ttk.Frame(self.pages['PaintOptions'])
        self.custom_paint_frame.grid(row=0, column=2, rowspan=len(self.paints) + 4, padx=20, pady=10, sticky=tk.N)
    
        # Add a label for the paint preview
        label = ttk.Label(self.custom_paint_frame, text="Custom Paint Options", font=("Helvetica", 16, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)
    
        # Add a canvas for paint preview
        self.preview_canvas = tk.Canvas(self.custom_paint_frame, width=200, height=300, bg="white")
        self.preview_canvas.grid(row=0, column=2, rowspan=10, padx=10, pady=10)
        
        self.update_paint_preview()
        # Add options for paint color
        color_label = ttk.Label(self.custom_paint_frame, text="Choose Paint Color:")
        color_label.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        self.color_var = tk.StringVar(value="Red")
        color_button = ttk.Button(self.custom_paint_frame, text="Select Color", command=self.choose_color, bootstyle="info")
        color_button.grid(row=1, column=1, pady=5, padx=5)
    
        color_button_confirm = ttk.Button(self.custom_paint_frame, text="Confirm Color", bootstyle="info")
        color_button_confirm.grid(row=2, column=1, pady=5, padx=5)
        color_button_confirm.bind("<ButtonRelease-1>", lambda e: self.update_paint_preview())
        
        # Add options for finish type
        finish_type_label = ttk.Label(self.custom_paint_frame, text="Choose Finish Type:")
        finish_type_label.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        self.finish_type_var = tk.StringVar(value="Matte")
        finish_type_options = ["Matte", "Glossy", "Satin"]
        finish_type_combobox = ttk.Combobox(self.custom_paint_frame, values=finish_type_options, textvariable=self.finish_type_var, bootstyle="info", state="readonly")
        finish_type_combobox.grid(row=3, column=1, pady=5, padx=5)
        finish_type_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_paint_preview())
    
        if selected_paint == "Custom Paint":
            # Add options for water resistance amount
            water_resistance_label = ttk.Label(self.custom_paint_frame, text="Water Resistance Amount:")
            water_resistance_label.grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
            self.water_resistance_var = tk.StringVar(value="Low")
            water_resistance_options = ["Low", "Medium", "High"]
            water_resistance_combobox = ttk.Combobox(self.custom_paint_frame, values=water_resistance_options, textvariable=self.water_resistance_var, bootstyle="info", state="readonly")
            water_resistance_combobox.grid(row=4, column=1, pady=5, padx=5)
            water_resistance_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_paint_preview())
        
            # Add options for durability level
            durability_label = ttk.Label(self.custom_paint_frame, text="Choose Durability Level:")
            durability_label.grid(row=5, column=0, pady=5, padx=5, sticky=tk.W)
            self.durability_var = tk.StringVar(value="Standard")
            durability_options = ["Standard", "Premium", "Ultra"]
            durability_combobox = ttk.Combobox(self.custom_paint_frame, values=durability_options, textvariable=self.durability_var, bootstyle="info")
            durability_combobox.grid(row=5, column=1, pady=5, padx=5)
        
            # Add options for UV protection level
            uv_protection_label = ttk.Label(self.custom_paint_frame, text="UV Protection Level:")
            uv_protection_label.grid(row=6, column=0, pady=5, padx=5, sticky=tk.W)
            self.uv_protection_var = tk.StringVar(value="Low")
            uv_protection_options = ["Low", "Medium", "High"]
            uv_protection_combobox = ttk.Combobox(self.custom_paint_frame, values=uv_protection_options, textvariable=self.uv_protection_var, bootstyle="info")
            uv_protection_combobox.grid(row=6, column=1, pady=5, padx=5)
        
            # Add options for scratch resistance
            scratch_resistance_label = ttk.Label(self.custom_paint_frame, text="Scratch Resistance:")
            scratch_resistance_label.grid(row=7, column=0, pady=5, padx=5, sticky=tk.W)
            self.scratch_resistance_var = tk.StringVar(value="Low")
            scratch_resistance_options = ["Low", "Medium", "High"]
            scratch_resistance_combobox = ttk.Combobox(self.custom_paint_frame, values=scratch_resistance_options, textvariable=self.scratch_resistance_var, bootstyle="info")
            scratch_resistance_combobox.grid(row=7, column=1, pady=5, padx=5)
        
            # Add options for eco-friendly
            eco_friendly_label = ttk.Label(self.custom_paint_frame, text="Eco-Friendly:")
            eco_friendly_label.grid(row=8, column=0, pady=5, padx=5, sticky=tk.W)
            self.eco_friendly_var = tk.StringVar(value="No")
            eco_friendly_options = ["No", "Yes"]
            eco_friendly_combobox = ttk.Combobox(self.custom_paint_frame, values=eco_friendly_options, textvariable=self.eco_friendly_var, bootstyle="info")
            eco_friendly_combobox.grid(row=8, column=1, pady=5, padx=5)
        
            # Add options for drying time
            drying_time_label = ttk.Label(self.custom_paint_frame, text="Drying Time (hours):")
            drying_time_label.grid(row=9, column=0, pady=5, padx=5, sticky=tk.W)
            self.drying_time_var = tk.StringVar(value="1")
            drying_time_entry = ttk.Entry(self.custom_paint_frame, textvariable=self.drying_time_var, bootstyle="info")
            drying_time_entry.grid(row=9, column=1, pady=5, padx=5)
        
            # Add options for coverage per gallon
            coverage_label = ttk.Label(self.custom_paint_frame, text="Coverage per Gallon (sq ft):")
            coverage_label.grid(row=10, column=0, pady=5, padx=5, sticky=tk.W)
            self.coverage_var = tk.StringVar(value="400")
            coverage_entry = ttk.Entry(self.custom_paint_frame, textvariable=self.coverage_var, bootstyle="info")
            coverage_entry.grid(row=10, column=1, pady=5, padx=5)
        
            # Add options for VOC level
            voc_label = ttk.Label(self.custom_paint_frame, text="VOC Level (g/L):")
            voc_label.grid(row=11, column=0, pady=5, padx=5, sticky=tk.W)
            self.voc_var = tk.StringVar(value="50")
            voc_entry = ttk.Entry(self.custom_paint_frame, textvariable=self.voc_var, bootstyle="info")
            voc_entry.grid(row=11, column=1, pady=5, padx=5)
    
        # Add a button to confirm custom paint options
        confirm_custom_paint_button = ttk.Button(self.custom_paint_frame, text="Confirm Custom Paint Options", command=self.on_confirm_custom_paint, bootstyle="success")
        confirm_custom_paint_button.grid(row=12, column=0, columnspan=2, pady=10)    
    def choose_color(self):
        color_code = colorchooser.askcolor(title="Choose color")[1]
        if color_code:
            self.color_var.set(color_code)
            print(f"Selected Color: {color_code}")  
    def update_paint_preview(self):
        """Update the paint preview based on selected options."""
        # Clear previous preview
        self.preview_canvas.delete("all")

        # Get the selected color and finish type
        selected_color = self.color_var.get() if self.color_var.get() != "Red" else "#FF0000"  # Default Red
        selected_finish_type = self.finish_type_var.get()
        
        # Draw a rectangle to represent the paint
        self.preview_canvas.create_rectangle(20, 20, 180, 280, fill=selected_color, outline="")

        # Add effects based on finish type
        if selected_finish_type == "Glossy":
            # Simulate gloss with white highlights
            self.preview_canvas.create_line(20, 20, 180, 100, fill="white", width=5)
        elif selected_finish_type == "Satin":
            # Add some sheen with a lighter shade
            lighter_color = self.lighter_color(selected_color)
            self.preview_canvas.create_rectangle(20, 20, 180, 280, fill=lighter_color, outline="")
    def on_confirm_custom_paint(self):
        selected_color = self.color_var.get()
        selected_water_resistance = self.water_resistance_var.get()
        selected_finish_type = self.finish_type_var.get()
        selected_durability = self.durability_var.get()

        print(f"Selected Color: {selected_color}")
        print(f"Selected Water Resistance: {selected_water_resistance}")
        print(f"Selected Finish Type: {selected_finish_type}")
        print(f"Selected Durability: {selected_durability}")
        self.create_payement_page()
    def create_payment_page(self, cost_before_tax, cost_after_tax):
        payment_frame = ttk.Frame(self)
        self.pages['Payment'] = payment_frame
        notebook = self.nametowidget(self.winfo_children()[0])
        notebook.add(payment_frame, text='Payment')
        
        # Add a label
        label = ttk.Label(payment_frame, text="Select Your Payment Method", font=("Helvetica", 16, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Display the costs
        self.cost_before_tax = cost_before_tax
        self.cost_after_tax = cost_after_tax
        self.cost_label_before_tax = ttk.Label(payment_frame, text=f"Cost Before Tax: ${round(cost_before_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_before_tax.grid(row=1, column=0, columnspan=2, pady=10, padx=50)
        
        self.cost_label_after_tax = ttk.Label(payment_frame, text=f"Cost After Tax: ${round(cost_after_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_after_tax.grid(row=2, column=0, columnspan=2, pady=10, padx=50)
        
        # Discount options (only for members)
        if self.member_var.get():
            discount_frame = ttk.Frame(payment_frame)
            discount_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
            
            discount_label = ttk.Label(discount_frame, text="Select Discount:", font=("Helvetica", 12))
            discount_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
            
            self.discount_var = tk.StringVar(value="5%")
            discount_options = ["5%", "75%"]
            discount_combobox = ttk.Combobox(discount_frame, values=discount_options, textvariable=self.discount_var, bootstyle="info", state="readonly")
            discount_combobox.grid(row=0, column=1, pady=5, padx=5)
            discount_combobox.bind("<<ComboboxSelected>>", self.apply_discount)
            row = 4
        else:
            row = 3
        
        # Payment options
        payment_frame_inner = ttk.Frame(payment_frame)
        payment_frame_inner.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        
        payment_options = {
            "Credit Card": "Visa, MasterCard, American Express",
            "Cash": "Cash payment",
            "Check": "Check payment",
            "PayPal": "PayPal account",
        }
        
        self.payment_choice_var = tk.StringVar(value="Credit Card")
        
        for payment, description in payment_options.items():
            ttk.Radiobutton(payment_frame_inner, text=f"{payment}: {description}", variable=self.payment_choice_var, value=payment).grid(row=row, column=0, sticky=tk.W, pady=5, padx=50)
            row += 1
        
        # Add a number input field for the payment amount
        amount_frame = ttk.Frame(payment_frame)
        amount_frame.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        
        amount_label = ttk.Label(amount_frame, text="Enter Payment Amount:", font=("Helvetica", 12))
        amount_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        
        self.amount_entry = ttk.Entry(amount_frame, bootstyle="info")
        self.amount_entry.grid(row=0, column=1, pady=5, padx=5)
        row += 1
        
        # Add a button to confirm payment amount
        button_frame = ttk.Frame(payment_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        # Add a button to confirm amount and payment selection
        confirm_button = ttk.Button(button_frame, text="Confirm Payment", command=lambda: [self.on_confirm_amount(self.cost_after_tax), self.on_confirm_payment()], bootstyle="success")
        confirm_button.grid(row=0, column=0, pady=10, padx=5, sticky=tk.W)
        
        # Add a frame to display the change
        self.change_frame = ttk.Frame(payment_frame)
        self.change_frame.grid(row=row + 1, column=0, columnspan=2, pady=10, padx=5)
    def apply_discount(self, event):
        discount_percentage = int(self.discount_var.get().strip('%'))
        discount_amount = self.cost_before_tax * (discount_percentage / 100)
        discounted_cost_before_tax = self.cost_before_tax - discount_amount
        self.cost_after_tax = discounted_cost_before_tax * 1.13  # Assuming a tax rate of 13%
        
        # Update the displayed costs
        self.cost_label_before_tax.config(text=f"Cost Before Tax: ${round(discounted_cost_before_tax, 2)}")
        self.cost_label_after_tax.config(text=f"Cost After Tax: ${round(self.cost_after_tax, 2)}")
    def on_confirm_amount(self, cost_after_tax):
        try:
            self.entered_amount = float(self.amount_entry.get().strip())
            if self.entered_amount >= cost_after_tax:
                print("Payment is sufficient.")
                change = self.entered_amount - cost_after_tax
                self.process_change(change)
            else:
                print("Entered amount is not sufficient.")
                messagebox.showerror("Error", "Entered amount is not sufficient.")
        except ValueError:
            print("Invalid amount entered.")
            messagebox.showerror("Error", "Invalid amount entered.")
    def process_change(self, difference):
        money_map = {
            50: "Fifty Dollar bills",
            20: "Twenty Dollar bills",
            10: "Ten Dollar bills",
            5: "Five Dollar bills",
            2: "Toonies",
            1: "Loonies",
            0.25: "Quarters",
            0.10: "Dimes",
            0.05: "Nickels",
            0.01: "Pennies",
        }
        change = {}
        for value, name in money_map.items():
            count = int(difference // value)
            if count > 0:
                change[name] = count
                difference = round(difference - count * value, 2)
        
        # Ensure change_frame is initialized
        if not hasattr(self, 'change_frame'):
            self.change_frame = ttk.Frame(self.pages['Payment'])
            self.change_frame.grid(row=10, column=0, columnspan=2, pady=10, padx=5)
        
        # Clear previous change display
        for widget in self.change_frame.winfo_children():
            widget.destroy()
        
        # Display the change
        ttk.Label(self.change_frame, text="Here is your change:", font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        row = 1
        for name, count in change.items():
            ttk.Label(self.change_frame, text=f"{name}: {count}", font=("Helvetica", 12)).grid(row=row, column=0, columnspan=2, pady=2)
            row += 1
    def on_confirm_payment(self):
        selected_payment_method = self.payment_choice_var.get()
        messagebox.showinfo("Payment Confirmation", f"Payment method '{selected_payment_method}' selected.")
        self.send_email_receipt()
    def send_email_receipt(self):
        if self.entered_amount >= self.cost_after_tax:
            # Collect the email address entered by the user
            recipient_email = self.email_entry.get().strip()
            
            # Generate the receipt content
            name = self.name_entry.get().strip()
            date_str = datetime.now().strftime("%Y-%m-%d")
            paint_choice = self.paint_choice_var.get()
            amount_of_paint = self.paint_cans_needed
            paint_cost = self.paints[paint_choice]
            subtotal = round(self.cost_before_tax, 2)
            tax = round(self.cost_after_tax - self.cost_before_tax, 2)
            total = round(self.cost_after_tax, 2)
            subject = "Paint Order Receipt"
            custom_details = f"Color: {self.color_var.get()}, Finish: {self.finish_type_var.get()}"
            
            receipt = f"""
            *****************************************************
            SIR MIXALOT PAINT
            5353 Fake street, Burlington ON, N4C 4M2
            invoice #: {randint(100000, 999999)}
            Receiver Name: {name}
            Date: {date_str}
            Description: {paint_choice if paint_choice == "Custom Paint" else paint_choice}
            Quantity: {amount_of_paint}
            Price per gallon: ${paint_cost}
            Subtotal: ${subtotal}
            Tax (13%): ${tax}
            Total: ${total}
                Custom Properties:
                    {custom_details}
            Balance Due: $0.00
            Thank you for your business!
            *****************************************************
            """

            # Email credentials and SMTP server details
            sender_email = os.getenv("SENDER_EMAIL")
            sender_password = os.getenv("SENDER_PASSWORD")
            smtp_server = "smtp.gmail.com"
            smtp_port = 587

            # Create the email message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient_email
            msg['Subject'] = subject
            msg.attach(MIMEText(receipt, 'plain'))

            try:
                # Connect to the SMTP server and send the email
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())
                server.quit()
                messagebox.showinfo("Email Sent", "The receipt has been sent to your email address.")
            except Exception as e:
                messagebox.showerror("Email Error", f"Failed to send email: {e}")
    def contact_support(self):
        # Implement the logic to contact support
        support_message = self.support_entry.get().strip()
        if support_message:
            try:
                # Email configuration
                sender_email = "your_email@gmail.com"
                receiver_email = "support_email@example.com"
                password = "your_email_password"

                # Create the email content
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = "Support Request from Member"
                body = f"Support request message:\n\n{support_message}"
                message.attach(MIMEText(body, "plain"))

                # Connect to the Gmail SMTP server and send the email
                server = smtplib.SMTP("smtp.gmail.com", 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
                server.quit()

                messagebox.showinfo("Support", "Support request sent successfully.")
            except Exception as e:
                messagebox.showerror("Support", f"Failed to send support request: {e}")
        else:
            messagebox.showwarning("Support", "Please enter a message for support.")

class ChatBotAI:
    def __init__(self):
        """Initialize the ChatBotAI instance."""
        load_dotenv()
        
    def get_response(self, user_message):
        """Generate a response based on user input."""
        if "hello" in user_message.lower():
            return "Hello! How can I assist you today?"
        elif "help" in user_message.lower():
            return "I'm here to help! What do you need assistance with?"
        elif "bye" in user_message.lower():
            return "Goodbye! Have a great day."
        elif user_message.strip():
            return self.get_api_response(user_message).json().get("response", "Sorry, I couldn't fetch a response.")
        else:
            return "I'm not sure how to respond to that. Could you rephrase?"

    def get_api_response(self, response):
        """Get a response from an API."""
        url = "https://chatgpt-gpt4-ai-chatbot.p.rapidapi.com/ask"
        payload = {"query": response}
        headers = {
            "x-rapidapi-key": os.getenv("API_KEY"),
            "x-rapidapi-host": "chatgpt-gpt4-ai-chatbot.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response if response.ok else self.loading_response()

    def loading_response(self):
        """Generate a loading response."""
        return "Please wait a moment while I process your request..."

class ChatBotUI(ttk.Frame):
    def __init__(self, root):
        """Initialize ChatBotUI with a reference to the parent widget and ChatBotAI instance."""
        super().__init__(root)
        self.root = root
        self.chat_bot_ai = ChatBotAI()
        self.create_chat_interface()

    def create_chat_interface(self):
        """Create a simple chat interface with essential components."""
        # Configure grid layout to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Chat history display
        self.chat_history_text = tk.Text(self, height=20, wrap=tk.WORD, state=tk.DISABLED,
                                         bg="#1D1E33", fg="#E5E5E5", font=("Helvetica", 12), padx=10, pady=10)
        self.chat_history_text.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Scrollbar for chat history
        scrollbar = ttk.Scrollbar(self, command=self.chat_history_text.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.chat_history_text['yscrollcommand'] = scrollbar.set

        # Message entry field
        self.message_entry = ttk.Entry(self, width=50, font=("Helvetica", 12))
        self.message_entry.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        # Send button
        send_button = ttk.Button(self, text="Send", command=self.on_send_message)
        send_button.grid(row=1, column=1, padx=5, pady=10)

        # Allow pressing Enter to send message
        self.message_entry.bind("<Return>", lambda event: self.on_send_message())

        # Add tags for styling messages
        self.chat_history_text.tag_configure("user", foreground="#007BFF", justify="right", lmargin1=10, lmargin2=10)
        self.chat_history_text.tag_configure("bot", foreground="#28A745", justify="left", lmargin1=10, lmargin2=10)

        # Add welcome message
        self.display_message("Bot", "Welcome! How can I assist you today?", "bot")

    def on_send_message(self):
        """Send the user's message and display the chatbot's response."""
        user_message = self.message_entry.get().strip()
        if user_message:
            self.display_message("You", user_message, "user")
            bot_response = self.chat_bot_ai.get_response(user_message)
            self.display_message("Bot", bot_response, "bot")
        self.message_entry.delete(0, tk.END)

    def display_message(self, sender, message, tag):
        """Display a message in the chat history with simple styling."""
        self.chat_history_text.config(state=tk.NORMAL)
        self.chat_history_text.insert(tk.END, f"{sender}: {message}\n\n", tag)
        self.chat_history_text.config(state=tk.DISABLED)
        self.chat_history_text.yview(tk.END)

if __name__ == "__main__":
    app = PaintProgramUI()
    app.mainloop()