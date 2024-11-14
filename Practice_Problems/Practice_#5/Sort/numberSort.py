def get_numbers():
    numbers = []
    for _ in range(10):
        while True:
            try:
                number = int(input("Enter a number: "))
                numbers.append(number)
                break
            except ValueError:
                print("Invalid input. Please enter an integer.")
    return numbers

def write_to_file(filename, numbers):
    with open(filename, 'w') as file:
        for number in numbers:
            file.write(f"{number}\n")

def read_from_file(filename):
    with open(filename, 'r') as file:
        numbers = [int(line.strip()) for line in file]
    return numbers

def main():
    numbers = get_numbers()
    write_to_file('Practice_Problems/Practice_#5/Sort/numbers.txt', numbers)
    
    numbers = read_from_file('Practice_Problems/Practice_#5/Sort/numbers.txt')
    sorted_numbers = sorted(numbers)
    write_to_file('Practice_Problems/Practice_#5/Sort/sorted_numbers.txt', sorted_numbers)
    
    print("Sorted numbers have been written to 'sorted_numbers.txt'.")

if __name__ == "__main__":
    main()
