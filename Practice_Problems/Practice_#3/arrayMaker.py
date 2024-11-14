from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def create_matrix(rows, cols, values):
    matrix = []
    values_list = [int(x) for x in values.replace("-", "").split(",") if x.strip().isdigit()]
    index = 0

    for _ in range(rows):
        row = []
        for _ in range(cols):
            if index < len(values_list):
                row.append(values_list[index])
                index += 1
            else:
                row.append(0)  
        matrix.append(row)
    return matrix

def format_matrix(matrix):
    formatted_matrix = []
    for row in matrix:
        formatted_row = ' '.join(f'{x}' for x in row)
        formatted_matrix.append(formatted_row)
    return formatted_matrix

def main():
    rows = int(input("Enter the number of rows: "))
    cols = int(input("Enter the number of columns: "))
    values = input("Enter values separated by commas: ")
    matrix = create_matrix(rows, cols, values)
    formatted_matrix = format_matrix(matrix)
    print("Matrix:")
    for row in formatted_matrix:
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