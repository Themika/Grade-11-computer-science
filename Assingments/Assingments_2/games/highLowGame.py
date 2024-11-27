import random
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import time
from threading import Timer

class HighLowGame:
    def __init__(self, root,game_manager):
        self.root = root
        self.game_manager = game_manager
        self.root.geometry("1000x650")
        self.root.title("High Low Guessing Game")
        self.style = tb.Style("superhero")  
        self.timer = None
        self.create_mode_selection_ui()

    def create_mode_selection_ui(self):
        # Clear existing widgets and stop the timer if running
        self.stop_timer()
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = tb.Label(self.root, text="High Low Guessing Game", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.pack(pady=20)

        # Instructions
        instruction_label = tb.Label(self.root, text="Select a game mode:", font=("Helvetica", 24))
        instruction_label.pack(pady=10)

        # Button frame
        button_frame = tb.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Normal mode button
        normal_button = tb.Button(button_frame, text="Normal", command=self.show_difficulty_options, bootstyle="success-outline", padding=10,width=20)
        normal_button.grid(row=0, column=0, padx=10,pady=20)

        # Timer mode button
        timer_button = tb.Button(button_frame, text="Timer", command=lambda: self.start_game("timer"), bootstyle="warning-outline", padding=10,width=20)
        timer_button.grid(row=0, column=1, padx=10,pady=20)

        # Limited guesses mode button
        limited_button = tb.Button(button_frame, text="Limited Guesses", command=lambda: self.start_game("limited"), bootstyle="danger-outline", padding=10,width=20)
        limited_button.grid(row=0, column=2, padx=10,pady=20)

        back_button = tb.Button(button_frame, text="Back", command=self.game_manager.main_menu, bootstyle="danger-outline",width=20)
        back_button.grid(row=2, column=1, padx=50, pady=20)

    def show_difficulty_options(self):
        # Clear existing widgets and stop the timer if running
        self.stop_timer()
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = tb.Label(self.root, text="Select Difficulty", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.pack(pady=20)

        # Button frame
        button_frame = tb.Frame(self.root, bootstyle="secondary")
        button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Easy button
        easy_button = tb.Button(button_frame, text="Easy", command=lambda: self.start_game("easy"), bootstyle="success-outline", padding=10,width=20)
        easy_button.grid(row=0, column=0, padx=10,pady=20)

        # Medium button
        medium_button = tb.Button(button_frame, text="Medium", command=lambda: self.start_game("medium"), bootstyle="warning-outline", padding=10,width=20)
        medium_button.grid(row=0, column=1, padx=10,pady=20)

        # Hard button
        hard_button = tb.Button(button_frame, text="Hard", command=lambda: self.start_game("hard"), bootstyle="danger-outline", padding=10,width=20)
        hard_button.grid(row=0, column=2, padx=10,pady=20)

        # Back button
        back_button = tb.Button(button_frame, text="Back", command=self.create_mode_selection_ui, bootstyle="danger-outline", padding=10,width=20)
        back_button.grid(row=1, column=1, pady=20)

    def start_game(self, mode):
        self.mode = mode
        if mode == "easy":
            self.number_to_guess = random.randint(1, 20)
            self.range_text = "1 and 20"
        elif mode == "medium":
            self.number_to_guess = random.randint(1, 100)
            self.range_text = "1 and 100"
        elif mode == "hard":
            self.number_to_guess = random.randint(1, 1000)
            self.range_text = "1 and 1000"
        elif mode == "timer":
            self.number_to_guess = random.randint(1, 100)
            self.range_text = "1 and 100"
            self.time_left = 30  # 30 seconds timer
        elif mode == "limited":
            self.number_to_guess = random.randint(1, 100)
            self.range_text = "1 and 100"
            self.guesses_left = 10  # 10 guesses limit
        self.guessed_numbers = []
        self.too_low_count = 0
        self.too_high_count = 0
        self.create_game_ui()

    def create_game_ui(self):
        # Clear existing widgets and stop the timer if running
        self.stop_timer()
        for widget in self.root.winfo_children():
            widget.destroy()

        # Title
        title_label = tb.Label(self.root, text="High Low Guessing Game", font=("Helvetica", 48), bootstyle="inverse-primary")
        title_label.pack(pady=20)

        # Instructions
        instruction_label = tb.Label(self.root, text=f"Guess a number between {self.range_text}:", font=("Helvetica", 24))
        instruction_label.pack(pady=10)

        # Entry
        self.entry = tb.Entry(self.root, font=("Helvetica", 24))
        self.entry.pack(pady=10)

        # Guess button
        guess_button = tb.Button(self.root, text="Guess", command=self.check_guess, bootstyle="primary-outline",width=20)
        guess_button.pack(pady=10)

        # Result label
        self.result_label = tb.Label(self.root, text="", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.result_label.pack(pady=10)

        # Guessed numbers label (initially hidden)
        self.guessed_numbers_label = tb.Label(self.root, text="", font=("Helvetica", 24), bootstyle="inverse-secondary", wraplength=900)
        self.guessed_numbers_label.pack(pady=10)

        # Too low count label
        self.too_low_label = tb.Label(self.root, text="", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.too_low_label.pack(side=LEFT, padx=20)

        # Too high count label
        self.too_high_label = tb.Label(self.root, text="", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.too_high_label.pack(side=RIGHT, padx=20)

        # Timer label for timer mode
        if self.mode == "timer":
            self.timer_label = tb.Label(self.root, text=f"Time left: {self.time_left} seconds", font=("Helvetica", 24), bootstyle="inverse-secondary")
            self.timer_label.pack(pady=10)
            self.start_timer()

        # Guesses left label for limited guesses mode
        if self.mode == "limited":
            self.guesses_left_label = tb.Label(self.root, text=f"Guesses left: {self.guesses_left}", font=("Helvetica", 24), bootstyle="inverse-secondary")
            self.guesses_left_label.pack(pady=10)

        # Back button
        back_button = tb.Button(self.root, text="Back", command=self.create_mode_selection_ui, bootstyle="danger-outline",width=20)
        back_button.pack(pady=20)

    def start_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.timer = self.root.after(1000, self.start_timer)
        else:
            self.result_label.config(text="Time's up! You didn't guess the number.", foreground="red")
            self.entry.config(state="disabled")

    def stop_timer(self):
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

    def check_guess(self):
        try:
            guess = int(self.entry.get())
            self.guessed_numbers.append(guess)
            if guess < self.number_to_guess:
                self.too_low_count += 1
                self.result_label.config(text=f"Too low! Try again.", foreground="red")
                self.too_low_label.config(text=f"Too low count: {self.too_low_count}", foreground="red")
            elif guess > self.number_to_guess:
                self.too_high_count += 1
                self.result_label.config(text=f"Too high! Try again.", foreground="orange")
                self.too_high_label.config(text=f"Too high count: {self.too_high_count}", foreground="orange")
            else:
                self.result_label.config(text="Congratulations! You guessed it!", foreground="green")
                self.update_guessed_numbers_label()
                self.entry.config(state="disabled")
                self.stop_timer()
                return

            if self.mode == "limited":
                self.guesses_left -= 1
                self.guesses_left_label.config(text=f"Guesses left: {self.guesses_left}")
                if self.guesses_left <= 0:
                    self.result_label.config(text="No more guesses left! You didn't guess the number.", foreground="red")
                    self.entry.config(state="disabled")

        except ValueError:
            self.result_label.config(text="Please enter a valid number.", foreground="red")

    def update_guessed_numbers_label(self):
        guessed_numbers_text = f"Guessed numbers: {', '.join(map(str, self.guessed_numbers))}"
        font_size = max(10, 24 - len(self.guessed_numbers) // 2)  # Decrease font size as more numbers are guessed
        self.guessed_numbers_label.config(text=guessed_numbers_text, font=("Helvetica", font_size))

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    game = HighLowGame(root)
    root.mainloop()