from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def main():
    ghostWriter("What is your name: ",0.05)
    input_name = str(input(""))
    ghostWriter("What is your address: ",0.05)
    input_address = str(input(""))
    ghostWriter("What is your postal code: ",0.05)
    input_postal_code = str(input(""))
    format_input(input_name,input_address,input_postal_code)


def format_input(name:str, address_input:str, postal_code:str):
    return print(f"{green}Your name is {blue}{name} {green}and you live on {blue}{address_input} {green}and your postal code is {blue}{postal_code}")

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
