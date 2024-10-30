import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

translations = {
    "English": {
        "welcome_label": "Welcome to the Paint Program!",
        "name_label": "Name:",
        "rooms_label": "Number of Rooms:",
        "email_label": "Email Address:",
        "age_label": "Age:",
        "member_check": "Member",
        "submit_button": "Submit",
        "select_language": "Select Language:",
        "select_theme": "Select Theme:",
        "font_size": "Select Font Size:",
        "volume_label": "Adjust Volume:"
    },
    "French": {
        "welcome_label": "Bienvenue au programme de peinture!",
        "name_label": "Nom:",
        "rooms_label": "Nombre de chambres:",
        "email_label": "Adresse électronique:",
        "age_label": "Âge:",
        "member_check": "Membre",
        "submit_button": "Soumettre",
        "select_language": "Choisir la langue:",
        "select_theme": "Choisir le thème:",
        "font_size": "Choisir la taille de police:",
        "volume_label": "Ajuster le volume:"
    }
}

class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.member_content_frame = ttk.Frame(self)
        self.member_content_frame.pack(pady=10)

        self.create_widgets()
        self.parent = parent
        self.update_member_content()

    def create_widgets(self):
        print("Creating settings page widgets")

        # Language Selection
        self.language_label = ttk.Label(self, text=translations["English"]["select_language"], bootstyle="info")
        self.language_label.pack(pady=5)
        languages = ["English", "French"]
        self.language_combobox = ttk.Combobox(self, values=languages, bootstyle="info")
        self.language_combobox.pack(pady=5)
        self.language_combobox.set("English")  # Set default language to English
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)

        # Theme Selection
        self.theme_label = ttk.Label(self, text="Select Theme:", bootstyle="info")
        self.theme_label.pack(pady=5)
        themes = ["darkly", "solar", "superhero", "cyborg", "vapor", "cosmo", "flatly", "journal", "litera", "lumen", "minty", "yeti"]
        self.theme_combobox = ttk.Combobox(self, values=themes, bootstyle="info")
        self.theme_combobox.pack(pady=5)
        self.theme_combobox.set("darkly")
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)

        # Font Size
        self.font_size_label = ttk.Label(self, text="Select Font Size:", bootstyle="info")
        self.font_size_label.pack(pady=5)
        self.font_size_var = ttk.IntVar(value=12)
        font_size_spinbox = ttk.Spinbox(
            self, from_=8, to=32, textvariable=self.font_size_var, bootstyle="info", 
            command=self.adjust_font_size
        )
        font_size_spinbox.pack(pady=5)

        # Checkbox
        self.checkbox_var = ttk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self, text="Enable Feature", variable=self.checkbox_var, bootstyle="info-round-toggle")
        self.checkbox.pack(pady=10)

        # Slider
        self.slider_var = ttk.IntVar(value=50)
        self.slider_label = ttk.Label(self, text="Adjust Volume:", bootstyle="info")
        self.slider_label.pack(pady=5)
        self.slider = ttk.Scale(self, from_=0, to=100, variable=self.slider_var, bootstyle="info")
        self.slider.pack(pady=5)

        self.update_member_content()

    def change_language(self, event):
        selected_language = self.language_combobox.get()
        self.controller.language = selected_language  # Update language in main controller
        self.controller.pages['Home'].update_language(selected_language)  # Update HomePage

    def change_theme(self, event):
        selected_theme = self.theme_combobox.get()
        self.controller.set_theme(selected_theme)

    def adjust_font_size(self):
        font_size = self.font_size_var.get()
        self.controller.update_font_size(font_size)

    def update_member_content(self):
        for widget in self.member_content_frame.winfo_children():
            widget.destroy()

        if self.controller.member_var.get():
            member_label = ttk.Label(self.member_content_frame, text="Member Exclusive Content", font=("Helvetica", 14, "bold"))
            member_label.pack(pady=5)

            discount_label = ttk.Label(self.member_content_frame, text="Enter Discount Code:")
            discount_label.pack(pady=5)
            self.discount_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.discount_entry.pack(pady=5)
            discount_button = ttk.Button(self.member_content_frame, text="Apply Discount", command=self.controller.validate_discount_code, bootstyle="success")
            discount_button.pack(pady=5)

            support_label = ttk.Label(self.member_content_frame, text="Premium Support Contact:")
            support_label.pack(pady=5)
            self.support_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.support_entry.pack(pady=5)
            support_button = ttk.Button(self.member_content_frame, text="Contact Support", command=self.controller.contact_support, bootstyle="success")
            support_button.pack(pady=5)
