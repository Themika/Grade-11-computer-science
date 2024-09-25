def main():
    angle1 = get_positive_integer("Enter the first angle: ")
    angle2 = get_positive_integer("Enter the second angle: ")
    angle3 = get_positive_integer("Enter the third angle: ")

    if angle1 + angle2 + angle3 == 180:
        print("This is a valid triangle.")
    else:
        print("This is not a valid triangle.")
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
if __name__ == "__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip()
        if continue_program == "no":
            break