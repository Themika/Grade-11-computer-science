from time import sleep
from class5 import *


def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)


def main():
    ghostWriter("Enter the shape you would like to draw(Ghost/Diamond/Parallelogram/Triangle): ", 0.05)
    try:
        shape = str(input()).lower().strip(" ")
        if shape == "ghost":
            ghostWriter("Enter the size of the ghost: ", 0.05)
            size = int(input())
            ghostWriter("Enter the character you would like to use: ", 0.05)
            char = str(input()).strip(" ")
            ghost(size, size, char)
        elif shape == "diamond":
            ghostWriter("Enter the size of the diamond: ", 0.05)
            size = int(input())
            ghostWriter("Enter the character you would like to use: ", 0.05)
            char = str(input()).strip(" ")
            diamond(size, char)
        elif shape == "parallelogram":
            ghostWriter("Enter the size of the parallelogram: ", 0.05)
            size_x = int(input())
            ghostWriter("Enter the width of the parallelogram: ", 0.05)
            size_y = int(input())
            ghostWriter("Enter the character you would like to use: ", 0.05)
            char = str(input()).strip(" ")
            parallelogram(size_x, size_y, char)
        elif shape == "triangle":
            ghostWriter("Enter the size of the triangle: ", 0.05)
            size = int(input())
            ghostWriter("Enter the character you would like to use: ", 0.05)
            char = str(input()).strip(" ")
            triangle(size, char)
        else:
            ghostWriter("Please enter a valid shape.", 0.05)
    except ValueError:
        ghostWriter("Please enter a valid input.", 0.05)

if __name__ == "__main__":
    while True:
        main()
        print()
        continue_program = str(input("\nWould you like to continue (yes/no): ")).lower().strip(" ")
        if continue_program == "no":
            break