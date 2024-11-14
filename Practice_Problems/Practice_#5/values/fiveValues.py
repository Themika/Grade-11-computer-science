def find_sum():
    with open("Practice_Problems/Practice_#5/values/values.txt", "r") as file:
        line = file.readline().strip()
        values = [int(element) for element in line.split(',')]
    total = sum(values)
    with open("Practice_Problems/Practice_#5/values/final.txt", "a") as file:
        file.write("The sum of the values is: " + str(total) + "\n")
    return total

def product():
    with open("Practice_Problems/Practice_#5/values/values.txt", "r") as file:
        line = file.readline().strip()
        values = [int(element) for element in line.split(',')]

    product = 1
    for value in values:
        product *= value

    with open("Practice_Problems/Practice_#5/values/final.txt", "a") as file:
        file.write("The product of the values is: " + str(product) + "\n")

    return product

def quotient():
    with open("Practice_Problems/Practice_#5/values/values.txt", "r") as file:
        line = file.readline().strip() 
        values = [int(element) for element in line.split(',')] 
    quotient = values[0]
    for value in values[1:]:
        quotient /= value    
    with open("Practice_Problems/Practice_#5/values/final.txt", "a") as file:
        file.write("The quotient of the values is: " + str(quotient) + "\n")
    file.close()

def find_average():
    with open("Practice_Problems/Practice_#5/values/values.txt", "r") as file:
        line = file.readline().strip() 
        values = [int(element) for element in line.split(',')] 
    with open("Practice_Problems/Practice_#5/values/final.txt", "a") as file:
        file.write("The average of the values is: " + str(sum(values) / len(values)) + "\n")
    file.close()


def main():
    find_sum()
    product()
    quotient()
    find_average()
    

if __name__ == "__main__":
    main()