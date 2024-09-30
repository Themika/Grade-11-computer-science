from time import sleep

white = "\033[0;37m"
codder_green = "\033[0;32m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)
def display_program():
    display_lines = ["__        __   _                            _                           \n",
                     "\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___    _ __ ___  _   _  \n",
                     " \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | '_ ` _ \| | | | \n",
                     "  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | | | | | | |_| | \n",
                     "   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_| |_| |_|\__, | \n",
                     "            | '_ \| '__/ _ \ / _` | '__/ _` | '_ ` _ \           |___/  \n",
                     "            | |_) | | | (_) | (_| | | | (_| | | | | | |                 \n",
                     "            | .__/|_|  \___/ \__, |_|  \__,_|_| |_| |_|                \n",
                     "            |_|              |___/                                     \n"
                     ]
    for line in display_lines:
        ghostWriter(f"{codder_green}  {line}", 0.05)
        

def main():
    display_program()

    ghostWriter("WELCOME TO THE DIGITS PROGRAM\n", 0.05)
    ghostWriter("Enter the number you want to be seprated \t", 0.05)
    intake = input("Enter a number: ")
    ghostWriter(f"The digits of {intake} are ", 0.05)
    output = [x for x in intake.replace("-", "") if x.isdigit()]

    for i, digit in enumerate(output):
        if i == len(output) - 1:
            ghostWriter(f"and {digit}.", 0.1)
        else:
            ghostWriter(f"{digit}, ", 0.1)
    print()  

if __name__ == "__main__":
    while True:
        main()
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        seperate_digit_continue = input().lower().strip()
        if seperate_digit_continue == "no":
            exit()
        elif seperate_digit_continue != "yes":
            ghostWriter("Invalid input! Please enter yes or no.", 0.05)