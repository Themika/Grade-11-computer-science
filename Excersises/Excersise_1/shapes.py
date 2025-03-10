"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program will print a shape based on the user's input on the rectangle and diamound shapes. 
On the parralorgam and trapzoid shapes, it will print the shape directly in a colored format.
"""
from time import sleep

#Logic for creating dynamic rectangle. Uses a matrix of characters to create the shape and selects the letters from a list of letters. 
# Choosing whicj lettters go where
#5 X 9 prints out a proper rectangle 
white = "\033[1;37m"
Green = "\033[1;32m"
Red = "\033[1;31m"
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
    print(Green + "  APEZO  ")
    print(Green + " R     I")
    print(Green + "TRAPEZOID")

#Creates a parralogram shape in a colored format
def parralagram():
    print(Red + "PARALLELOG")
    print(Red + " A        R")
    print(Red + "  R         A")
    print(Red + "    ALLELOGRAM")

#Logic for creating dynamic diamound. Uses a matrix of characters to create the shape and selects the letters from a list of letters. 
# Choosing whicj lettters go where
# 7 X 7 prints out a full diamound 
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
            print(" ".join(row))
    except IndexError as e:
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
            print("ERROR: Enter a valid positive integer.")

#Main method where all the logic is don basically gets all the input from the user 
def main():
    print(white + "Welcome to shape maker. Enter any of these 4 shapes:")
    print(white +"Rectangle: 0, Trapazoid: 1, Diamond: 2, Parallelogram: 3")
    type_shape = get_positive_integer(white +"Enter the type of shape (0-3): ")

    if type_shape not in [0, 1, 2, 3]:
        print("ERROR: Enter a valid shape type (0-3).")
        return
    if type_shape == 2 or type_shape  == 0:
        length = get_positive_integer(white +"Enter the length of the shape: ")
        width = get_positive_integer(white +"Enter the width of the shape: ")
        if type_shape == 0:
            if length == width and length != 0:
                print("Please do not create a square")
                exit()
            elif length == 0 or width ==0:
                print("Enter a non zero value")
                exit()
            rectangle(length, width)
        elif type_shape == 2:
            if length > width:
                print("Make the width greater then length")
                exit()
            diamond(length, width)
    if type_shape == 1:
        trapazoid()
    if type_shape == 3:
        parralagram()



if __name__ == "__main__":
    while True:
        main()
        make_shape_again = input("Would you like to continue (yes/no): ").lower().strip()
        if make_shape_again == "no":
            exit()
        elif make_shape_again != "yes" or make_shape_again == "no":
            print(white+ "Invalid input! Please enter yes or no.")