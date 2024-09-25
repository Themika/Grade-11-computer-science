def main():
    while True:
        input_grade = get_positive_integer("Enter a number: ")
        if input_grade < 0:
            print("Negative input. Restarting......",flush=True)
            break
        else:
            continue
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