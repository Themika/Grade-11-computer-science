import random
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import time
from threading import Timer

class HighLowGame:
    # Class to manage the High Low Guessing Game
    def __init__(self, root, game_manager):
        self.root = root
        self.game_manager = game_manager
        self.root.geometry("1000x700")
        self.root.title("High Low Guessing Game")
        self.style = tb.Style("superhero")  
        self.timer = None
        self.tooltip = None
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
        normal_button = tb.Button(button_frame, text="Normal", command=self.show_difficulty_options, bootstyle="success-outline", padding=10, width=20)
        normal_button.grid(row=0, column=0, padx=20, pady=10)
        normal_button.bind("<Enter>", lambda e: self.show_tooltip(e, "Normal Mode: Guess the number with no special rules."))
        normal_button.bind("<Leave>", self.hide_tooltip)

        # Timer mode button
        timer_button = tb.Button(button_frame, text="Timer", command=lambda: self.start_game("timer"), bootstyle="warning-outline", padding=10, width=20)
        timer_button.grid(row=0, column=1, padx=20, pady=10)
        timer_button.bind("<Enter>", lambda e: self.show_tooltip(e, "Timer Mode: Guess the number within 30 seconds."))
        timer_button.bind("<Leave>", self.hide_tooltip)

        # Limited guesses mode button
        limited_button = tb.Button(button_frame, text="Limited Guesses", command=lambda: self.start_game("limited"), bootstyle="danger-outline", padding=10, width=20)
        limited_button.grid(row=0, column=2, padx=20, pady=10)
        limited_button.bind("<Enter>", lambda e: self.show_tooltip(e, "Limited Guesses Mode: Guess the number within 10 guesses."))
        limited_button.bind("<Leave>", self.hide_tooltip)

        # Reverse mode button
        reverse_button = tb.Button(button_frame, text="Reverse Mode", command=lambda: self.start_game("reverse"), bootstyle="info-outline", padding=10, width=20)
        reverse_button.grid(row=1, column=0, padx=20, pady=10)
        reverse_button.bind("<Enter>", lambda e: self.show_tooltip(e, "Reverse Mode: The computer tries to guess your number."))
        reverse_button.bind("<Leave>", self.hide_tooltip)

        # Range Shrink mode button
        range_shrink_button = tb.Button(button_frame, text="Range Shrink Mode", command=lambda: self.start_game("range_shrink"), bootstyle="danger-outline", padding=10, width=20)
        range_shrink_button.grid(row=1, column=1, padx=20, pady=10)
        range_shrink_button.bind("<Enter>", lambda e: self.show_tooltip(e, "Range Shrink Mode: The range shrinks after each incorrect guess."))
        range_shrink_button.bind("<Leave>", self.hide_tooltip)

        # Hot and Cold mode button
        hot_cold_button = tb.Button(button_frame, text="Hot and Cold Mode", command=lambda: self.start_game("hot_cold"), bootstyle="primary-outline", padding=10, width=20)
        hot_cold_button.grid(row=1, column=2, padx=20, pady=10)
        hot_cold_button.bind("<Enter>", lambda e: self.show_tooltip(e, "Hot and Cold Mode: Get feedback on how close your guess is."))
        hot_cold_button.bind("<Leave>", self.hide_tooltip)

        back_button = tb.Button(button_frame, text="Back", command=self.game_manager.main_menu, bootstyle="danger-outline", padding=10, width=20)
        back_button.grid(row=2, column=1, padx=50, pady=20)

    def show_tooltip(self, event, text):
        # Show tooltip at the mouse position
        if self.tooltip:
            self.tooltip.destroy()
        self.tooltip = tb.Label(self.root, text=text, font=("Helvetica", 12), bootstyle="info", relief="solid", borderwidth=1, padding=5)
        self.tooltip.place(x=event.widget.winfo_rootx() - self.root.winfo_rootx() + event.widget.winfo_width() - 350, y=event.widget.winfo_rooty() - self.root.winfo_rooty() - 30)

    def hide_tooltip(self, event):
        # Hide the tooltip
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

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
        easy_button = tb.Button(button_frame, text="Easy", command=lambda: self.start_game("easy"), bootstyle="success-outline", padding=10, width=20)
        easy_button.grid(row=0, column=0, padx=20, pady=10)

        # Medium button
        medium_button = tb.Button(button_frame, text="Medium", command=lambda: self.start_game("medium"), bootstyle="warning-outline", padding=10, width=20)
        medium_button.grid(row=0, column=1, padx=20, pady=10)

        # Hard button
        hard_button = tb.Button(button_frame, text="Hard", command=lambda: self.start_game("hard"), bootstyle="danger-outline", padding=10, width=20)
        hard_button.grid(row=0, column=2, padx=20, pady=10)

        # Back button
        back_button = tb.Button(button_frame, text="Back", command=self.create_mode_selection_ui, bootstyle="danger-outline", padding=10, width=20)
        back_button.grid(row=1, column=1, pady=20)

    def start_game(self, mode):
        # Set up the game based on the selected mode
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
        elif mode == "reverse":
            self.range_text = "1 and 100"
            self.min_guess = 1
            self.max_guess = 100
            self.computer_guess = (self.min_guess + self.max_guess) // 2
            self.computer_guesses = []  # Track computer's guesses
        elif mode == "range_shrink":
            self.number_to_guess = random.randint(1, 100)
            self.range_text = "1 and 100"
            self.shrink_factor = 5  # Shrink the range by 5 after each incorrect guess
        elif mode == "hot_cold":
            self.number_to_guess = random.randint(1, 100)
            self.range_text = "1 and 100"
            self.previous_guess = None
        # Initialize game variables
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

        # Result label (created for all modes)
        self.result_label = tb.Label(self.root, text="", font=("Helvetica", 24), bootstyle="inverse-secondary")
        self.result_label.pack(pady=10)

        if self.mode == "reverse":
            # Instructions for reverse mode
            instruction_label = tb.Label(self.root, text=f"Think of a number between {self.range_text}. The computer will try to guess it.", font=("Helvetica", 24))
            instruction_label.pack(pady=10)

            # Computer's guess label
            self.computer_guess_label = tb.Label(self.root, text=f"Computer's guess: {self.computer_guess}", font=("Helvetica", 24), bootstyle="inverse-secondary")
            self.computer_guess_label.pack(pady=10)

            # Buttons for feedback
            button_frame = tb.Frame(self.root, bootstyle="secondary")
            button_frame.place(relx=0.5, rely=0.75, anchor=CENTER)

            too_low_button = tb.Button(button_frame, text="Too Low", command=lambda: self.feedback("low"), bootstyle="warning-outline", padding=10, width=20)
            too_low_button.grid(row=0, column=0, padx=20, pady=10)

            correct_button = tb.Button(button_frame, text="Correct", command=lambda: self.feedback("correct"), bootstyle="success-outline", padding=10, width=20)
            correct_button.grid(row=0, column=1, padx=20, pady=10)

            too_high_button = tb.Button(button_frame, text="Too High", command=lambda: self.feedback("high"), bootstyle="danger-outline", padding=10, width=20)
            too_high_button.grid(row=0, column=2, padx=20, pady=10)

            # Guessed numbers label for reverse mode
            self.computer_guessed_numbers_label = tb.Label(self.root, text="", font=("Helvetica", 24), bootstyle="inverse-secondary", wraplength=900)
            self.computer_guessed_numbers_label.pack(pady=10)

        else:
            # Instructions for normal modes
            instruction_label = tb.Label(self.root, text=f"Guess a number between {self.range_text}:", font=("Helvetica", 24))
            instruction_label.pack(pady=10)

            # Entry
            self.entry = tb.Entry(self.root, font=("Helvetica", 24))
            self.entry.pack(pady=10)

            # Guess button
            guess_button = tb.Button(self.root, text="Guess", command=self.check_guess, bootstyle="primary-outline", width=20)
            guess_button.pack(pady=10)

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
        back_button = tb.Button(self.root, text="Back", command=self.create_mode_selection_ui, bootstyle="danger-outline", width=20)
        back_button.pack(side=BOTTOM, pady=20)
        # Replay button
        replay_button = tb.Button(self.root, text="Replay", command=self.replay_game, bootstyle="info-outline", width=20)
        replay_button.pack(side=BOTTOM,pady=25)


    def replay_game(self):
        self.start_game(self.mode)

    def start_timer(self):
        # Start the timer for timer mode
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Time left: {self.time_left} seconds")
            self.timer = self.root.after(1000, self.start_timer)
        # Time's up
        else:
            self.result_label.config(text="Time's up! You didn't guess the number.", foreground="red")
            self.entry.config(state="disabled")

    def stop_timer(self):
        # Stop the timer if running
        if self.timer:
            self.root.after_cancel(self.timer)
            self.timer = None

    def check_guess(self):
        # Check the user's guess and provide feedback
        try:
            guess = int(self.entry.get())
            # Check if the guess is within the range
            if guess < int(self.range_text.split()[0]) or guess > int(self.range_text.split()[-1]):
                self.result_label.config(text=f"Please enter a number between {self.range_text}.", foreground="red")
                return
            # Update the guessed numbers list
            self.guessed_numbers.append(guess)
            # Provide feedback based on the mode
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
            # Update the guessed numbers label
            if self.mode == "limited":
                self.guesses_left -= 1
                self.guesses_left_label.config(text=f"Guesses left: {self.guesses_left}")
                if self.guesses_left <= 0:
                    self.result_label.config(text="No more guesses left! You didn't guess the number.", foreground="red")
                    self.entry.config(state="disabled")
            # Update the guessed numbers label
            if self.mode == "hot_cold":
                if self.previous_guess is not None:
                    # Provide feedback based on how close the guess is
                    if abs(self.number_to_guess - guess) < abs(self.number_to_guess - self.previous_guess):
                        self.result_label.config(text="Hot!", foreground="red")
                    else:
                        self.result_label.config(text="Cold!", foreground="blue")
                self.previous_guess = guess
            # Update the guessed numbers label
            if self.mode == "range_shrink":
                self.range_text = f"{max(1, guess - self.shrink_factor)} and {min(100, guess + self.shrink_factor)}"
                self.result_label.config(text=f"Range shrunk! New range: {self.range_text}", foreground="purple")
        # Handle invalid input
        except ValueError:
            self.result_label.config(text="Please enter a valid number.", foreground="red")

    def feedback(self, feedback_type):
        # Provide feedback to the computer based on the user's response
        self.computer_guesses.append(self.computer_guess)  # Track the computer's guess
        # Update the guessed numbers label
        if feedback_type == "low":
            self.min_guess = self.computer_guess + 1
        elif feedback_type == "high":
            self.max_guess = self.computer_guess - 1
        elif feedback_type == "correct":
            self.result_label.config(text="The computer guessed your number!", foreground="green")
            self.update_computer_guessed_numbers_label()
            return
        # Update the computer's guess
        self.computer_guess = (self.min_guess + self.max_guess) // 2
        self.computer_guess_label.config(text=f"Computer's guess: {self.computer_guess}")

    def update_guessed_numbers_label(self):
        # Update the guessed numbers label
        guessed_numbers_text = f"Guessed numbers: {', '.join(map(str, self.guessed_numbers))}"
        font_size = max(10, 24 - len(self.guessed_numbers) // 2)  # Decrease font size as more numbers are guessed
        self.guessed_numbers_label.config(text=guessed_numbers_text, font=("Helvetica", font_size))

    def update_computer_guessed_numbers_label(self):
        # Update the computer's guessed numbers label
        computer_guessed_numbers_text = f"Computer's guesses: {', '.join(map(str, self.computer_guesses))}"
        self.computer_guessed_numbers_label.config(text=computer_guessed_numbers_text)

if __name__ == "__main__":
    # Run the game
    root = tb.Window(themename="superhero")
    root.resizable(False, False)
    game = HighLowGame(root, None)
    root.mainloop()