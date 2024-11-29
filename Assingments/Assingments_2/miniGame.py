import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from games.RPS import RPSClient
from games.TicTakToe import TicTacToe
from games.highLowGame import HighLowGame

"""
    This program is a game manager that allows the user to play three different games: Rock Paper Scissors, Tic Tac Toe, and High Low Game.
    The user can navigate between the games and return to the main menu at any time. 

    Instructions
    ----------------------------
        - First in terminal run the server.py file to start the servers.
        - Then run the game manager file.
        - Click on the game you want to play.
    
    Online Modes
    ----------------------------
        - Rock Paper Scissors and Tic Tac Toe have online multiplayer modes.
        - The user can play against another player by connecting to the server.
        - FIrst create the lobby 
        - Run another Game Manager instance and join the lobby by entering the lobby id. The id should have Lobbyxxxx format.
        - Play the game with the other players.
    
    Features
    ----------------------------
        - Rock Paper Scissors
        - Tic Tac Toe
        - High Low Game
        - Multiplayer options for all games
        - Fun extra game modes
        - Visually appealing interface
    
    Improvements
    ----------------------------
    - Add more games to the game manager.
"""


class GameManager:
    # Initialize the game manager
    def __init__(self, root):
        self.root = root
        self.root.title("Game Manager")
        self.root.resizable(False, False)
        self.create_ui()
        self.width = 1000

    def create_ui(self):
        self.root.geometry(f"1000x600")
        
        # Title
        title_label = ttk.Label(self.root, text="Game Manager", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)
        
        # Buttons
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=1.0, anchor=S, width=1000, height=100)
        
        button_width = 1000 // 3  # Each button's width is a third of the screen width
        # Initialize buttons for each game
        self.game1_button = ttk.Button(button_frame, text="Rock Paper Scissors", command=self.start_game1, bootstyle="primary")
        self.game1_button.place(x=0, y=0, width=button_width, height=100)
        # Hide the buttons initially
        self.game2_button = ttk.Button(button_frame, text="Tic Tac Toe", command=self.start_game2, bootstyle="success")
        self.game2_button.place(x=button_width, y=0, width=button_width, height=100)
        
        self.game3_button = ttk.Button(button_frame, text="High Low Game", command=self.start_game3, bootstyle="info")
        self.game3_button.place(x=2 * button_width, y=0, width=button_width, height=100)
        
        self.back_button = ttk.Button(button_frame, text="Back to Main Menu", command=self.main_menu, bootstyle="danger")
        self.back_button.place(x=button_width, y=0, width=button_width, height=100)
        self.back_button.place_forget()  # Hide the back button initially

        # Initialize labels for game title and placeholder text
        self.game_title_label = None
        self.placeholder_label = None
    
    def start_game1(self):
        # Start Rock Paper Scissors game
        self.rps_client = RPSClient(self.root, self)

    def start_game2(self):
        # Start Tic Tac Toe game
        self.tic_tac_toe_client = TicTacToe(self.root, self)

    def start_game3(self):
        # Start High Low Game
        self.higher_lower_client = HighLowGame(self.root, self)

    def main_menu(self):
        # Return to the main menu
        self.show_main_ui()

    def show_main_ui(self):
        self.root.geometry(f"1000x600")
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = ttk.Label(self.root, text="Game Manager", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.place(relx=0.5, y=50, anchor=CENTER)

        # Buttons
        button_frame = ttk.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=1.0, anchor=S, width=1000, height=100)

        button_width = 1000 // 3  # Each button's width is a third of the screen width
        # Initialize buttons for each game
        game1_button = ttk.Button(button_frame, text="Rock Paper Scissors", command=self.start_game1, bootstyle="primary")
        game1_button.place(x=0, y=0, width=button_width, height=100)
        # Hide the buttons initially
        game2_button = ttk.Button(button_frame, text="Tic Tac Toe", command=self.start_game2, bootstyle="success")
        game2_button.place(x=button_width, y=0, width=button_width, height=100)

        game3_button = ttk.Button(button_frame, text="High Low Game", command=self.start_game3, bootstyle="info")
        game3_button.place(x=2 * button_width, y=0, width=button_width, height=100)

    def show_game_ui(self, game_title):
        # Safely handle widgets to avoid errors
        try:
            self.game1_button.place_forget()
            self.game2_button.place_forget()
            self.game3_button.place_forget()
        except AttributeError:
            # Buttons might not be initialized; skip
            pass

        # Adjust back button position for High Low Game
        if game_title == "High Low Game":
            self.back_button.place(x=2 * 1000 // 3 + 50, y=0, width=1000 // 3, height=100)
        else:
            self.back_button.place(x=1000 // 3, y=0, width=1000 // 3, height=100)

        # Display game-specific UI
        # Remove any existing labels to prevent overlapping
        if self.game_title_label:
            self.game_title_label.destroy()
        if self.placeholder_label:
            self.placeholder_label.destroy()

        # Game title
        self.game_title_label = ttk.Label(self.root, text=game_title, font=("Helvetica", 36), bootstyle="inverse-primary")
        self.game_title_label.place(relx=0.5, y=150, anchor=CENTER)

        # Placeholder text
        self.placeholder_label = ttk.Label(self.root, text="Game content goes here!", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.placeholder_label.place(relx=0.5, y=250, anchor=CENTER)

if __name__ == "__main__":
    # Start the game manager
    root = ttk.Window(themename="superhero")
    game_manager = GameManager(root)
    root.mainloop()