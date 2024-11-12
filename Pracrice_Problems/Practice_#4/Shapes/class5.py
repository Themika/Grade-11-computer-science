def ghost(size_x: int, size_y: int, char: str):
    for i in range(size_x):
        for j in range(size_y):
            if (i == 0 and j % 2 == 0) or (i == size_x - 1 and j % 2 == 0) or (j == 0 and i % 2 == 0) or (j == size_y - 1 and i % 2 == 0):
                print(char, end="")
            elif (i == size_x // 2 and j == size_y // 4) or (i == size_x // 2 and j == 3 * size_y // 4):
                print("o", end="")  # Eyes
            elif i == size_x // 2 + 1 and j == size_y // 2:
                print("~", end="")  # Mouth
            else:
                print(" ", end="")
        print()

def diamond(size: int, char: str):
    n = size // 2
    for i in range(n + 1):
        print(" " * (n - i) + char * (2 * i + 1))
    for i in range(n - 1, -1, -1):
        print(" " * (n - i) + char * (2 * i + 1))

def parallelogram(size_x: int, size_y: int, char: str):
    for i in range(size_x):
        print(" " * (size_x - i - 1), end="")
        for j in range(size_y):
            if i == 0 or i == size_x - 1 or j == 0 or j == size_y - 1:
                print(char, end="")
            else:
                print(" ", end="")
        print()

def triangle(size: int, char: str):
    for i in range(size):
        print(" " * (size - i - 1) + char * (2 * i + 1))


