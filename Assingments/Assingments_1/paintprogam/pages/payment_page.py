import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from utils.email_utils import send_email
from datetime import datetime
from random import randint
import os
from dotenv import load_dotenv

translations = {
    "English": {
        "select_payment_method": "Select Your Payment Method",
        "cost_before_tax": "Cost Before Tax",
        "cost_after_tax": "Cost After Tax",
        "select_discount": "Select Discount:",
        "enter_payment_amount": "Enter Payment Amount:",
        "confirm_payment": "Confirm Payment",
        "payment_confirmation": "Payment Confirmation",
        "payment_method_selected": "Payment method '{0}' selected.",
        "payment_sufficient": "Payment is sufficient.",
        "payment_insufficient": "Entered amount is not sufficient.",
        "invalid_amount": "Invalid amount entered.",
        "here_is_your_change": "Here is your change:",
        "fifty_dollar_bills": "Fifty Dollar bills",
        "twenty_dollar_bills": "Twenty Dollar bills",
        "ten_dollar_bills": "Ten Dollar bills",
        "five_dollar_bills": "Five Dollar bills",
        "toonies": "Toonies",
        "loonies": "Loonies",
        "quarters": "Quarters",
        "dimes": "Dimes",
        "nickels": "Nickels",
        "pennies": "Pennies",
        "error": "Error"
    },
    "French": {
        "select_payment_method": "Sélectionnez votre méthode de paiement",
        "cost_before_tax": "Coût avant taxes",
        "cost_after_tax": "Coût après taxes",
        "select_discount": "Sélectionnez la remise:",
        "enter_payment_amount": "Entrez le montant du paiement:",
        "confirm_payment": "Confirmer le paiement",
        "payment_confirmation": "Confirmation de paiement",
        "payment_method_selected": "Méthode de paiement '{0}' sélectionnée.",
        "payment_sufficient": "Le paiement est suffisant.",
        "payment_insufficient": "Le montant saisi n'est pas suffisant.",
        "invalid_amount": "Montant saisi invalide.",
        "here_is_your_change": "Voici votre monnaie:",
        "fifty_dollar_bills": "Billets de cinquante dollars",
        "twenty_dollar_bills": "Billets de vingt dollars",
        "ten_dollar_bills": "Billets de dix dollars",
        "five_dollar_bills": "Billets de cinq dollars",
        "toonies": "Pièces de deux dollars",
        "loonies": "Pièces de un dollar",
        "quarters": "Quarts",
        "dimes": "Dix sous",
        "nickels": "Nickels",
        "pennies": "Sous",
        "error": "Erreur"
    }
}

