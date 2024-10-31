import ttkbootstrap as ttk
import os
import tkinter as tk

from ttkbootstrap.constants import *
from tkinter import messagebox
from dotenv import load_dotenv
from utils.email_utils import send_email
# Translations for different languages
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
        "contact_support": "Contact Support",
        "support": "Support",
        "only_members_support": "Only members can contact support.",
        "enter_support_message": "Please enter a message for support.",
        "support_request_sent": "Support request sent successfully.",
        "failed_to_send_support": "Failed to send support request",
        "support_request": "Support Request",
        "support_request_message": "Support Request Message",
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
        "contact_support": "Contacter le support",
        "support": "Support",
        "only_members_support": "Seuls les membres peuvent contacter le support.",
        "failed_to_send_support": "Échec de l'envoi de la demande de support",
        "support_request": "Demande de support",
        "support_request_message": "Message de demande de support",
        "support_request_sent": "Demande de support envoyée avec succès.",
        "failed_to_send_support": "Échec de l'envoi de la demande de support",
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
        load_dotenv()
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
        # Available themes
        themes = ["darkly", "solar", "superhero", "cyborg", "vapor", "cosmo", "flatly", "journal", "litera", "lumen", "minty", "yeti"]
        self.theme_combobox = ttk.Combobox(self, values=themes, bootstyle="info")
        # Set default theme
        self.theme_combobox.pack(pady=5)
        self.theme_combobox.set("darkly")
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)

        # Font Size
        self.font_size_label = ttk.Label(self, text=translations[self.language]["font_size"], bootstyle="info")
        self.font_size_label.pack(pady=5)
        self.font_size_var = ttk.IntVar(value=12)
        # Spinbox for selecting font size
        font_size_spinbox = ttk.Spinbox(
            self, from_=8, to=32, textvariable=self.font_size_var, bootstyle="info", 
            command=self.adjust_font_size
        )
        font_size_spinbox.pack(pady=5)


        self.update_member_content()

    def change_language(self, event):
        # Get selected language
        selected_language = self.language_combobox.get()
        self.controller.change_language(selected_language)  # Update language in main controller
        self.update_language(selected_language)

    def change_theme(self, event):
        # Get selected theme
        selected_theme = self.theme_combobox.get()
        self.controller.set_theme(selected_theme)

    def adjust_font_size(self):
        # Get selected font size
        font_size = self.font_size_var.get()
        self.controller.update_font_size(font_size)

    def update_language(self, language):
        # Update all labels and widgets with new language
        self.language = language
        self.language_label.config(text=translations[language]["select_language"])
        self.theme_label.config(text=translations[language]["select_theme"])
        self.font_size_label.config(text=translations[language]["font_size"])
        self.update_member_content()

    def update_member_content(self):
        # Clear existing member content
        for widget in self.member_content_frame.winfo_children():
            widget.destroy()
        # Add member content if member feature is enabled
        if self.controller.member_var.get():
            member_label = ttk.Label(self.member_content_frame, text=translations[self.language]["member_exclusive_content"], font=("Helvetica", 14, "bold"))
            member_label.pack(pady=5)
            # Discount code entry
            discount_label = ttk.Label(self.member_content_frame, text=translations[self.language]["enter_discount_code"])
            discount_label.pack(pady=5)
            # Entry for discount code
            self.controller.discount_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.controller.discount_entry.pack(pady=5)
            # Button to apply discount code
            discount_button = ttk.Button(self.member_content_frame, text=translations[self.language]["apply_discount"], command=self.controller.validate_discount_code, bootstyle="success")
            discount_button.pack(pady=5)
            # Premium support contact
            support_label = ttk.Label(self.member_content_frame, text=translations[self.language]["premium_support_contact"])
            support_label.pack(pady=5)
            # Entry for support contact
            self.support_entry = ttk.Entry(self.member_content_frame, bootstyle="info")
            self.support_entry.pack(pady=5)
            support_button = ttk.Button(self.member_content_frame, text=translations[self.language]["contact_support"], command=self.contact_support, bootstyle="success")
            support_button.pack(pady=5)
    def contact_support(self):
        # Check if the user is a member
        if not self.controller.member_var.get():
            messagebox.showwarning(translations[self.current_language]["support"], translations[self.current_language]["only_members_support"])
            return
    
        # Implement the logic to contact support
        support_message = self.support_entry.get().strip()
        # Check if the user entered a support message
        if not support_message:
            messagebox.showwarning(translations[self.current_language]["support"], translations[self.current_language]["enter_support_message"])
            return
    
        try:
            # Email configuration
            sender_email = f"{os.getenv('SENDER_EMAIL')}"
            receiver_email = f"{os.getenv('SENDER_EMAIL')}"
            password = f"{os.getenv('SENDER_PASSWORD')}"
    
            # Create the email content
            subject = translations[self.controller.current_language]["support_request"]
            body = f"{translations[self.controller.current_language]['support_request_message']}:\n\n{support_message}"
    
            # Send the email
            send_email(sender_email, receiver_email, subject, body, password)
    
            messagebox.showinfo(translations[self.controller.current_language]["support"], translations[self.controller.current_language]["support_request_sent"])
        except Exception as e:
            print(e)
            messagebox.showerror(translations[self.controller.current_language]["support"], f"{translations[self.controller.current_language]['failed_to_send_support']}: {e}")