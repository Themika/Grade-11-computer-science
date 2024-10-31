import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

translations = {
    "English": {
        "select_language": "Select Language:",
        "select_theme": "Select Theme:",
        "font_size": "Select Font Size:",
        "volume_label": "Adjust Volume:",
        "enable_feature": "Enable Feature",
        "member_exclusive_content": "Member Exclusive Content",
        "enter_discount_code": "Enter Discount Code:",
        "apply_discount": "Apply Discount",
        "premium_support_contact": "Premium Support Contact:",
        "contact_support": "Contact Support"
    },
    "French": {
        "select_language": "Choisir la langue:",
        "select_theme": "Choisir le thème:",
        "font_size": "Choisir la taille de police:",
        "volume_label": "Ajuster le volume:",
        "enable_feature": "Activer la fonctionnalité",
        "member_exclusive_content": "Contenu exclusif pour les membres",
        "enter_discount_code": "Entrer le code de réduction:",
        "apply_discount": "Appliquer la réduction",
        "premium_support_contact": "Contact de support premium:",
        "contact_support": "Contacter le support"
    }
}
class SettingsPage(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.language = controller.current_language
        self.member_content_frame = ttk.Frame(self)
        self.member_content_frame.pack(pady=10)

        self.create_widgets()
        self.update_member_content()

    def create_widgets(self):
        print("Creating settings page widgets")

        # Language Selection
        self.language_label = ttk.Label(self, text=translations[self.language]["select_language"], bootstyle="info")
        self.language_label.pack(pady=5)
        languages = ["English", "French"]
        self.language_combobox = ttk.Combobox(self, values=languages, bootstyle="info")
        self.language_combobox.pack(pady=5)
        self.language_combobox.set(self.language)  # Set default language
        self.language_combobox.bind("<<ComboboxSelected>>", self.change_language)

        # Theme Selection
        self.theme_label = ttk.Label(self, text=translations[self.language]["select_theme"], bootstyle="info")
        self.theme_label.pack(pady=5)
        themes = ["darkly", "solar", "superhero", "cyborg", "vapor", "cosmo", "flatly", "journal", "litera", "lumen", "minty", "yeti"]
        self.theme_combobox = ttk.Combobox(self, values=themes, bootstyle="info")
        self.theme_combobox.pack(pady=5)
        self.theme_combobox.set("darkly")
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)

        # Font Size
        self.font_size_label = ttk.Label(self, text=translations[self.language]["font_size"], bootstyle="info")
        self.font_size_label.pack(pady=5)
        self.font_size_var = ttk.IntVar(value=12)
        font_size_spinbox = ttk.Spinbox(
            self, from_=8, to=32, textvariable=self.font_size_var, bootstyle="info", 
            command=self.adjust_font_size
        )
        font_size_spinbox.pack(pady=5)

        # Checkbox
        self.checkbox_var = ttk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self, text=translations[self.language]["enable_feature"], variable=self.checkbox_var, bootstyle="info-round-toggle")
        self.checkbox.pack(pady=10)

        # Slider
        self.slider_var = ttk.IntVar(value=50)
        self.slider_label = ttk.Label(self, text=translations[self.language]["volume_label"], bootstyle="info")
        self.slider_label.pack(pady=5)
        self.slider = ttk.Scale(self, from_=0, to=100, variable=self.slider_var, bootstyle="info")
        self.slider.pack(pady=5)

        self.update_member_content()

    def change_language(self, event):
        selected_language = self.language_combobox.get()
        self.controller.change_language(selected_language)  # Update language in main controller
        self.update_language(selected_language)

    def change_theme(self, event):
        selected_theme = self.theme_combobox.get()
        self.controller.set_theme(selected_theme)

    def adjust_font_size(self):
        font_size = self.font_size_var.get()
        self.controller.update_font_size(font_size)

    def update_language(self, language):
        self.language = language
        self.language_label.config(text=translations[language]["select_language"])
        self.theme_label.config(text=translations[language]["select_theme"])
        self.font_size_label.config(text=translations[language]["font_size"])
        self.checkbox.config(text=translations[language]["enable_feature"])
        self.slider_label.config(text=translations[language]["volume_label"])
        self.update_member_content()

    def update_member_content(self):
        for widget in self.member_content_frame.winfo_children():
            widget.destroy()

        if self.controller.member_var.get():
            member_label = ttk.Label(self.member_content_frame, text=translations[self.language]["member_exclusive_content"], font=("Helvetica", 14, "bold"))
            member_label.pack(pady=5)

            discount_label = ttk.Label(self.member_content_frame, text=translations[self.language]["enter_discount_code"])
            discount_label.pack(pady=5)
            self.discount_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.discount_entry.pack(pady=5)
            discount_button = ttk.Button(self.member_content_frame, text=translations[self.language]["apply_discount"], command=self.controller.validate_discount_code, bootstyle="success")
            discount_button.pack(pady=5)

            support_label = ttk.Label(self.member_content_frame, text=translations[self.language]["premium_support_contact"])
            support_label.pack(pady=5)
            self.support_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.support_entry.pack(pady=5)
            support_button = ttk.Button(self.member_content_frame, text=translations[self.language]["contact_support"], command=self.controller.contact_support, bootstyle="success")
            support_button.pack(pady=5)