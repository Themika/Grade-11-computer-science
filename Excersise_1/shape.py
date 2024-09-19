"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program will print a shape based on the user's input on the rectangle and diamound shapes. 
On the parralorgam and trapzoid shapes, it will print the shape directly in a colored format.
"""
from time import sleep

#Logic for creating dynamic rectangle. Uses a matrix of characters to create the shape and selects the letters from a list of letters. 
# Choosing whicj lettters go where
def rectangle(length, width):
    try:
        letters = ["R", "E", "C", "T", "A", "N", "G", "L", "E"]
        reverse_letters = letters[::-1]

        matrix = [[" " for col in range(width)] for row in range(length)]

        for col in range(width):
            matrix[0][col] = letters[col % len(letters)]

        for col in range(width):
            matrix[length - 1][col] = reverse_letters[col % len(reverse_letters)]

        for row in range(1, length - 1):
            matrix[row][0] = letters[row % len(letters)]
            matrix[row][width - 1] = reverse_letters[row % len(reverse_letters)]

        for row in matrix:
            print("".join(row))
    except Exception as e:
        print(f"Error evaluating the expression: {e}")

#Creates a parralogram shape in a colored format
def trapazoid():
    Green = "\033[1;32m"
    print(Green + "  APEZO  ")
    print(Green + " R     I")
    print(Green + "TRAPEZOID")

#Creates a parralogram shape in a colored format
def parralagram():
    Red = "\033[1;31m"
    print(Red + "PARALLELOG")
    print(Red + " A        R")
    print(Red + "  R         A")
    print(Red + "    ALLELOGRAM")

#Logic for creating dynamic diamound. Uses a matrix of characters to create the shape and selects the letters from a list of letters. 
# Choosing whicj lettters go where
def diamond(custom_length, custom_width):
    try:
        letters_diamond = ["D", "I", "A", "M", "O", "N", "D"]

        matrix = [[" " for _ in range(custom_width)] for _ in range(custom_length)]

        middle = custom_width // 2

        for i in range(custom_length):
            if i <= custom_length // 2:
                num_letters = 2 * i + 1
            else:
                num_letters = 2 * (custom_length - 1 - i) + 1

            start = middle - (num_letters // 2)

            for j in range(num_letters):
                matrix[i][start + j] = letters_diamond[i % len(letters_diamond)]

        for row in matrix:
            print("".join(row))
    except Exception as e:
        print(f"Error evaluating the expression: {e}")

#This function will get the user input for the shape type, the length and width of the shape. Checking whether it is valud 
def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
            else:
                print("ERROR: Enter a positive integer value.")
        except ValueError:
            print("ERROR: Enter a valid integer.")
#Main method where all the logic is don basically gets all the input from the user 
def main():
    print("Welcome to shape maker. Enter any of these 4 shapes:")
    print("Rectangle: 0, Trapazoid: 1, Diamond: 2, Parallelogram: 3")
    type_shape = get_positive_integer("Enter the type of shape (0-3): ")

    if type_shape not in [0, 1, 2, 3]:
        print("ERROR: Enter a valid shape type (0-3).")
        return

    if type_shape in [0, 2]:  # Rectangle or Diamond
        length = get_positive_integer("Enter the length of the shape: ")
        width = get_positive_integer("Enter the width of the shape: ")
        if type_shape == 0:
            rectangle(length, width)
        elif type_shape == 2:
            diamond(length, width)
    else:  
        if type_shape == 1:
            trapazoid()
        elif type_shape == 3:
            parralagram()

white = "\033[1;37m"

if __name__ == "__main__":
    while True:
        main()
        make_shape_again = input(white + "Would you like to continue making shapes (yes/no): ").lower().strip()
        if make_shape_again != "yes" or make_shape_again == "no":
            print("Invalid input! Please enter yes or no.")
        else:
            if make_shape_again == "no":
                print("Goodbye!")
                break
            else:
                continue