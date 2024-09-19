from time import sleep
"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program is a simple calcultator built into the terminal. It will give the user a simple tutorial 
on how to use the calculator and then allow the user to input their own calculations.
"""

amount = 2
#Displays the tutorial
def tutorial():
    print("Welcome to the terminal calculator tutorial")
    sleep(amount)
    print("Here we will show you the basics by showing operations in action")
    sleep(amount)
    print("For example: 3 + 6 * 2")
    sleep(amount)
    print(3 + 6 * 2)
    print("For example: 4 * 7 - 6 / 3")
    sleep(amount)
    print(4 * 7 - 6 / 3)
    print("For example: 2 * (3 + 11) - 6 * (2 - 8)")
    sleep(amount)
    print(2 * (3 + 11) - 6 * (2 - 8))
    print("For example: 13 + 23 - 9 / 3")
    sleep(amount)
    print(13 + 23 - 9 / 3)

#Displays the operations and does all the logic of a simple calulator
def main():
    skip_tutorial = input("Would you like to skip the tutorial (yes/no) ")
    if skip_tutorial.lower() != "yes":
        tutorial()
    print("Now you may enter your own numbers to calculate")
    problem = input("Enter the problem: ")
    problem = problem.strip()
    
    try:
        result = eval(problem)
        print(f"The result is: {result}")
    except Exception as e:
        print(f"Error evaluating the expression: {e}")

if __name__ == "__main__":
    while True: 
        main()
        continue_loop = input("Would you like to continue (yes/no) ").lower().strip()
        if continue_loop != "yes" or continue_loop == "no":
            print("Invalid input! Please enter yes or no")
        else:
            if continue_loop == "no":
                print("Goodbye!")
                break
            else:
                continue