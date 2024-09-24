def main():
    amount = int(input("Enter the amount of numbers you want to input: "))
    numbers = []
    for i in range(amount):
        numbers.append(int(input(f"Input {i + 1}: ")))
    numbers.sort()

    for i in range(len(numbers)):
        print(numbers[i], end=" ")
    print()  

if __name__ == "__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip()
        if continue_program == "no":
            break