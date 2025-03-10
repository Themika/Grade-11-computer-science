import socket
import random
import tkinter as tk
from tkinter import ttk, CENTER, messagebox
from threading import Thread
from PIL import Image, ImageTk
import ttkbootstrap as tb  # Modern styling

class RPSClient:
    # Initialize the client
    def __init__(self, root, game_manager):
        self.root = root
        self.game_manager = game_manager  
        self.root.geometry("1150x650")
        self.root.title("Rock Paper Scissors")
        self.style = tb.Style("superhero")  
        self.client_socket = None
        self.lobby_id = None
        self.create_initial_ui()
    # Create the initial UI
    def create_initial_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Rock Paper Scissors", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Mode selection
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        # Online and computer buttons
        online_button = ttk.Button(button_frame, text="Online", command=self.show_lobby_options, bootstyle="primary-outline", padding=10, width=20)
        online_button.grid(row=0, column=0, padx=50, pady=20)

        computer_button = ttk.Button(button_frame, text="Computer", command=self.start_computer, bootstyle="success-outline",padding=10, width=20)
        computer_button.grid(row=0, column=1, padx=50, pady=20)

        # Back button
        back_button = ttk.Button(button_frame, text="Back", command=self.game_manager.main_menu, bootstyle="danger-outline",padding=10, width=20)
        back_button.grid(row=0, column=2, padx=50, pady=20)

    def show_lobby_options(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Rock Paper Scissors - Online", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Lobby options
        lobby_frame = ttk.Frame(self.root, bootstyle="secondary")
        lobby_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        create_lobby_button = ttk.Button(lobby_frame, text="Create Lobby", command=self.create_lobby, bootstyle="primary-outline",padding=10, width=20)
        create_lobby_button.grid(row=0, column=0, padx=50, pady=20)

        join_lobby_button = ttk.Button(lobby_frame, text="Join Lobby", command=self.join_lobby, bootstyle="success-outline",padding=10, width=20)
        join_lobby_button.grid(row=0, column=1, padx=50, pady=20)

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_initial_ui, bootstyle="danger-outline",padding=10, width=20).place(relx=0.5, y=550, anchor=CENTER)

    def create_lobby(self):
        # Clear existing widgets
        self.lobby_id = f"Lobby{random.randint(1000, 9999)}"
        # Title
        if self.connect_to_server():
            self.client_socket.sendall(f"CREATE_LOBBY {self.lobby_id}".encode())
            response = self.client_socket.recv(1024).decode()
            # Check if lobby was created
            if response.startswith("LOBBY_CREATED"):
                self.create_online_ui()
            # Show error if lobby already exists
            elif response == "LOBBY_EXISTS":
                messagebox.showerror("Error", "Lobby already exists. Please try again.")
                self.client_socket.close()

    def join_lobby(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Join Lobby", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Lobby ID entry
        lobby_id_label = ttk.Label(self.root, text="Enter Lobby ID:", font=("Helvetica", 24))
        lobby_id_label.place(relx=0.5, y=200, anchor=CENTER)

        self.lobby_id_entry = ttk.Entry(self.root, font=("Helvetica", 24))
        self.lobby_id_entry.place(relx=0.5, y=250, anchor=CENTER)

        # Join button
        join_button = ttk.Button(self.root, text="Join", command=self.join_existing_lobby, bootstyle="primary-outline",padding=10)
        join_button.place(relx=0.5, y=300, anchor=CENTER)

        # Back button
        ttk.Button(self.root, text="Back", command=self.show_lobby_options, bootstyle="danger-outline",padding=10).place(relx=0.5, y=550, anchor=CENTER)

    def join_existing_lobby(self):
        # Get lobby ID from entry
        self.lobby_id = self.lobby_id_entry.get()
        # Connect to server
        if self.connect_to_server():
            self.client_socket.sendall(self.lobby_id.encode())
            response = self.client_socket.recv(1024).decode()
            # Check if lobby was found
            if response == "LOBBY_NOT_FOUND":
                messagebox.showerror("Error", "Lobby does not exist. Please check the Lobby ID and try again.")
                self.client_socket.close()
            # Check if lobby is full
            else:
                self.create_online_ui()

    def connect_to_server(self):
        # Connect to server
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", 8765))
            return True
        # Show error if connection fails
        except ConnectionError:
            self.show_error("Unable to connect to the server.")
            return False

    def create_online_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Rock Paper Scissors - Online", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Instructions
        instruction_label = ttk.Label(self.root, text="Choose your move:", font=("Helvetica", 24))
        instruction_label.place(relx=0.5, y=150, anchor=CENTER)

        # Load images
        self.load_images()

        # Buttons
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=0.7, anchor=CENTER)

        ttk.Button(button_frame, image=self.rock_img, command=lambda: self.send_move("Rock"), bootstyle="primary").grid(row=0, column=0, padx=50)
        ttk.Button(button_frame, image=self.paper_img, command=lambda: self.send_move("Paper"), bootstyle="success").grid(row=0, column=1, padx=50)
        ttk.Button(button_frame, image=self.scissors_img, command=lambda: self.send_move("Scissors"), bootstyle="info").grid(row=0, column=2, padx=50)

        # Result label
        self.result_label = ttk.Label(self.root, text="Waiting for result...", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.result_label.place(relx=0.5, y=250, anchor=CENTER)

        # Start thread to listen for server responses
        self.listener_thread = Thread(target=self.listen_to_server, daemon=True)
        self.listener_thread.start()

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_initial_ui, bootstyle="danger-outline",padding=10).place(relx=0.5, y=600, anchor=CENTER)

    def start_computer(self):
        self.create_computer_ui()

    def create_computer_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Rock Paper Scissors", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Load images
        self.load_images()

        # Buttons
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=0.7, anchor=CENTER)
        # Rock, paper, scissors buttons
        ttk.Button(button_frame, image=self.rock_img, command=lambda: self.play_vs_computer("Rock"), bootstyle="primary").grid(row=0, column=0, padx=50)
        ttk.Button(button_frame, image=self.paper_img, command=lambda: self.play_vs_computer("Paper"), bootstyle="success").grid(row=0, column=1, padx=50)
        ttk.Button(button_frame, image=self.scissors_img, command=lambda: self.play_vs_computer("Scissors"), bootstyle="info").grid(row=0, column=2, padx=50)

        # Result label
        self.result_label = ttk.Label(self.root, text="Choose your move to play!", font=("Helvetica", 16), bootstyle="inverse-secondary")
        self.result_label.place(relx=0.5, y=250, anchor=CENTER)

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_initial_ui, bootstyle="danger-outline").place(relx=0.5, y=600, anchor=CENTER)

    def load_images(self):
        # Load and resize images for buttons
        self.rock_img = ImageTk.PhotoImage(Image.open("assets/Screenshot_2024-11-20_090719-removebg-preview.png").resize((150, 150)))
        self.paper_img = ImageTk.PhotoImage(Image.open("assets/Screenshot_2024-11-20_090747-removebg-preview.png").resize((150, 150)))
        self.scissors_img = ImageTk.PhotoImage(Image.open("assets/Screenshot_2024-11-20_090824-removebg-preview.png").resize((150, 150)))

    def send_move(self, move):
        try:
            # Send move to server
            self.client_socket.sendall(move.encode())
            self.result_label.config(text=f"You chose {move}. Waiting for opponent...")
        except BrokenPipeError:
            self.result_label.config(text="Connection lost.")

    def listen_to_server(self):
        # Listen for server responses
        while True:
            try:
                # Receive message from server
                message = self.client_socket.recv(1024).decode()
                self.root.after(0, lambda: self.result_label.config(text=message))
            # Show error if connection is lost
            except ConnectionResetError:
                self.root.after(0, lambda: self.result_label.config(text="Server disconnected."))
                break

    def play_vs_computer(self, player_choice):
        # Determine computer's choice
        self.result_label.config(text="You chose " + player_choice)
        self.animate_choice(player_choice)

    def animate_choice(self, player_choice):
        # Animate the computer's choice
        animation_steps = ["Rock...", "Paper...", "Scissors...","Shoot!"]
        for i, step in enumerate(animation_steps):
            self.root.after(i * 900, lambda s=step: self.result_label.config(text=s))
        self.root.after(len(animation_steps) * 900, lambda: self.show_computer_thinking(player_choice))

    def show_computer_thinking(self, player_choice):
        # Show the computer's choice
        self.result_label.config(text="Computer is thinking...")
        self.root.after(2000, self.show_computer_result, player_choice)

    def determine_winner(self, player_choice, computer_choice):
        # Determine the winner
        if player_choice == computer_choice:
            return "It's a tie!"
        if player_choice == "Rock" and computer_choice == "Scissors":
            return "You win!"
        if player_choice == "Paper" and computer_choice == "Rock":
            return "You win!"
        if player_choice == "Scissors" and computer_choice == "Paper":
            return "You win!"
        return "You lose!"

    def show_error(self, message):
        # Show an error message
        messagebox.showerror("Error", message)

    def show_computer_result(self, player_choice):
        # Show the computer's choice and determine the winner
        computer_choice = random.choice(["Rock", "Paper", "Scissors"])
        result = self.determine_winner(player_choice, computer_choice)
        self.result_label.config(text=f"You chose {player_choice}, Computer chose {computer_choice}. \n\t\t{result}")

# Run the client
if __name__ == "__main__":
    # Create the client window
    root = tb.Window()
    root.resizable(width=False, height=False)
    app = RPSClient(root, None)
    root.mainloop()