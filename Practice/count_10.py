def main():
    top_bound = int(input("Input the highest number you want to count to: "))
    lower_blound = int(input("Input the lowest number you want to count to: "))
    for i in range(lower_blound,top_bound + 1):
        print(i)

if __name__ =="__main__":
    while True:
        main()
        continue_program = str(input("Would you like to continue (yes/no): ")).lower().strip(" ")
        if continue_program == "no":
            break