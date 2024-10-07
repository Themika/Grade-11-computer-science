from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def string_input(prompt):
    while True:
            try:
                value = str(input(prompt).strip())
                return value
            except ValueError:
                print(f"{red}ERROR: {white}Enter a valid string.")


def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def main():
    ghostWriter("Enter a string: ",0.05)
    input_name = string_input("")
    check_case(input_name)


def check_case(string:str):
    counter_uppercase = 0
    counter_lowercase= 0
    for char in string:
        if char.isupper():
            counter_uppercase+=1
        elif char.islower():
            counter_lowercase += 1
    ghostWriter(f"\n\n{green}There are {blue}{counter_uppercase} {green}upercase chaarcters and {blue}{counter_lowercase} {green}lowercase characters",0.05)
            

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
