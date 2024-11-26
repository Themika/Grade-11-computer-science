import ttkbootstrap as tb  # Modern styling
import tk as tk 
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import socket
from threading import Thread, Timer
import random

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.geometry("800x600")
        self.root.title("Tic Tac Toe")
        self.style = ttk.Style("superhero")
        self.client_socket = None
        self.lobby_id = None
        self.player_symbol = None
        self.is_my_turn = False
        self.timer = None
        self.time_remaining = 30
        self.timer_started = False
        self.board_size = (3, 3)  # Default board size
        self.create_initial_ui()

    def create_initial_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Tic Tac Toe", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Mode selection
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        online_button = ttk.Button(button_frame, text="Online", command=self.show_lobby_options, bootstyle="primary")
        online_button.grid(row=0, column=0, padx=50, pady=20)

        computer_button = ttk.Button(button_frame, text="Computer", command=self.start_computer, bootstyle="success")
        computer_button.grid(row=0, column=1, padx=50, pady=20)

    def show_lobby_options(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Tic Tac Toe - Online", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Lobby options
        lobby_frame = ttk.Frame(self.root, bootstyle="secondary")
        lobby_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        create_lobby_1v1_button = ttk.Button(lobby_frame, text="Create 1v1 Lobby", command=lambda: self.create_lobby("1v1"), bootstyle="primary")
        create_lobby_1v1_button.grid(row=0, column=0, padx=50, pady=20)

        create_lobby_blitz_button = ttk.Button(lobby_frame, text="Create Blitz Lobby", command=lambda: self.create_lobby("blitz"), bootstyle="primary")
        create_lobby_blitz_button.grid(row=0, column=1, padx=50, pady=20)

        join_lobby_button = ttk.Button(lobby_frame, text="Join Lobby", command=self.join_lobby, bootstyle="success")
        join_lobby_button.grid(row=1, column=0, columnspan=2, padx=50, pady=20)

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_initial_ui, bootstyle="danger").place(relx=0.5, y=550, anchor=CENTER)

    def create_lobby(self, mode):
        self.lobby_id = f"Lobby{random.randint(1000, 9999)}"
        self.board_size = (3, 3) if mode == "1v1" else (5, 5)  # Ensure the board size is set correctly
        if self.connect_to_server():
            self.client_socket.sendall(f"CREATE_LOBBY {self.lobby_id} {mode}".encode('utf-8'))
            print(f"Sent CREATE_LOBBY {self.lobby_id} {mode} to server")
            self.player_symbol = "X"
            self.is_my_turn = True
            self.create_online_ui()

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
        join_button = ttk.Button(self.root, text="Join", command=self.join_existing_lobby, bootstyle="primary")
        join_button.place(relx=0.5, y=300, anchor=CENTER)

        # Back button
        ttk.Button(self.root, text="Back", command=self.show_lobby_options, bootstyle="danger").place(relx=0.5, y=550, anchor=CENTER)

    def join_existing_lobby(self):
        self.lobby_id = self.lobby_id_entry.get()
        if self.connect_to_server():
            self.client_socket.sendall(f"JOIN_LOBBY {self.lobby_id}".encode('utf-8'))
            print(f"Sent JOIN_LOBBY {self.lobby_id} to server")
            self.player_symbol = "O"
            self.is_my_turn = False
            # Wait for the server to send the board size
            board_size_message = self.client_socket.recv(1024).decode()
            if board_size_message.startswith("BOARD_SIZE"):
                _, size = board_size_message.split()
                self.board_size = (int(size), int(size))
            self.create_online_ui()

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", 2341))
            print("Connected to server")
            return True
        except ConnectionError:
            self.show_error("Unable to connect to the server.")
            return False

    def create_online_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Tic Tac Toe - Online", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Lobby ID display
        lobby_id_label = ttk.Label(self.root, text=f"Lobby ID: {self.lobby_id}", font=("Helvetica", 24))
        lobby_id_label.place(relx=0.5, y=150, anchor=CENTER)

        # Instructions
        instruction_label = ttk.Label(self.root, text="Choose your move:", font=("Helvetica", 24))
        instruction_label.place(relx=0.5, y=200, anchor=CENTER)

        # Create board
        self.create_board(*self.board_size)

        # Result label
        self.result_label = ttk.Label(self.root, text="Waiting for result...", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.result_label.place(relx=0.5, y=450, anchor=CENTER)

        # Timer label and start button for Blitz mode
        if self.board_size == (5, 5):
            self.timer_label = ttk.Label(self.root, text=f"Time remaining: {self.time_remaining} seconds", font=("Helvetica", 24), bootstyle="inverse-secondary")
            self.timer_label.place(relx=0.85, rely=0.2, anchor=CENTER)
            self.start_timer_button = ttk.Button(self.root, text="Start Timer", command=self.start_timer, bootstyle="warning")
            self.start_timer_button.place(relx=0.85, rely=0.3, anchor=CENTER)

        # Start thread to listen for server responses
        self.listener_thread = Thread(target=self.listen_to_server, daemon=True)
        self.listener_thread.start()

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_initial_ui, bootstyle="danger").place(relx=0.5, y=550, anchor=CENTER)

    def start_computer(self):
        self.create_computer_ui()

    def create_computer_ui(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Tic Tac Toe", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Create board
        self.create_board(3, 3)

        # Result label
        self.result_label = ttk.Label(self.root, text="Choose your move to play!", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.result_label.place(relx=0.5, y=450, anchor=CENTER)

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_initial_ui, bootstyle="danger").place(relx=0.5, y=550, anchor=CENTER)

        self.is_my_turn = True
        self.player_symbol = "X"

    def create_board(self, length, width):
        self.board_frame = ttk.Frame(self.root, bootstyle="secondary")
        self.board_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.buttons = []
        for i in range(length):
            row = []
            for j in range(width):
                button = ttk.Button(self.board_frame, text="", command=lambda i=i, j=j: self.make_move(i, j), bootstyle="primary", width=10)
                button.grid(row=i, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

    def make_move(self, i, j):
        if self.is_my_turn and self.buttons[i][j]["text"] == "" and self.timer_started:
            self.buttons[i][j]["text"] = self.player_symbol
            self.client_socket.sendall(f"MOVE {self.lobby_id} {i},{j},{self.player_symbol}".encode('utf-8'))
            self.is_my_turn = False
            self.update_buttons_state()
            self.check_winner()

    def start_timer(self):
        self.timer_started = True
        self.start_timer_button.config(state="disabled")
        self.update_buttons_state()
        self.timer = Timer(1.0, self.update_timer)
        self.timer.start()

    def update_timer(self):
        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.timer_label.config(text=f"Time remaining: {self.time_remaining} seconds")
            self.timer = Timer(1.0, self.update_timer)
            self.timer.start()
        else:
            self.timer_started = False
            self.timer_label.config(text="Time's up!")
            self.update_buttons_state()

    def update_buttons_state(self):
        state = "normal" if self.is_my_turn and self.timer_started else "disabled"
        for row in self.buttons:
            for button in row:
                if button["text"] == "":
                    button.config(state=state)

    def update_board(self, i, j, symbol):
        self.buttons[i][j]["text"] = symbol
        self.is_my_turn = (symbol != self.player_symbol)
        self.update_buttons_state()

    def check_winner(board):
        size = len(board)
        win_length = 5 if size == 5 else 3  # Set win length based on board size

        # Check rows
        for row in board:
            for i in range(size - win_length + 1):
                if all(cell == row[i] != '' for cell in row[i:i+win_length]):
                    return row[i]

        # Check columns
        for col in range(size):
            for i in range(size - win_length + 1):
                if all(board[row][col] == board[i][col] != '' for row in range(i, i+win_length)):
                    return board[i][col]

        # Check diagonals
        for i in range(size - win_length + 1):
            for j in range(size - win_length + 1):
                if all(board[i+k][j+k] == board[i][j] != '' for k in range(win_length)):
                    return board[i][j]
                if all(board[i+k][j+win_length-1-k] == board[i][j+win_length-1] != '' for k in range(win_length)):
                    return board[i][j+win_length-1]

        # Check for tie
        if all(board[i][j] != '' for i in range(size) for j in range(size)):
            return 'Tie'
        return None

    def listen_to_server(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                print(f"Received message from server: {message}")
                if message.startswith("MOVE"):
                    _, move = message.split()
                    i, j, symbol = move.split(',')
                    self.update_board(int(i), int(j), symbol)
                elif message.startswith("WINNER"):
                    winner = message.split()[1]
                    if winner == 'Tie':
                        self.result_label.config(text="It's a tie!")
                    else:
                        self.result_label.config(text=f"{winner} wins!")
                    # Disable further moves after game ends
                    self.update_buttons_state()
            except ConnectionResetError:
                self.result_label.config(text="Server disconnected.")
                break

    def show_error(self, message):
        error_label = ttk.Label(self.root, text=message, font=("Helvetica", 16), bootstyle="danger")
        error_label.place(relx=0.5, y=550, anchor=CENTER)

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = TicTacToe(root)
    root.mainloop()