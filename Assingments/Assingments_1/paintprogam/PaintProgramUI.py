import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from dotenv import load_dotenv
from pages.home_page import HomePage
from pages.settings_page import SettingsPage
from pages.room_page import RoomPage
from pages.paint_options_page import PaintOptionsPage
from pages.payment_page import PaymentPage
from pages.chatbot_page import ChatBotUI
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Translations for the application
translations = {
    "English": {
        "home": "Home",
        "rooms": "Rooms",
        "paint_options": "Paint Options",
        "payment": "Payment",
        "chatbot": "ChatBot",
        "settings": "Settings",
        "upgrade_to_member": "Upgrade to Member for Exclusive Features.",
        "discount": "Discount",
        "discount_applied": "75% discount applied successfully!",
        "member_discount_applied": "5% member discount applied.",
        "support": "Support",
        "only_members_support": "Only members can contact support.",
        "enter_support_message": "Please enter a message for support.",
        "support_request_sent": "Support request sent successfully.",
        "failed_to_send_support": "Failed to send support request"
    },
    "French": {
        "home": "Accueil",
        "rooms": "Pièces",
        "paint_options": "Options de peinture",
        "payment": "Paiement",
        "chatbot": "ChatBot",
        "settings": "Paramètres",
        "upgrade_to_member": "Passez à Membre pour des fonctionnalités exclusives.",
        "discount": "Remise",
        "discount_applied": "Remise de 75% appliquée avec succès!",
        "member_discount_applied": "Remise de 5% pour les membres appliquée.",
        "support": "Support",
        "only_members_support": "Seuls les membres peuvent contacter le support.",
        "enter_support_message": "Veuillez entrer un message pour le support.",
        "support_request_sent": "Demande de support envoyée avec succès.",
        "failed_to_send_support": "Échec de l'envoi de la demande de support"
    }
}

class PaintProgramUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Set default theme to "darkly"
        self.title("Paint Program UI")
        self.geometry("800x600")
        
        self.pages = {}
        self.member_var = ttk.BooleanVar(value=False)
        self.color_var = tk.StringVar(value="Red")
        self.water_resistance_var = tk.StringVar(value="Low")
        self.finish_type_var = tk.StringVar(value="Matte")
        self.wall_entries = {}  # Initialize wall_entries
        self.member_content_frame = None  # Initialize member_content_frame
        self.current_language = "English"  # Default language to English
        load_dotenv()
        
        self.create_widgets()

    def create_widgets(self):
        # Create a style object to customize the appearance of ttk widgets
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=TRUE)
        # Create a style object to customize the appearance of ttk widgets
        self.pages['Main'] = ttk.Frame(self.notebook)
        
        self.notebook.add(self.pages['Main'], text=translations[self.current_language]['home'])
        
        self.create_home_page()
        
        # Start on the home page
        self.notebook.select(self.pages['Main'])

    def create_home_page(self):
        # Check if the home page already exists and remove it
        if 'Home' in self.pages:
            old_home_page = self.pages.pop('Home')
            self.notebook.forget(old_home_page)
        # Create a new home page
        home_page = HomePage(self.pages['Main'], self)
        self.pages['Home'] = home_page
        home_page.pack(fill=tk.BOTH, expand=True)
        self.notebook.select(self.pages['Main'])
    
    def create_room_page(self, num_rooms):
        # Check if the room page already exists and remove it
        if 'Rooms' in self.pages:
            old_settings_page = self.pages.pop('Rooms')
            self.notebook.forget(old_settings_page)
        # Create a new room page
        room_page = RoomPage(self.notebook, self, num_rooms)
        self.pages['Rooms'] = room_page
        self.notebook.add(room_page, text=translations[self.current_language]['rooms'])
        self.notebook.select(self.pages['Rooms'])
    
    def create_paint_options_page(self):
        # Check if the paint options page already exists and remove it
        if 'PaintOptions' in self.pages:
            old_settings_page = self.pages.pop('PaintOptions')
            self.notebook.forget(old_settings_page)
        # Create a new paint options page
        paint_options_page = PaintOptionsPage(self.notebook, self)
        self.pages['PaintOptions'] = paint_options_page
        self.notebook.add(paint_options_page, text=translations[self.current_language]['paint_options'])
        self.notebook.select(self.pages['PaintOptions'])
    
    def create_payment_page(self, cost_before_tax, cost_after_tax):
        # Check if the payment page already exists and remove it
        if 'Payment' in self.pages:
            old_settings_page = self.pages.pop('Payment')
            self.notebook.forget(old_settings_page)
        # Create a new payment page
        payment_page = PaymentPage(self.notebook, self, cost_before_tax, cost_after_tax)
        self.pages['Payment'] = payment_page
        self.notebook.add(payment_page, text=translations[self.current_language]['payment'])
        self.notebook.select(self.pages['Payment'])
    
    def add_chatbot_tab(self):
        # Check if the chatbot page already exists and remove it
        if 'ChatBot' in self.pages:
            old_settings_page = self.pages.pop('ChatBot')
            self.notebook.forget(old_settings_page)
        # Create a new chatbot page with the current language
        chatbot_page = ChatBotUI(self.notebook)
        self.pages['ChatBot'] = chatbot_page
        # Add the chatbot page to the notebook
        self.notebook.add(chatbot_page, text=translations[self.current_language]['chatbot'])
        self.notebook.select(self.pages['ChatBot'])
    
    def create_settings_page(self):
        # Check if the settings page already exists and remove it
        if 'Settings' in self.pages:
            old_settings_page = self.pages.pop('Settings')
            self.notebook.forget(old_settings_page)
    
        # Create a new settings page
        settings_page = SettingsPage(self.notebook, self)  # Use SettingsPage directly
        self.pages['Settings'] = settings_page
        self.notebook.add(settings_page, text=translations[self.current_language]['settings'])  # Add to notebook here
        self.member_content_frame = settings_page.member_content_frame
        self.update_member_content()  # Ensure any member content updates
    
        # Select Settings page to ensure it’s visible
        self.notebook.select(self.pages['Settings'])

    def set_theme(self, theme):
        self.style.theme_use(theme)  # Change the theme of the application

    def update_font_size(self, font_size):
        # Update the default style font used by ttkbootstrap widgets
        self.style.configure('.', font=("Helvetica", font_size))

        # Update only font-compatible widgets
        for widget in self.winfo_children():
            try:
                widget.configure(font=("Helvetica", font_size))
            except tk.TclError:
                # Skip widgets that don't support font configuration
                pass

    def change_language(self, language):
        # Update the current language
        self.current_language = language
        self.update_language()

    def update_language(self):
        # Update language for each notebook tab and its associated widgets
        for page_name, page in self.pages.items():
            # Update the tab text for each page
            if page_name == 'Main':
                self.notebook.tab(page, text=translations[self.current_language]['home'])
            elif page_name == 'Settings':
                self.notebook.tab(page, text=translations[self.current_language]['settings'])
            elif page_name == 'Rooms':
                self.notebook.tab(page, text=translations[self.current_language]['rooms'])
            elif page_name == 'PaintOptions':
                self.notebook.tab(page, text=translations[self.current_language]['paint_options'])
            elif page_name == 'Payment':
                self.notebook.tab(page, text=translations[self.current_language]['payment'])
            elif page_name == 'ChatBot':
                self.notebook.tab(page, text=translations[self.current_language]['chatbot'])

            # Loop through each widget in the page and update its text
            for widget in page.winfo_children():
                if isinstance(widget, ttk.Label) or isinstance(widget, ttk.Button):
                    # Translate the widget's current text and update
                    widget_text = widget.cget("text")
                    for key, value in translations['English'].items():
                        # Check if the widget text matches the English translation
                        if value == widget_text:
                            translated_text = translations[self.current_language][key]
                            widget.config(text=translated_text)
                            break

            # Re-render page if it has a method to refresh itself (e.g., custom pages with complex layouts)
            if hasattr(page, 'update_language'):
                page.update_language(self.current_language)
        # Update member content if the user is a member
        self.update_member_content()

    def update_member_content(self):
        # Clear previous member-specific content
        if self.member_content_frame:
            for widget in self.member_content_frame.winfo_children():
                widget.destroy()
    
        # Check if the user is marked as a member
        if self.member_var.get():
            self.pages['Settings'].update_member_content()  # Display member content
        else:
            # Optionally display a message or hide member content if not a member
            no_member_label = ttk.Label(self.member_content_frame, text=translations[self.current_language]["upgrade_to_member"], bootstyle="warning")
            no_member_label.pack(pady=5)

    def validate_discount_code(self):
        discount_code = self.discount_entry.get().strip()
        # Check if the user is a member
        if discount_code == "MRBAWA":
            # Apply a 75% discount for members
            self.discount_var.set("75%")
            self.apply_discount()
            # Show a success message
            messagebox.showinfo(translations[self.current_language]["discount"], translations[self.current_language]["discount_applied"])
        else:
            # Apply a 5% discount for non-members
            self.discount_var.set("5%")
            # Check if the user is a member
            self.apply_discount()
            messagebox.showinfo(translations[self.current_language]["discount"], translations[self.current_language]["member_discount_applied"])

    def apply_discount(self, event=None):
        # Calculate the cost after applying the discount
        discount = self.discount_var.get()
        if discount == "75%":
            self.cost_after_tax = self.cost_before_tax * 0.25
        elif discount == "5%":
            self.cost_after_tax = self.cost_before_tax * 0.95
        self.cost_label_after_tax.config(text=f"{translations[self.current_language]['cost_after_tax']}: ${round(self.cost_after_tax, 2)}")

    def contact_support(self):
        # Check if the user is a member
        if not self.member_var.get():
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
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = translations[self.current_language]["support_request"]
            body = f"{translations[self.current_language]['support_request_message']}:\n\n{support_message}"
            message.attach(MIMEText(body, "plain"))

            # Connect to the Gmail SMTP server and send the email
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

            messagebox.showinfo(translations[self.current_language]["support"], translations[self.current_language]["support_request_sent"])
        except Exception as e:
            messagebox.showerror(translations[self.current_language]["support"], f"{translations[self.current_language]['failed_to_send_support']}: {e}")

    def on_submit_walls(self, wall_entries):
        """Validate wall dimensions and highlight invalid entries."""
        valid = True
        for room, entries in wall_entries.items():
            for entry in entries:
                entry_value = entry.get().strip()
                if not entry_value.isdigit():
                    entry.config(bootstyle="danger")
                    valid = False
                else:
                    entry.config(bootstyle="info")
        if valid:
            self.wall_entries = wall_entries  # Store wall_entries in the PaintProgramUI class
            # You can add further processing logic here
# Run the application
if __name__ == "__main__":
    app = PaintProgramUI()
    app.mainloop()