def main():
    top_bound = get_positive_integer("Input the  number you want to count down from: ")
    lower_blound = get_positive_integer("Input the number you want to count down to: ")
    for i in range(top_bound,-lower_blound,-1):
        print(i)
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
if __name__ =="__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip(" ")
        if continue_program == "no":
            break