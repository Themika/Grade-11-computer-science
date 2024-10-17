from time import sleep

"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program is a simple progarm that will allow a user to choose from various interior paint options. Then give you a invoince on the cost
of painting the room. Proviiding you with 2 payemnet options. 
"""
#IDEA
#All the typical things
#Add a emailing system 
#credit card system
#Add ui maybe

# ANSI color for output
white = "\033[1;37m"
green  = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)
def get_string_input(idea,prompt):
    # Get a string value from the user
    while True:
        try:
            ghostWriter(idea, 0.05)
            value = str(input(prompt).strip())
            return value
        except ValueError:
            print(f"{red}ERROR: {white}Enter a valid string.")
def get_integer_input(idea,prompt):
    # Get a string value from the user
    while True:
        try:
            ghostWriter(idea, 0.05)
            value = int(input(prompt).strip())
            return value
        except ValueError:
            print(f"{red}ERROR: {white}Enter a valid string.")
def display_program():
    # Display the program name
    display_lines = [
                        r"                     ____          _                      ____       _       _         ",
                        r"                    / ___|___  ___| |_   _ __  ___ _ __  |  _ \ __ _(_)_ __ | |_       ",
                        r"                   | |   / _ \/ __| __|| '_ \ / _ \ '__| | |_) / _` | | '_ \| __|      ",
                        r"                   | |__| (_) \__ \ |_ | |_) |  __/ |    |  __/ (_| | | | | | |_       ",
                        r"                    \____\___/|___/\__|| .__/\___|_|     |_|   \__,_|_|_| |_|\__|       ",
                        r"                                     __|_|  _           _                             ",
                        r"                                     |  ___(_)_ __   __| | ___ _ __                    ",
                        r"                                     | |_  | | '_ \ / _` |/ _ \ '__|                   ",
                        r"                                     |  _| | | | | | (_| |  __/ |                      ",
                        r"                                     |_|   |_|_| |_|\__,_|\___|_|                      "  
                     ]
    # Display the program name
    for line in display_lines:
        ghostWriter(f"{green}{line}\n", 0.005)
def run_program():
    # This handles the display method checking whether the user wants to see it again for future runs
    global displayed, run_count, skip_display
    if not displayed or (run_count >= 0 and not skip_display):
        display_program()
        displayed = True
        run_count += 1
        # Checks if the code has run once
        if run_count == 1:
            # Checks if the user wants to skip
            ghostWriter(f"\n{white}Would you like to skip the display in future runs (yes/no)?\n", 0.05)
            skip_display_input = input().lower().strip()
            while True:
                # Checks if the input is yes or no
                if skip_display_input == "yes":
                    skip_display = True
                    break
                elif skip_display_input == "no":
                    break
                else:
                    ghostWriter(f"{red}ERROR: {white}Invalid input! Please enter yes or no.\n", 0.05)
                    skip_display_input = input().lower().strip()

def process_room(room_number,areas):
    total_area = 0
    for i in range(room_number):
        length = get_integer_input(f"{white}Enter the dimensions of room {i + 1} (length): ", f"{blue}")
        width = get_integer_input(f"{white}Enter the dimensions of room {i + 1} (width): ", f"{blue}")
        areas.append(length * width)
        total_area += areas[i]
    for i in range(len(areas)):
        ghostWriter(f"{green}Room {i + 1} area: {areas[i]}\n", 0.05)
    ghostWriter(f"{green}Total area: {total_area}\n", 0.05)

def process_tax(total_area,paints):
    pass

def main():
    run_program()
    # Display the program name
    areas = []
    values = []
    paints = {
        "Custom Paint"  : 250,
        "Luxury Paint"  : 200,
        "Designer Paint": 150,
        "Premium Paint" : 105,
        "Low Odor Paint": 90,
        "Regular Paint" : 75,
        "Value paint"   : 40,

    }
    ghostWriter(f"{green}Welcome to the Paint Program!\n", 0.05)
    # Get the user's name
    name = get_string_input(f"{white}Enter your name: ", f"{blue}")
    values.append(name)
    # Get the amount of rooms
    room_amount = get_integer_input(f"{white}Enter the number of rooms you would like to paint: ", f"{blue}")
    values.append(room_amount)
    process_room(room_amount,areas)

    

# Runs the main method continuously
if __name__ == "__main__":
    displayed = False
    run_count = 0
    skip_display = False
    while True:
        main()
        # Checks for the user's input on whether they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        # Checks for the user's input
        continue_choice = input().lower().strip()
        # Ends the code 
        if continue_choice == "no":
            exit()
        # Checks if the answer is not yes or no
        elif continue_choice != "yes":
            ghostWriter(f"{red}ERROR: {white}Invalid input! Please enter yes or no.\n", 0.05)
            break