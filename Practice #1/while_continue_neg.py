def main():
    while True:
        input_grade = int(input("Enter input: "))
        if input_grade < 0:
            break
        else:
            print("Entered negative input value. Stopping the loop")
            continue

if __name__ == "__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip()
        if continue_program == "no":
            break