import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from dotenv import load_dotenv
from pages.home_page import HomePage
from pages.settings_page import SettingsPage  # Ensure SettingsPage is imported
from pages.room_page import RoomPage
from pages.paint_options_page import PaintOptionsPage
from pages.payment_page import PaymentPage
from pages.chatbot_page import ChatBotUI
from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class PaintProgramUI(ttk.Window):
    def __init__(self):
        super().__init__(themename="darkly")  # Set default theme to "darkly"
        self.title("Paint Program UI")
        self.geometry("800x600")
        self.language = "English"
        
        self.pages = {}
        self.member_var = ttk.BooleanVar(value=False)
        self.color_var = tk.StringVar(value="Red")
        self.water_resistance_var = tk.StringVar(value="Low")
        self.finish_type_var = tk.StringVar(value="Matte")
        self.wall_entries = {}  # Initialize wall_entries
        self.member_content_frame = None  # Initialize member_content_frame
        load_dotenv()
        
        self.create_widgets()
        self.update_member_content()  

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=BOTH, expand=TRUE)
        
        self.pages['Main'] = ttk.Frame(self.notebook)
        self.notebook.add(self.pages['Main'], text='Home')
        
        self.create_home_page()
        
        # Start on the home page
        self.update_member_content()  # Initialize member content if needed
        self.notebook.select(self.pages['Main'])

    def create_home_page(self):
        if 'Home' in self.pages:
            old_home_page = self.pages.pop('Home')
            self.notebook.forget(old_home_page)
        home_page = HomePage(self.pages['Main'], self)
        self.pages['Home'] = home_page
        home_page.pack(fill=tk.BOTH, expand=True)
        self.notebook.select(self.pages['Main'])
    
    def create_room_page(self, num_rooms):
        if 'Rooms' in self.pages:
            old_settings_page = self.pages.pop('Rooms')
            self.notebook.forget(old_settings_page)
        room_page = RoomPage(self.notebook, self, num_rooms)
        self.pages['Rooms'] = room_page
        self.notebook.add(room_page, text='Rooms')
        self.notebook.select(self.pages['Rooms'])
    
    def create_paint_options_page(self):
        if 'PaintOptions' in self.pages:
            old_settings_page = self.pages.pop('PaintOptions')
            self.notebook.forget(old_settings_page)
        paint_options_page = PaintOptionsPage(self.notebook, self)
        self.pages['PaintOptions'] = paint_options_page
        self.notebook.add(paint_options_page, text='Paint Options')
        self.notebook.select(self.pages['PaintOptions'])
    
    def create_payment_page(self, cost_before_tax, cost_after_tax):
        if 'Payment' in self.pages:
            old_settings_page = self.pages.pop('Payment')
            self.notebook.forget(old_settings_page)
        payment_page = PaymentPage(self.notebook, self, cost_before_tax, cost_after_tax)
        self.pages['Payment'] = payment_page
        self.notebook.add(payment_page, text='Payment')
        self.notebook.select(self.pages['Payment'])
    
    def add_chatbot_tab(self):
        if 'ChatBot' in self.pages:
            old_settings_page = self.pages.pop('ChatBot')
            self.notebook.forget(old_settings_page)
        chatbot_page = ChatBotUI(self.notebook)
        self.pages['ChatBot'] = chatbot_page
        self.notebook.add(chatbot_page, text='ChatBot')
        self.notebook.select(self.pages['ChatBot'])
    
    def create_settings_page(self):
        if 'Settings' in self.pages:
            old_settings_page = self.pages.pop('Settings')
            self.notebook.forget(old_settings_page)
    
        settings_page = SettingsPage(self.notebook, self)
        self.pages['Settings'] = settings_page
        self.notebook.add(settings_page, text='Settings')
        self.member_content_frame = settings_page.member_content_frame
        self.update_member_content()
    
        self.notebook.select(self.pages['Settings'])

    def set_theme(self, theme):
        self.style.theme_use(theme)  # Change the theme of the application

    def update_font_size(self, font_size):
        self.style.configure('.', font=("Helvetica", font_size))
        for widget in self.winfo_children():
            try:
                widget.configure(font=("Helvetica", font_size))
            except tk.TclError:
                pass

    def update_member_content(self):
        if self.member_content_frame:
            for widget in self.member_content_frame.winfo_children():
                widget.destroy()

        if self.member_var.get():
            self.pages['Settings'].update_member_content()
        else:
            if 'Settings' in self.pages:
                no_member_label = ttk.Label(self.member_content_frame, text="Upgrade to Member for Exclusive Features.", bootstyle="warning")
                no_member_label.pack(pady=5)

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
    def set_language(self, language):
        """Change the language across the application."""
        self.language = language
        # Update all pages that need translation
        if "Home" in self.pages:
            self.pages["Home"].update_language(language)
        
    def contact_support(self):
        if not self.member_var.get():
            messagebox.showwarning("Support", "Only members can contact support.")
            return

        support_message = self.support_entry.get().strip()
        if not support_message:
            messagebox.showwarning("Support", "Please enter a message for support.")
            return

        try:
            sender_email = "your_email@gmail.com"
            receiver_email = "support_email@example.com"
            password = "your_email_password"

            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = "Support Request from Member"
            body = f"Support request message:\n\n{support_message}"
            message.attach(MIMEText(body, "plain"))

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            server.quit()

            messagebox.showinfo("Support", "Support request sent successfully.")
        except Exception as e:
            messagebox.showerror("Support", f"Failed to send support request: {e}")

    def on_submit_walls(self, wall_entries):
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
            self.wall_entries = wall_entries
            print("Wall dimensions submitted successfully.")

if __name__ == "__main__":
    app = PaintProgramUI()
    app.mainloop()
