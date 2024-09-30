def convert_temp(temp, from_unit, to_unit):
    if from_unit == "C" and to_unit == "F":
        return temp * 9/5 + 32
    elif from_unit == "F" and to_unit == "C":
        return (temp - 32) * 5/9
    else:
        return temp

def main():
    starting_value = input("Input the value you are starting with: ").lower()
    
    digits = []
    letters = []
    
    for char in starting_value:
        if char.isdigit():
            digits.append(char)
        elif char.isalpha():
            letters.append(char)
    convert_temp()

if __name__ == "__main__":
    main()