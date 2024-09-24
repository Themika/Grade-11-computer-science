def main():
    amount = int(input("Enter the amount of numbers you want to input: "))
    numbers = []
    for i in range(amount):
        numbers.append(int(input(f"Input {i + 1}: ")))
    average = sum(numbers) / len(numbers)
    print(f"The average of the numbers is: {average}")

if __name__ == "__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip()
        if continue_program == "no":
            break