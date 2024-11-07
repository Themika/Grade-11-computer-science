from time import sleep

white = "\033[0;37m"
codder_green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"


def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def string_input(prompt):
    while True:
            try:
                value = str(input(prompt).strip())
                return value
            except ValueError:
                print(f"{red}ERROR: {white}Enter a valid string.")

def main():
    word = string_input("Enter a word: ").lower()
    letter = string_input("Enter a letter: ").lower()
    if len(letter) > 1:
        print(f"{red}ERROR: {white}Enter a single letter")
        return
    counter = 0
    if letter in word:
        counter+=1
    ghostWriter(f"{blue}{letter} {white}is in {blue}{word} {counter} {white}time", 0.05)

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