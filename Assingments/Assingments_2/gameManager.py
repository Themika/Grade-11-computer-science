import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from games.RPS import RPSClient
from games.TicTakToe import TicTacToe

class GameManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Manager")
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
        
        self.game1_button = ttk.Button(button_frame, text="Mini Game 1", command=self.start_game1, bootstyle="primary")
        self.game1_button.place(x=0, y=0, width=button_width, height=100)
        
        self.game2_button = ttk.Button(button_frame, text="Mini Game 2", command=self.start_game2, bootstyle="success")
        self.game2_button.place(x=button_width, y=0, width=button_width, height=100)
        
        self.game3_button = ttk.Button(button_frame, text="Mini Game 3", command=self.start_game3, bootstyle="info")
        self.game3_button.place(x=2 * button_width, y=0, width=button_width, height=100)
        
        self.back_button = ttk.Button(button_frame, text="Back to Main Menu", command=self.main_menu, bootstyle="danger")
        self.back_button.place(x=button_width, y=0, width=button_width, height=100)
        self.back_button.place_forget()  # Hide the back button initially

        # Initialize labels for game title and placeholder text
        self.game_title_label = None
        self.placeholder_label = None

    def start_game1(self):
        self.show_game_ui("Mini Game 1")
        self.rps_client = RPSClient(self.root)

    def start_game2(self):
        self.show_game_ui("Mini Game 2")
        self.tic_tac_toe_client = TicTacToe(self.root)

    def start_game3(self):
        self.show_game_ui("Mini Game 3")

    def main_menu(self):
        self.show_main_ui()

    def show_main_ui(self):
        self.game1_button.place(x=0, y=0, width=1000 // 3, height=100)
        self.game2_button.place(x=1000 // 3, y=0, width=1000 // 3, height=100)
        self.game3_button.place(x=2 * 1000 // 3, y=0, width=1000 // 3, height=100)
        self.back_button.place_forget()
        
        # Hide game title and placeholder labels if they exist
        if self.game_title_label:
            self.game_title_label.place_forget()
        if self.placeholder_label:
            self.placeholder_label.place_forget()

    def show_game_ui(self, game_title):
        self.game1_button.place_forget()
        self.game2_button.place_forget()
        self.game3_button.place_forget()
        self.back_button.place(x=1000 // 3, y=0, width=1000 // 3, height=100)
        
        # Game title
        self.game_title_label = ttk.Label(self.root, text=game_title, font=("Helvetica", 36), bootstyle="inverse-primary")
        self.game_title_label.place(relx=0.5, y=150, anchor=CENTER)
        
        # Placeholder text
        self.placeholder_label = ttk.Label(self.root, text="Game content goes here!", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.placeholder_label.place(relx=0.5, y=250, anchor=CENTER)

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    game_manager = GameManager(root)
    root.mainloop()