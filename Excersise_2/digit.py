from time import sleep

white = "\033[0;37m"
codder_green = "\033[0;32m"
#Ghost writer method
def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)
#Display method print out the welocm message
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
        ghostWriter(f"{codder_green}  {line}\n", 0.05)
        

def main():
    #Displays the message 
    display_program()
    #Input is taken here
    ghostWriter("Enter the number you want to be seprated \t", 0.05)
    intake = input("Enter a number: ")
    ghostWriter(f"The digits of {intake} are ", 0.05)
    output = [x for x in intake.replace("-", "") if x.isdigit()]
    #Parses the inputs and sepertaes them 
    for i, digit in enumerate(output):
        if i == len(output) - 1:
            ghostWriter(f"and {digit}.", 0.1)
        else:
            ghostWriter(f"{digit}, ", 0.1)
    print()  
#Runs the main method continously 
if __name__ == "__main__":
    while True:
        main()
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        seperate_digit_continue = input().lower().strip()
        if seperate_digit_continue == "no":
            exit()
        elif seperate_digit_continue != "yes":
            ghostWriter("Invalid input! Please enter yes or no.", 0.05)