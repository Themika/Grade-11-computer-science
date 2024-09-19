"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program is a simple progarm that will print the sum, difference, product, and quotient of two numbers.
and then ask if the user would like to continue.
"""
#Displays the operations
def main():
    print("The sum of 5.261 and 3.674 is 8.9")
    print("The difference of 12.5 and 5.5 is 7.0")
    print("The product of 7.1 and 4.25.0 is 30.2")
    print("The quotient of 15.0 and 3.0 is 5.0")

if __name__ == "__main__":
    main()
    print("Would you like to continue (yes/no) ")
    continue_loop = input().lower().strip()
    try:
        if continue_loop != "yes" and continue_loop != "no":
            print ("Invalid input! Please enter yes or no")
            exit()
        elif continue_loop == "no":
            print("Goodbye!")
            exit()
        else:
            main()
            print("Would you like to continue (yes/no) ")
            continue_loop = input().lower()
            if continue_loop != "yes":
                print("Goodbye!")
                exit()
            else:
                main()
                print("Goodbye!")
    except Exception as e:
        print(f"Error evaluating the expression: {e}")
        exit()