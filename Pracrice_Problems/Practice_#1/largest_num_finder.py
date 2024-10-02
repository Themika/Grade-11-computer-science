def main():
    amount = get_positive_integer("Enter the amount of numbers you want to input: ")
    numbers = []
    for i in range(amount):
        numbers.append(int(input(f"Input {i + 1}: ")))
    print(f"The largest number is: {max(numbers)}")


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