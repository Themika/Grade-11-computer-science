from time import sleep
from class1 import *


def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)


def main():
    numbers = []
    count = 1
    print("Enter numbers one by one. Type 'done' to finish.")
    while True:
        num = input(f"Enter number {count}: ")
        if num.lower() == 'done':
            break
        try:
            numbers.append(float(num))
            count += 1
        except ValueError:
            print("Please enter a valid number.")
    ghostWriter(f"\nSum: {sum_numbers(numbers)}",0.05)
    ghostWriter(f"\nMean: {mean(numbers)}",0.05)
    ghostWriter(f"\nMedian: {median(numbers)}",0.05)
    ghostWriter(f"\nMode: {mode(numbers)}",0.05)

if __name__ == "__main__":
    while True:
        main()
        print()
        continue_program = str(input("\nWould you like to continue (yes/no): ")).lower().strip(" ")
        if continue_program == "no":
            break