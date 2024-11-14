def get_input(first_name, last_name, age,address,phone_number):
    with open("Practice_Problems/Practice_#5/User_Input/storedInfo.txt", "w") as file:
        file.write(f"First Name: {first_name}\n")
        file.write(f"Last Name: {last_name}\n")
        file.write(f"Age: {age}\n")
        file.write(f"Address: {address}\n")
        file.write(f"Phone Number: {phone_number}\n")

def main():
    try:
        name = str(input("Enter your first name: "))
        last_name = str(input("Enter your last name: "))
        age = int(input("Enter your age: "))
        address = input("Enter your address: ")
        phone_number = int(input("Enter your phone number: "))
        get_input(name, last_name, age, address, phone_number)
    except ValueError:
        print("Invalid input. Please enter the correct information.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()