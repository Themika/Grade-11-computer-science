import smtplib
import os

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tkinter import messagebox

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
    except smtplib.SMTPAuthenticationError:
        messagebox.showerror("Email", "Failed to authenticate with the SMTP server. Check your email and password.")
    except smtplib.SMTPConnectError:
        messagebox.showerror("Email", "Failed to connect to the SMTP server. Check your network connection.")
    except smtplib.SMTPException as e:
        messagebox.showerror("Email", f"SMTP error occurred: {e}")
    except Exception as e:
        messagebox.showerror("Email", f"Failed to send email: {e}")