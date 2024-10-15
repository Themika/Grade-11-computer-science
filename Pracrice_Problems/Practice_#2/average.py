from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def float_input(prompt):
    while True:
            try:
                value = float(input(prompt).strip())
                return value
            except ValueError:
                print(f"{red}ERROR: {white}Enter a valid floating point number.")


def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def average(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    ghostWriter(f"\n{green}The average of these numbers is {blue}{total/len(numbers)}",0.05)

def main():
    ghostWriter("Enter the amount of numbers you want to input: ", 0.05) 
    input_amount = int(input(""))
    numbers = []
    for i in range(input_amount):
        ghostWriter(f"\nEnter the {i + 1} integer ",0.05)
        numbers.append(float_input(""))
    average(numbers)

# Runs the main method continuously
if __name__ == "__main__":
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