class PaymentPage(ttk.Frame):
    def __init__(self, container, parent, cost_before_tax, cost_after_tax):
        super().__init__(container)
        self.parent = parent
        self.language = parent.current_language
        self.cost_before_tax = cost_before_tax
        self.cost_after_tax = cost_after_tax
        self.create_widgets()
        load_dotenv()

    def create_widgets(self):
        self.label = ttk.Label(self, text=translations[self.language]["select_payment_method"], font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.cost_label_before_tax = ttk.Label(self, text=f"{translations[self.language]['cost_before_tax']}: ${round(self.cost_before_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_before_tax.grid(row=1, column=0, columnspan=2, pady=10, padx=50)
        
        self.cost_label_after_tax = ttk.Label(self, text=f"{translations[self.language]['cost_after_tax']}: ${round(self.cost_after_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_after_tax.grid(row=2, column=0, columnspan=2, pady=10, padx=50)
        
        if self.parent.member_var.get():
            discount_frame = ttk.Frame(self)
            discount_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
            
            discount_label = ttk.Label(discount_frame, text=translations[self.language]["select_discount"], font=("Helvetica", 12))
            discount_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
            
            self.discount_var = tk.StringVar(value="5%")
            discount_options = ["5%", "75%"]
            discount_combobox = ttk.Combobox(discount_frame, values=discount_options, textvariable=self.discount_var, bootstyle="info", state="readonly")
            discount_combobox.grid(row=0, column=1, pady=5, padx=5)
            discount_combobox.bind("<<ComboboxSelected>>", self.parent.apply_discount)
            row = 4
        else:
            row = 3
        
        payment_frame_inner = ttk.Frame(self)
        payment_frame_inner.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        
        payment_options = {
            "Credit Card": "Visa, MasterCard, American Express",
            "Cash": "Cash payment",
            "Check": "Check payment",
            "PayPal": "PayPal account",
        }
        
        self.payment_choice_var = tk.StringVar(value="Credit Card")
        
        for payment, description in payment_options.items():
            ttk.Radiobutton(payment_frame_inner, text=(f"{payment}: {description}"), variable=self.payment_choice_var, value=payment).grid(row=row, column=0, sticky=tk.W, pady=5, padx=50)
            row += 1
        
        amount_frame = ttk.Frame(self)
        amount_frame.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        
        amount_label = ttk.Label(amount_frame, text=translations[self.language]["enter_payment_amount"], font=("Helvetica", 12))
        amount_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
        
        self.amount_entry = ttk.Entry(amount_frame, bootstyle="info")
        self.amount_entry.grid(row=0, column=1, pady=5, padx=5)
        row += 1
        
        button_frame = ttk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        
        confirm_button = ttk.Button(button_frame, text=translations[self.language]["confirm_payment"], command=self.on_confirm_payment, bootstyle="success")
        confirm_button.grid(row=0, column=0, pady=10, padx=5, sticky=tk.W)
        
        self.change_frame = ttk.Frame(self)
        self.change_frame.grid(row=row + 1, column=0, columnspan=2, pady=10, padx=5)    

    def on_confirm_amount(self, cost_after_tax):
        try:
            self.entered_amount = float(self.amount_entry.get().strip())
            if self.entered_amount >= cost_after_tax:
                print(translations[self.language]["payment_sufficient"])
                change = self.entered_amount - cost_after_tax
                self.process_change(change)
                return True
            else:
                print(translations[self.language]["payment_insufficient"])
                messagebox.showerror(translations[self.language]["error"], translations[self.language]["payment_insufficient"])
                return False
        except ValueError:
            print(translations[self.language]["invalid_amount"])
            messagebox.showerror(translations[self.language]["error"], translations[self.language]["invalid_amount"])
            return False

    def process_change(self, difference):
        money_map = {
            50: translations[self.language]["fifty_dollar_bills"],
            20: translations[self.language]["twenty_dollar_bills"],
            10: translations[self.language]["ten_dollar_bills"],
            5: translations[self.language]["five_dollar_bills"],
            2: translations[self.language]["toonies"],
            1: translations[self.language]["loonies"],
            0.25: translations[self.language]["quarters"],
            0.10: translations[self.language]["dimes"],
            0.05: translations[self.language]["nickels"],
            0.01: translations[self.language]["pennies"],
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
        ttk.Label(self.change_frame, text=translations[self.language]["here_is_your_change"], font=("Helvetica", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=5)
        row = 1
        for name, count in change.items():
            ttk.Label(self.change_frame, text=f"{name}: {count}", font=("Helvetica", 12)).grid(row=row, column=0, columnspan=2, pady=2)
            row += 1

    def on_confirm_payment(self):
        if self.on_confirm_amount(self.cost_after_tax):
            selected_payment_method = self.payment_choice_var.get()
            messagebox.showinfo(translations[self.language]["payment_confirmation"], translations[self.language]["payment_method_selected"].format(selected_payment_method))
            self.send_email_receipt()

    def send_email_receipt(self):
        # Access user data from the parent class
        user_data = self.parent.user_data

        # Generate the receipt content
        name = user_data["name"]
        email = user_data["email"]
        print(email)
        date_str = datetime.now().strftime("%Y-%m-%d")
        paint_choice = user_data["paint_choice"]
        amount_of_paint =  user_data["total_paint_cans"]
        paint_cost = user_data["cost_after_tax"]
        subtotal = round(self.cost_before_tax, 2)
        tax = round(self.cost_after_tax - self.cost_before_tax, 2)
        total = round(self.cost_after_tax, 2)
        subject = "Paint Order Receipt"
        custom_details = (
            f"Color: {user_data['color']}, "
            f"Finish: {user_data['finish_type']}\n, "
            f"Water Resistance: {user_data['water_resistance']}\n, "
            f"Durability: {user_data['durability']}\n"
            if paint_choice == "Custom Paint"
            else f"Color: {user_data['color']}\n, "
            f"Finish: {user_data['finish_type']}," 
        )
        send_email(
            sender_email=os.getenv("SENDER_EMAIL"),
            receiver_email=email,
            subject=subject,
            body=f"""
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
            """,
            password=os.getenv("SENDER_PASSWORD")
        )

    def update_language(self, language):
        self.language = language
        self.label.config(text=translations[language]["select_payment_method"])
        self.cost_label_before_tax.config(text=f"{translations[language]['cost_before_tax']}: ${round(self.cost_before_tax, 2)}")
        self.cost_label_after_tax.config(text=f"{translations[language]['cost_after_tax']}: ${round(self.cost_after_tax, 2)}")
        if hasattr(self, 'discount_frame'):
            self.discount_label.config(text=translations[language]["select_discount"])
        self.amount_label.config(text=translations[language]["enter_payment_amount"])
        self.confirm_button.config(text=translations[language]["confirm_payment"])
        if hasattr(self, 'change_frame'):
            self.change_frame.grid_remove()
        self.process_change(0)  # Reset change display