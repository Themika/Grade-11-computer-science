from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
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
            print(f"{red}ERROR: {white}Enter a valid floating point number.")

def main():
    ghostWriter("Enter digits separated by commas: ", 0.05)
    integer = string_input("")
    integers = [int(x) for x in integer.replace("-", "") if x.isdigit()]
    
    # Create a dictionary to store the count of each integer
    integer_counts = {}
    for num in integers:
        if num in integer_counts:
            integer_counts[num] += 1
        else:
            integer_counts[num] = 1
    
    # Print the occurrences of integers that are greater than 1
    for num, count in integer_counts.items():
        if count > 1:
            ghostWriter(f"\n{green}The count of integer {blue}{num}{green} is: {blue}{count}\n", 0.05)
    
    

# Runs the main method continuously
if __name__ == "__main__":
    while True:
        main()
        # Checks for the user's input on whether they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        # Checks for the user's input
        continue_choice = input().lower().strip()
        # Ends the code 
        if continue_choice == "no":
            exit()
        # Checks if the answer is not yes or no
        elif continue_choice != "yes":
            ghostWriter(f"{red}ERROR: {white}Invalid input! Please enter yes or no.\n", 0.05)
            break