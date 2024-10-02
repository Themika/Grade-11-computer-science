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
    display_lines = [r"__        __   _                            _                           ",
                     r"\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___    _ __ ___  _   _  ",
                     r" \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | '_ ` _ \| | | | ",
                     r"  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | | | | | | |_| | ",
                     r"   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_| |_| |_|\__, | ",
                     r"            | '_ \| '__/ _ \ / _` | '__/ _` | '_ ` _ \           |___/  ",
                     r"            | |_) | | | (_) | (_| | | | (_| | | | | | |                 ",
                     r"            | .__/|_|  \___/ \__, |_|  \__,_|_| |_| |_|                ",
                     r"            |_|              |___/                                     "
                     ]
    for line in display_lines:
        ghostWriter(f"{green}{line}\n", 0.005)

# Currency denominations and their names
money_map = {
    50: "Fifty Dollars bills",
    20: "Twenty Dollars bills",
    10: "Ten Dollars bills",
    5: "FiveDollars bills",
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
    for value in money_map.keys():
        count = int(amount // value)  # Get the number of times a denomination fits into the amount
        if count > 0:
            change[money_map[value]] = count
            amount = round(amount - count * value, 2)  # Subtract the value and round to avoid floating-point issues

    # Display the change
    ghostWriter("\nHere is your change:\n", 0.05)
    for denomination, count in change.items():
        print(f"{denomination}: {count}")

# Runs the main method continuously
if __name__ == "__main__":
    while True:
        main()
        # Ask user if they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)? ", 0.05)
        continue_response = input().lower().strip()
        if continue_response == "no":
            exit()
        elif continue_response != "yes":
            ghostWriter("Invalid input! Please enter yes or no.\n", 0.05)

