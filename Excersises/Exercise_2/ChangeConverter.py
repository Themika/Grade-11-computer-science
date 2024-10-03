from time import sleep

# ANSI color for output
white = "\033[1;37m"
green  = "\033[0;32m"
# Ghost writer method
def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def display_program():
    # Display the program name
    display_lines = [
                        r"__        __   _                            _                           ",
                        r"\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___    _ __ ___  _   _  ",
                        r" \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | '_ ` _ \| | | | ",
                        r"  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | | | | | | |_| | ",
                        r"   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_| |_| |_|\__, | ",
                        r"            | '_ \| '__/ _ \ / _` | '__/ _` | '_ ` _ \           |___/  ",
                        r"            | |_) | | | (_) | (_| | | | (_| | | | | | |                 ",
                        r"            | .__/|_|  \___/ \__, |_|  \__,_|_| |_| |_|                ",
                        r"            |_|              |___/                                     "
                     ]
    # Display the program name
    for line in display_lines:
        ghostWriter(f"{green}{line}\n", 0.005)

# Currency change and their names
money_map = {
    50: "Fifty Dollar bills",
    20: "Twenty Dollar bills",
    10: "Ten Dollar bills",
    5: "Five Dollar bills",
    2: "Toonies",
    1: "Loonies",
    0.25: "Quarters",
    0.10: "Dimes",
    0.05: "Nickels",
    0.01: "Pennies",
}

# Function to get a valid positive floating point value
def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if 0 < value <= 100:
                return value
            else:
                print("ERROR: Enter a value between $0 and $100.")
        except ValueError:
            print("ERROR: Enter a valid floating-point number.")

# Main logic to calculate and display change
def main():
    display_program()
    amount = get_positive_float("Please enter a dollar amount between $0 and $100: ")

    change = {}
    # Iterate through the changes
    for value in money_map.keys():
        count = int(amount // value)  # Get the number of times a change fits into the amount
        if count > 0:
            # Add the change to the change dictionary
            change[money_map[value]] = count # Add the change to the change dictionary
            amount = round(amount - count * value, 2)  # Subtract the value and round to avoid floating-point issues

    # Display the change
    ghostWriter("\nHere is your change:\n", 0.05)
    for change, count in change.items():
        print(f"{change}: {count}")

# Runs the main method continuously
if __name__ == "__main__":
    while True:
        main()
        # Ask user if they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)? ", 0.05)
        continue_response = input().lower().strip()
        # Exit if the user does not want to continue
        if continue_response != "yes":
            # Exit if the user does not want to continue
            if continue_response != "no":
                ghostWriter("Invalid input! Please enter yes or no.\n", 0.05)
            exit()

