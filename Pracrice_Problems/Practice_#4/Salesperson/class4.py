from time import sleep
from class3 import *


def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)


def main():
    ghostWriter("Enter the amount the sum of the sales you've made for example \n($10000): ", 0.05)
    try:
        person_sales = int(input())
        ghostWriter(f"You are a {sales(person_sales)}", 0.05)
    except ValueError:
        print("\nInvalid input. Please enter a valid number.")
    


if __name__ == "__main__":
    while True:
        main()
        print()
        continue_program = str(input("\nWould you like to continue (yes/no): ")).lower().strip(" ")
        if continue_program == "no":
            break