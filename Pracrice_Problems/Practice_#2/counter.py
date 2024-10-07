from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"
# Ghost writer method
def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def get_float(prompt):
    # Get a floating-point value from the user
    while True:
        try:
            value = float(input(prompt).strip())
            return value
        except ValueError:
            print(f"{red}ERROR: {white}Enter a valid number.")

def count_between(start, end):
    if start < end:
        step = 1
    else:
        step = -1

    for value in range(int(start), int(end) + step, step):
        ghostWriter(f"{value}\n", 0.05)

def main():
    ghostWriter("Enter the first number: ", 0.05)
    first_number = get_float("")
    ghostWriter("Enter the second number: ", 0.05)
    second_number = get_float("")
    count_between(first_number, second_number)

# Runs the main method continuously
if __name__ == "__main__":
    while True:
        main()
        # Checks for the user's input on whether they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        continue_choice = input().lower().strip()
        if continue_choice == "no":
            exit()
        elif continue_choice != "yes":
            ghostWriter(f"{white}Invalid input! Please enter yes or no.\n", 0.05)