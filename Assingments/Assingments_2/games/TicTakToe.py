import ttkbootstrap as tb  # Modern styling
import tk as tk 
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import socket
from threading import Thread
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
        # Add Warp Button

        join_lobby_button = ttk.Button(lobby_frame, text="Join Lobby", command=self.join_lobby, bootstyle="success")
        join_lobby_button.grid(row=1, column=0, columnspan=2, padx=50, pady=20)

        # Back button
        ttk.Button(self.root, text="Back", command=self.create_initial_ui, bootstyle="danger").place(relx=0.5, y=550, anchor=CENTER)

    def create_lobby(self, mode):
        self.lobby_id = f"Lobby{random.randint(1000, 9999)}"
        if self.connect_to_server():
            self.client_socket.sendall(f"CREATE_LOBBY {self.lobby_id} {mode}".encode('utf-8'))
            print(f"Sent CREATE_LOBBY {self.lobby_id} {mode} to server")
            self.player_symbol = "X"
            self.is_my_turn = True
            
            # Set board size based on mode
            board_size = 5 if mode == "blitz" else 3
            self.create_online_ui(board_size)


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

            # Wait for the response from the server about the lobby details
            response = self.client_socket.recv(1024).decode('utf-8')
            if "Board size" in response:
                # Extract the board size from the server response
                board_size = int(response.split(":")[-1].strip())
                self.player_symbol = "O"
                self.is_my_turn = False
                self.create_online_ui(board_size)  # Pass the correct board size to create the UI
            else:
                self.show_error(response)  # Display error if the lobby doesn't exist or the response is not correct


    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect(("localhost", 2341))
            print("Connected to server")
            return True
        except ConnectionError:
            self.show_error("Unable to connect to the server.")
            return False

    def create_online_ui(self, board_size=3):
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

        # Create board with appropriate size
        self.create_board(board_size, board_size)

        # Result label
        self.result_label = ttk.Label(self.root, text="Waiting for result...", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.result_label.place(relx=0.5, y=450, anchor=CENTER)

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

        # Create 3x3 board for the computer mode
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
        if self.is_my_turn and self.buttons[i][j]["text"] == "":
            self.buttons[i][j]["text"] = self.player_symbol
            self.client_socket.sendall(f"MOVE {self.lobby_id} {i},{j},{self.player_symbol}".encode('utf-8'))
            self.is_my_turn = False
            self.update_buttons_state()
            self.check_winner()

    def update_buttons_state(self):
        state = "normal" if self.is_my_turn else "disabled"
        for row in self.buttons:
            for button in row:
                if button["text"] == "":
                    button.config(state=state)

    def update_board(self, i, j, symbol):
        self.buttons[i][j]["text"] = symbol
        self.is_my_turn = (symbol != self.player_symbol)
        self.update_buttons_state()

    def check_winner(self):
        size = len(self.buttons)  # Dynamic board size
        for i in range(size):
            for j in range(size - 3):  # Ensure index j+3 is within bounds
                # Check horizontal
                if self.buttons[i][j]["text"] == self.buttons[i][j+1]["text"] == self.buttons[i][j+2]["text"] == self.buttons[i][j+3]["text"] != "":
                    self.result_label.config(text=f"{self.buttons[i][j]['text']} wins!")
                    return True
                # Check vertical
                if self.buttons[j][i]["text"] == self.buttons[j+1][i]["text"] == self.buttons[j+2][i]["text"] == self.buttons[j+3][i]["text"] != "":
                    self.result_label.config(text=f"{self.buttons[j][i]['text']} wins!")
                    return True

        for i in range(size - 3):
            for j in range(size - 3):  # Ensure diagonal indices are within bounds
                # Check diagonal (top-left to bottom-right)
                if self.buttons[i][j]["text"] == self.buttons[i+1][j+1]["text"] == self.buttons[i+2][j+2]["text"] == self.buttons[i+3][j+3]["text"] != "":
                    self.result_label.config(text=f"{self.buttons[i][j]['text']} wins!")
                    return True
                # Check diagonal (top-right to bottom-left)
                if self.buttons[i][j+3]["text"] == self.buttons[i+1][j+2]["text"] == self.buttons[i+2][j+1]["text"] == self.buttons[i+3][j]["text"] != "":
                    self.result_label.config(text=f"{self.buttons[i][j+3]['text']} wins!")
                    return True

        # Check for a tie
        if all(self.buttons[i][j]["text"] != "" for i in range(size) for j in range(size)):
            self.result_label.config(text="It's a tie!")
            return True

        return False


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