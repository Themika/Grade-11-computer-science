def main():
    top_bound = int(input("Input the  number you want to count down from: "))
    lower_blound = int(input("Input the number you want to count down to: "))
    for i in range(top_bound,-lower_blound,-1):
        print(i)

if __name__ =="__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip(" ")
        if continue_program == "no":
            break