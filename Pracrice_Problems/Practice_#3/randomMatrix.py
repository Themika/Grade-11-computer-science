from time import sleep
import random 

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def create_matrix(rows, cols):
    matrix = []    
    for _ in range(rows):
        row = [random.randint(0, 100) for _ in range(cols)]
        matrix.append(row)
    return matrix

def main():
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    matrix = create_matrix(rows, cols)
    print("Matrix:")
    for row in matrix:
        print(row)

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