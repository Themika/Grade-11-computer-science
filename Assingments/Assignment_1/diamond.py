def main():
    custom_length = get_positive_integer("Input a length: ")
    custom_width = get_positive_integer("Input a width: ")
    custom_name = input("Enter the custom word: ").strip(" ")
    diamond(custom_width,custom_length,custom_name)

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

def diamond(custom_length, custom_width,custom_name):
    try:
        letters_diamond = [x for x in custom_name]

        custom_length = max(1, custom_length + (custom_length + 1) % 2)
        custom_width = max(1, custom_width + (custom_width + 1) % 2)

        matrix = [[" " for _ in range(custom_width)] for _ in range(custom_length)]
        middle = custom_width // 2

        for i in range(custom_length):
            if i <= custom_length // 2:
                num_letters = min(2 * i + 1, custom_width)  
            else:
                num_letters = min(2 * (custom_length - 1 - i) + 1, custom_width)

            start = max(0, middle - (num_letters // 2))
            end = min(custom_width, start + num_letters)

            for j in range(start, end):
                matrix[i][j] = letters_diamond[i % len(letters_diamond)]

        for row in matrix:
            print(" ".join(row))
    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    while True:
        main()
        make_shape_again = input("Would you like to continue (yes/no): ").lower().strip()
        if make_shape_again == "no":
            exit()
        elif make_shape_again != "yes" or make_shape_again == "no":
            print("Invalid input! Please enter yes or no.")