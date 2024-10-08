from time import sleep

# Defining colors for terminal output (optional)
white = "\033[0;37m"
codder_green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def main(total):
    input_string = input("Enter a number: ").strip()  
    for i in range(len(input_string) - 1):
        if int(input_string[i + 1]) >= int(input_string[i]):
            total += int(input_string[i + 1])
        else:
            total -= int(input_string[i + 1])
        print(f"Current total: {total}")  
        
    total += int(input_string[0])
    print(f"The input {input_string} would give an output of {total}")  

if __name__ == "__main__":
    while True:
        main(0)
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        continue_choice = input().lower().strip()
        if continue_choice == "no":
            exit()
        elif continue_choice != "yes":
            ghostWriter(f"{red}ERROR: {white}Invalid input! Please enter yes or no.\n", 0.05)
            break
