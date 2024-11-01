import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from utils.validation_utils import validate_input
# Translations for different languages
translations = {
    "English": {
        "welcome_label": "Welcome to the Paint Program!",
        "name_label": "First Name:",
        "rooms_label": "Number of Rooms:",
        "email_label": "Email Address:",
        "age_label": "Age:",
        "member_check": "Member",
        "submit_button": "Submit"
    },
    "French": {
        "welcome_label": "Bienvenue dans le programme de peinture!",
        "name_label": "Prénom:",
        "rooms_label": "Nombre de chambres:",
        "email_label": "Adresse e-mail:",
        "age_label": "Âge:",
        "member_check": "Membre",
        "submit_button": "Soumettre"
    }
}

class HomePage(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        self.language = parent.current_language  

        self.create_widgets()

    def create_widgets(self):
        # Static labels without translation
        """Entry Fields for user data. Validates input and stores data in the parent class."""
        self.welcome_label = ttk.Label(self, text=translations[self.language]["welcome_label"], font=("Helvetica", 16, "bold"))
        self.welcome_label.pack(pady=10)
        # Name Entry
        self.name_label = ttk.Label(self, text=translations[self.language]["name_label"])
        self.name_label.pack(pady=5)
        self.name_entry = ttk.Entry(self, bootstyle="info")
        self.name_entry.pack(pady=5)
        self.name_error_label = ttk.Label(self, text="", foreground="red")
        self.name_error_label.pack(pady=5)
        # Rooms Entry
        self.rooms_label = ttk.Label(self, text=translations[self.language]["rooms_label"])
        self.rooms_label.pack(pady=5)
        self.rooms_entry = ttk.Entry(self, bootstyle="info")
        self.rooms_entry.pack(pady=5)
        self.rooms_error_label = ttk.Label(self, text="", foreground="red")
        self.rooms_error_label.pack(pady=5)
        # Email Entry
        self.email_label = ttk.Label(self, text=translations[self.language]["email_label"])
        self.email_label.pack(pady=5)
        self.email_entry = ttk.Entry(self, bootstyle="info")
        self.email_entry.pack(pady=5)
        self.email_error_label = ttk.Label(self, text="", foreground="red")
        self.email_error_label.pack(pady=5)
        # Age Entry
        self.age_label = ttk.Label(self, text=translations[self.language]["age_label"])
        self.age_label.pack(pady=5)
        self.age_entry = ttk.Entry(self, bootstyle="info")
        self.age_entry.pack(pady=5)
        self.age_error_label = ttk.Label(self, text="", foreground="red")
        self.age_error_label.pack(pady=5)
        # Member Check
        self.member_check = ttk.Checkbutton(self, text=translations[self.language]["member_check"], variable=self.parent.member_var, bootstyle="success-round-toggle")
        self.member_check.pack(pady=5)
        # Submit Button
        self.submit_button = ttk.Button(self, text=translations[self.language]["submit_button"], command=self.on_button_click, bootstyle="success")
        self.submit_button.pack(pady=10)

    def update_language(self, language):
        """Update all labels to the selected language."""
        self.language = language
        # Update all labels with new language
        self.welcome_label.config(text=translations[language]["welcome_label"])
        self.name_label.config(text=translations[language]["name_label"])
        self.rooms_label.config(text=translations[language]["rooms_label"])
        self.email_label.config(text=translations[language]["email_label"])
        self.age_label.config(text=translations[language]["age_label"])
        self.member_check.config(text=translations[language]["member_check"])
        self.submit_button.config(text=translations[language]["submit_button"])

    def on_button_click(self):
        # Get user data from entry fields
        name = self.name_entry.get().strip()
        rooms = self.rooms_entry.get().strip()
        email = self.email_entry.get().strip()
        age = self.age_entry.get().strip()
        member = self.parent.member_var.get()
        # Validate user data
        valid = True
        # Validate input and show error messages if invalid
        if not validate_input(name, r"^[A-Za-z]+$", self.name_error_label, "Please enter a valid name (letters only)."):
            valid = False
        # Validate input and show error messages if invalid
        if not validate_input(rooms, r"^[1-5]$", self.rooms_error_label, "Please enter a valid number of rooms (1-5)."):
            valid = False
        # Validate input and show error messages if invalid
        if not validate_input(email, r"[^@]+@[^@]+\.[^@]+", self.email_error_label, "Please enter a valid email address."):
            valid = False
        # Validate input and show error messages if invalid
        if not validate_input(age, r"^[1-9][0-9]*$", self.age_error_label, "Please enter a valid age (positive number)."):
            valid = False
        # Proceed if all input is valid
        if valid:
            if int(age) < 16:
                messagebox.showerror("Age Restriction", "You must be 18 or older to use this program. Please get an adult to proceed.")
                self.parent.quit()  # Exit the program
                return
            # Print user
            print(f"Name: {name}")
            print(f"Number of Rooms: {rooms}")
            print(f"Email Address: {email}")
            print(f"Age: {age}")
            print(f"Member: {member}")
            
            # Store user data in the parent class
            self.parent.user_data = {
                "name": name,
                "rooms": rooms,
                "email": email,
                "age": age,
                "member": member
            }
            # Create the next pages
            self.parent.create_room_page(int(rooms))
            self.parent.create_settings_page()
            if member:
                self.parent.add_chatbot_tab()