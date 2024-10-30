import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
import os
import requests
from dotenv import load_dotenv

class ChatBotUI(ttk.Frame):
    def __init__(self, root):
        """Initialize ChatBotUI with a reference to the parent widget."""
        super().__init__(root)
        self.root = root
        load_dotenv()
        self.create_chat_interface()

    def create_chat_interface(self):
        """Create a simple chat interface with essential components."""
        # Configure grid layout to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # Chat history display
        self.chat_history_text = tk.Text(self, height=20, wrap=tk.WORD, state=tk.DISABLED,
                                         bg="#1D1E33", fg="#E5E5E5", font=("Helvetica", 12), padx=10, pady=10)
        self.chat_history_text.grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Scrollbar for chat history
        scrollbar = ttk.Scrollbar(self, command=self.chat_history_text.yview)
        scrollbar.grid(row=0, column=2, sticky='ns')
        self.chat_history_text['yscrollcommand'] = scrollbar.set

        # Message entry field
        self.message_entry = ttk.Entry(self, width=50, font=("Helvetica", 12))
        self.message_entry.grid(row=1, column=0, padx=5, pady=10, sticky="ew")

        # Send button
        send_button = ttk.Button(self, text="Send", command=self.on_send_message)
        send_button.grid(row=1, column=1, padx=5, pady=10)

        # Allow pressing Enter to send message
        self.message_entry.bind("<Return>", lambda event: self.on_send_message())

        # Add tags for styling messages
        self.chat_history_text.tag_configure("user", foreground="#007BFF", justify="right", lmargin1=10, lmargin2=10)
        self.chat_history_text.tag_configure("bot", foreground="#28A745", justify="left", lmargin1=10, lmargin2=10)

        # Add welcome message
        self.display_message("Bot", "Welcome! How can I assist you today?", "bot")

    def on_send_message(self):
        """Send the user's message and display the chatbot's response."""
        user_message = self.message_entry.get().strip()
        if user_message:
            self.display_message("You", user_message, "user")
            bot_response = self.get_response(user_message)
            self.display_message("Bot", bot_response, "bot")
        self.message_entry.delete(0, tk.END)

    def display_message(self, sender, message, tag):
        """Display a message in the chat history with simple styling."""
        self.chat_history_text.config(state=tk.NORMAL)
        self.chat_history_text.insert(tk.END, f"{sender}: {message}\n\n", tag)
        self.chat_history_text.config(state=tk.DISABLED)
        self.chat_history_text.yview(tk.END)

    def get_response(self, user_message):
        """Generate a response based on user input."""
        if "hello" in user_message.lower():
            return "Hello! How can I assist you today?"
        elif "help" in user_message.lower():
            return "I'm here to help! What do you need assistance with?"
        elif "bye" in user_message.lower():
            return "Goodbye! Have a great day."
        elif user_message.strip():
            return self.get_api_response(user_message).json().get("response", "Sorry, I couldn't fetch a response.")
        else:
            return "I'm not sure how to respond to that. Could you rephrase?"

    def get_api_response(self, response):
        """Get a response from an API."""
        url = "https://chatgpt-gpt4-ai-chatbot.p.rapidapi.com/ask"
        payload = {"query": response}
        headers = {
            "x-rapidapi-key": os.getenv("API_KEY"),
            "x-rapidapi-host": "chatgpt-gpt4-ai-chatbot.p.rapidapi.com",
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        return response if response.ok else self.loading_response()

    def loading_response(self):
        """Generate a loading response."""
        return "Please wait a moment while I process your request..."