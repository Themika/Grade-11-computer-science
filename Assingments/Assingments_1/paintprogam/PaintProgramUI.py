import ttkbootstrap as ttk
import tkinter as tk

from ttkbootstrap.constants import *
from dotenv import load_dotenv
from pages.home_page import HomePage
from pages.settings_page import SettingsPage
from pages.room_page import RoomPage
from pages.paint_options_page import PaintOptionsPage
from pages.payment_page import PaymentPage
from pages.chatbot_page import ChatBotUI
from tkinter import messagebox

"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program is a simple program that will allow a user to choose from various interior paint options. Then give you an invoice on the cost
of painting the room, providing you with 2 payment options.
1.) Discount code is MRBAWA:
    - 75% discount
2.) Non-member:
    - 5% discount
3.) Settings:
    The program will also allow you to change the language of the program to French.
    The program will also allow you to change the theme of the program to light or dark.
    The program will also allow you to change the font size of the program.
    This program for premium members will allow you to contact support.
4.) ChatBot:
    This program for premium members will allow you to enter a discount code and a AI assistant will help you with anything.
    The AI assistant will also help you with any questions you have about the program.
5.) Email:
    The program will also allow you to send an email to the support team.
I reccomend checking out the settings page first to see all the features of the program. Such as langaueg translation, theme changing, Dicount codes, font size changing, and support.
Functions used
    Enumerate()
        https://www.w3schools.com/python/ref_func_enumerate.asp
    isInstance()
        https://www.w3schools.com/python/ref_func_isinstance.asp
    hasatrr()
        https://www.w3schools.com/python/ref_func_hasattr.asp
Reasources uses
    ttkbootstrap
        https://ttkbootstrap.readthedocs.io/en/latest/
    smtplib
        https://docs.python.org/3/library/smtplib.html
        https://www.youtube.com/watch?v=S465v4mWsRg
    tkinter 
        https://docs.python.org/3/library/tkinter.html
        https://www.youtube.com/watch?v=epDKamC-V-8  
"""



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
        "cost_after_tax": "Cost After Tax",
        "code_activated": "CODE ACTIVATED",
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
        "cost_after_tax": "Coût après impôt",
        "code_activated": "CODE ACTIVÉ",
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
        self.discount_var = tk.StringVar()  # Initialize discount_var
        self.cost_before_tax = 0  # Initialize cost_before_tax
        self.cost_after_tax = 0  # Initialize cost_after_tax
        self.cost_label_after_tax = None  # Initialize cost_label_after_tax
        self.discount_entry = tk.StringVar()  # Initialize discount_entry
        self.code_activated_label = None  # Initialize code_activated_label
        self.support_entry = tk.StringVar()  # Initialize support_entry
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

        # Create a label for displaying the cost after tax
        self.cost_label_after_tax = ttk.Label(self.pages['Main'], text="")
        self.cost_label_after_tax.pack(pady=10)

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
            self.pages['Payment'].update_discount_options(["5%"])
            self.apply_discount()
            messagebox.showinfo(translations[self.current_language]["discount"], translations[self.current_language]["member_discount_applied"])

    def apply_discount(self, event=None):
        """Apply the selected discount and update the cost after tax."""
        discount = self.discount_var.get()
        if discount == "75%":
            self.cost_after_tax = self.cost_before_tax * 0.25
        elif discount == "5%":
            self.cost_after_tax = self.cost_before_tax * 0.95
        self.cost_label_after_tax.config(text=f"{translations[self.current_language]['cost_after_tax']}: ${round(self.cost_after_tax, 2)}")


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