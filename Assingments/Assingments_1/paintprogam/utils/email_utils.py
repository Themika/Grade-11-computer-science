import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox
import os

def send_email(sender_email, receiver_email, subject, body, password):
    """Send an email using SMTP."""
    try:
        # Create the email content
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        messagebox.showinfo("Email", "Email sent successfully.")
    except Exception as e:
        messagebox.showerror("Email", f"Failed to send email: {e}")