import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox
from utils.email_utils import send_email
from datetime import datetime
from random import randint
import os
from dotenv import load_dotenv
# Translations for different languages
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
        "error": "Error",
        "enter_card_number": "Enter Card Number(16 Numbers):",
        "enter_expiration_date": "Enter Expiration Date (MM/YY):",
        "enter_cvv": "Enter CVV:",
        "enter_paypal_email": "Enter PayPal Email:"
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
        "error": "Erreur",
        "enter_card_number": "Entrez le numéro de carte(16 par nom):",
        "enter_expiration_date": "Entrez la date d'expiration (MM/AA):",
        "enter_cvv": "Entrez le CVV:",
        "enter_paypal_email": "Entrez l'email PayPal:"
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
        # Payment Method Selection
        self.label = ttk.Label(self, text=translations[self.language]["select_payment_method"], font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)
        # Cost Labels
        self.cost_label_before_tax = ttk.Label(self, text=f"{translations[self.language]['cost_before_tax']}: ${round(self.cost_before_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_before_tax.grid(row=1, column=0, columnspan=2, pady=10, padx=0)
        # Cost After Tax
        self.cost_label_after_tax = ttk.Label(self, text=f"{translations[self.language]['cost_after_tax']}: ${round(self.cost_after_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_after_tax.grid(row=2, column=0, columnspan=2, pady=10, padx=0)
        # Discount Selection
        if self.parent.member_var.get():
            # Discount Frame
            discount_frame = ttk.Frame(self)
            discount_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
            # Discount Label
            discount_label = ttk.Label(discount_frame, text=translations[self.language]["select_discount"], font=("Helvetica", 12))
            discount_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
            # Discount Combobox
            self.discount_var = tk.StringVar(value="5%")
            discount_options = ["5%", "75%"]
            discount_combobox = ttk.Combobox(discount_frame, values=discount_options, textvariable=self.discount_var, bootstyle="info", state="readonly")
            discount_combobox.grid(row=0, column=1, pady=5, padx=5)
            discount_combobox.bind("<<ComboboxSelected>>", self.parent.apply_discount)
            row = 4
        else:
            row = 3
        # Payment Method Selection
        payment_frame_inner = ttk.Frame(self)
        payment_frame_inner.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        # Payment Options
        payment_options = {
            "Credit Card": "Visa, MasterCard, American Express",
            "Cash": "Cash payment",
            "PayPal": "PayPal account",
        }
        # Payment Choice Variable
        self.payment_choice_var = tk.StringVar(value="Credit Card")
        # Payment Radiobuttons
        for payment, description in payment_options.items():
            ttk.Radiobutton(payment_frame_inner, text=(f"{payment}: {description}"), variable=self.payment_choice_var, value=payment, command=self.update_payment_fields).grid(row=row, column=0, sticky=tk.W, pady=5, padx=50)
            row += 1
        # Payment Fields
        self.payment_fields_frame = ttk.Frame(self)
        self.payment_fields_frame.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        # Amount Entry
        self.amount_frame = ttk.Frame(self)
        self.amount_frame.grid(row=row + 1, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        # Amount Label
        self.amount_label = ttk.Label(self.amount_frame, text=translations[self.language]["enter_payment_amount"], font=("Helvetica", 12))
        self.amount_label.grid(row=0, column=0, pady=5, padx=259, sticky=tk.W)
        # Amount Entry
        self.amount_entry = ttk.Entry(self.amount_frame, bootstyle="info")
        self.amount_entry.grid(row=1, column=0, pady=5, padx=300, sticky=tk.W)
        # Confirm Button
        row += 1
        button_frame = ttk.Frame(self)
        button_frame.grid(row=row, column=0, columnspan=2, pady=10, padx=5, sticky=tk.W)
        # Confirm Payment Button
        self.confirm_button = ttk.Button(button_frame, text=translations[self.language]["confirm_payment"], command=self.on_confirm_payment, bootstyle="success")
        self.confirm_button.grid(row=0, column=0, pady=10, padx=5, sticky=tk.W)
        # Change Frame
        self.change_frame = ttk.Frame(self)
        self.change_frame.grid(row=row + 1, column=0, columnspan=2, pady=10, padx=5)  
        # Hide amount entry and label for Credit Card payment
        self.update_payment_fields()
    # Update payment fields based on the selected payment method
    def update_payment_fields(self):
        # Clear previous payment fields
        for widget in self.payment_fields_frame.winfo_children():
            widget.destroy()
        # Get the selected payment method
        selected_payment_method = self.payment_choice_var.get()
        # Display payment fields based on the selected payment method
        if selected_payment_method == "Credit Card":
            # Credit Card Fields
            card_number_label = ttk.Label(self.payment_fields_frame, text=translations[self.language]["enter_card_number"], font=("Helvetica", 12))
            card_number_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
            # Card Number Entry
            self.card_number_entry = ttk.Entry(self.payment_fields_frame, bootstyle="info")
            self.card_number_entry.grid(row=0, column=1, pady=5, padx=5)
            print("The code has to be 16 numbers")
            # Expiration Date Entry
            expiration_date_label = ttk.Label(self.payment_fields_frame, text=translations[self.language]["enter_expiration_date"], font=("Helvetica", 12))
            expiration_date_label.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
            self.expiration_date_entry = ttk.Entry(self.payment_fields_frame, bootstyle="info")
            self.expiration_date_entry.grid(row=1, column=1, pady=5, padx=5)
            # CVV Entry
            cvv_label = ttk.Label(self.payment_fields_frame, text=translations[self.language]["enter_cvv"], font=("Helvetica", 12))
            cvv_label.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)
            self.cvv_entry = ttk.Entry(self.payment_fields_frame, bootstyle="info")
            self.cvv_entry.grid(row=2, column=1, pady=5, padx=5)
            
            # Hide amount entry and label for Credit Card payment
            self.amount_frame.grid_remove()
        
        elif selected_payment_method == "PayPal":
            # PayPal Email Entry
            paypal_email_label = ttk.Label(self.payment_fields_frame, text=translations[self.language]["enter_paypal_email"], font=("Helvetica", 12))
            paypal_email_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)
            self.paypal_email_entry = ttk.Entry(self.payment_fields_frame, bootstyle="info")
            self.paypal_email_entry.grid(row=0, column=1, pady=5, padx=5)
            
            # Show amount entry and label for PayPal payment
            self.amount_frame.grid()
        
        elif selected_payment_method == "Cash":
            # Show amount entry and label for Cash payment
            self.amount_frame.grid()

    def on_confirm_amount(self, cost_after_tax):
        try:
            # Get the entered amount
            self.entered_amount = float(self.amount_entry.get().strip())
            if self.entered_amount >= cost_after_tax:
                print(translations[self.language]["payment_sufficient"])
                change = self.entered_amount - cost_after_tax
                # Process change if payment method is Cash
                if self.payment_choice_var.get() == "Cash":
                    self.process_change(change)
                return True
            # Display error message if the entered amount is insufficient
            else:
                print(translations[self.language]["payment_insufficient"])
                # Display error message
                messagebox.showerror(translations[self.language]["error"], translations[self.language]["payment_insufficient"])
                return False
        except ValueError:
            # Display error message if the entered amount is invalid
            print(translations[self.language]["invalid_amount"])
            messagebox.showerror(translations[self.language]["error"], translations[self.language]["invalid_amount"])
            return False

    def process_change(self, difference):
        # Map money values to their names
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
        # Calculate the change
        change = {}
        for value, name in money_map.items():
            # Calculate the number of each money value
            count = int(difference // value)
            # Update the difference
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
    """Validate the entered payment amount and process the payment."""
    def on_confirm_payment(self):
        if self.payment_choice_var.get() != "Credit Card" and not self.on_confirm_amount(self.cost_after_tax):
            return
        # Get the selected payment method
        selected_payment_method = self.payment_choice_var.get()
        if selected_payment_method == "Credit Card":
            card_number = self.card_number_entry.get().strip()
            expiration_date = self.expiration_date_entry.get().strip()
            cvv = self.cvv_entry.get().strip()
            # Validate the entered card details
            if not (card_number.isdigit() and len(card_number) == 16):
                # Display error message
                messagebox.showerror(translations[self.language]["error"], "Invalid card number.")
                return
            # Validate the entered expiration date
            if not (len(expiration_date) == 5 and expiration_date[2] == '/'):
                # Display error message
                messagebox.showerror(translations[self.language]["error"], "Invalid expiration date.")
                return
            # Validate the entered CVV
            if not self.validate_expiration_date(expiration_date):
                # Display error message
                messagebox.showerror(translations[self.language]["error"], "Expiration date is in the past.")
                return
            # Validate the entered CVV
            if not (cvv.isdigit() and len(cvv) == 3):
                # Display error message
                messagebox.showerror(translations[self.language]["error"], "Invalid CVV.")
                return
        elif selected_payment_method == "PayPal":
            # Validate the entered PayPal email
            paypal_email = self.paypal_email_entry.get().strip()
            if not paypal_email:
                messagebox.showerror(translations[self.language]["error"], "Invalid PayPal email.")
                return

        messagebox.showinfo(translations[self.language]["payment_confirmation"], translations[self.language]["payment_method_selected"].format(selected_payment_method))
        self.send_email_receipt()

    def validate_expiration_date(self, expiration_date):
        # Validate the expiration date
        try:
            # Extract the month and year
            exp_month, exp_year = expiration_date.split('/')
            exp_month = int(exp_month)
            exp_year = int(exp_year) + 2000  # Assuming the year is in YY format
            # Validate the month and year
            if exp_month < 1 or exp_month > 12:
                return False
            current_date = datetime.now()
            exp_date = datetime(exp_year, exp_month, 1)
            return exp_date >= current_date
        except ValueError:
            return False

    def send_email_receipt(self):
        # Access user data from the parent class
        user_data = self.parent.user_data
        
        # Generate the receipt content
        name = user_data["name"]
        email = user_data["email"]
        print(email)
        """Send an email receipt to the user."""
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
    """Update all labels to the selected language."""
    def update_language(self, language):
        # Update all labels with new language
        self.language = language
        # Update all labels with new language
        self.label.config(text=translations[language]["select_payment_method"])
        self.cost_label_before_tax.config(text=f"{translations[language]['cost_before_tax']}: ${round(self.cost_before_tax, 2)}")
        self.cost_label_after_tax.config(text=f"{translations[language]['cost_after_tax']}: ${round(self.cost_after_tax, 2)}")
        # Update discount label if it exists
        if hasattr(self, 'discount_frame'):
            self.discount_label.config(text=translations[language]["select_discount"])
        self.amount_label.config(text=translations[language]["enter_payment_amount"])
        self.confirm_button.config(text=translations[language]["confirm_payment"])
        # Update payment fields based on the new language
        if hasattr(self, 'change_frame'):
            self.change_frame.grid_remove()
        self.process_change(0)  # Reset change display
        self.update_payment_fields()  # Update payment fields based on the new language