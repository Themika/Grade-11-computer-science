
def main():
    input_grade = get_positive_integer("Enter your current grade: ")
    print(check_grade(input_grade))

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

def check_grade(grade):
    current_grade = " "
    if grade >= 80 and grade <= 100:
        current_grade = "Your current grade is an A"
    elif grade >= 70 and grade < 80:
        current_grade = "Your current grade is a B"
    elif grade >= 60 and grade < 70:
        current_grade = "Your current grade is a C"
    elif grade < 60 and grade >= 50:
        current_grade = "Your current grade is a F"
    elif grade < 0 or grade > 100:
        current_grade = "INVALID GRADE"
    return current_grade

if __name__ =="__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip(" ")
        if continue_program == "no":
            break