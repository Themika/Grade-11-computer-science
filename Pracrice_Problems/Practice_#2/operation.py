from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def get_float(prompt):
    # Get a positive floating-point value from the user
    while True:
        try:
            value = float(input(prompt).strip())
            return value
        except ValueError:
            print(f"{red}ERROR: {white}Enter a valid positive number.")

def main():
    ghostWriter(f"{green}Enter your first number: ",0.05)
    input_one = get_float("")
    ghostWriter(f"{green}Enter your second number: ",0.05)
    input_two = get_float("")
    operation(input_one,input_two)


def operation(input_1:int, input_2:int):
    ghostWriter(f"\n\n{green}The sum of the values is {blue}{input_1 + input_2}\n",0.05)
    ghostWriter(f"{green}The difference of the values is {blue}{input_1-input_2}\n",0.05)
    ghostWriter(f"{green}The quotient of the values is {blue}{input_1/input_2}\n",0.05)
    ghostWriter(f"{green}The product of these values are {blue}{input_1 * input_2}\n",0.05)

# Runs the main method continuously
if __name__ == "__main__":
    displayed = False
    run_count = 0
    skip_display = False
    while True:
        main()
        #Checks for the users input on whether they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        #Checks for the users input
        continue_choice = input().lower().strip()
        #Ends the code 
        if continue_choice == "no":
            exit()
        #Checks if the answer is not yes or no
        elif continue_choice != "yes":
            ghostWriter(f"{red}ERROR: {white}Invalid input! Please enter yes or no.\n", 0.05)
            break
