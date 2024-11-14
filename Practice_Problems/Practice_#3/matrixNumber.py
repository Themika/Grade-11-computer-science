from time import sleep

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
    one_counter = 0
    max_ones = 0
    row_with_max_ones = []
    
    for i in range(rows):
        row_input = input(f"Enter values for row {i} separated by spaces: ")
        row = [int(x) for x in row_input.split()]
        if len(row) != cols:
            ghostWriter(f"{red}ERROR: {white}Row {i} does not have {cols} columns. Please enter the row again.\n", 0.05)
            return create_matrix(rows, cols)
        ones_count = row.count(1)
        if ones_count > max_ones:
            max_ones = ones_count
            row_with_max_ones = row
        if 1 in row:
            one_counter += 1
        matrix.append(row)
    
    ghostWriter(f"\n{green}Number of rows containing the value 1: {blue}{one_counter}\n", 0.05)
    ghostWriter(f"\n{green}Row with the most ones: {blue}{row_with_max_ones}\n", 0.05)
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