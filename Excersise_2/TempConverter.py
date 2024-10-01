from time import sleep

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"

def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def display_program():
    display_lines = [r"__        __   _                            _                           ",
                     r"\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___    _ __ ___  _   _  ",
                     r" \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | '_ ` _ \| | | | ",
                     r"  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | | | | | | |_| | ",
                     r"   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_| |_| |_|\__, | ",
                     r"            | '_ \| '__/ _ \ / _` | '__/ _` | '_ ` _ \           |___/  ",
                     r"            | |_) | | | (_) | (_| | | | (_| | | | | | |                 ",
                     r"            | .__/|_|  \___/ \__, |_|  \__,_|_| |_| |_|                ",
                     r"            |_|              |___/                                     "
                     ]
    for line in display_lines:
        ghostWriter(f"{green}  {line}\n", 0.05)

def convert_temp(temp, from_unit, to_unit):
    if from_unit == "C" and to_unit == "F":
        return temp * 9/5 + 32
    elif from_unit == "F" and to_unit == "C":
        return (temp - 32) * 5/9
    else:
        return temp

def main():
    global displayed, run_count, skip_display
    if not displayed or (run_count >= 0 and not skip_display):
        display_program()
        displayed = True
        run_count += 1
        if run_count == 2:
            ghostWriter(f"\n{white}Would you like to skip the display in future runs (yes/no)?\n", 0.05)
            skip_display_input = input().lower().strip()
            if skip_display_input == "yes":
                skip_display = True
            elif skip_display_input != "no":
                ghostWriter(f"{white}Invalid input! Please enter yes or no.\n", 0.05)
    
    ghostWriter("Input the value you are starting with: ", 0.05)
    starting_value = input().lower()
    
    digits = []
    letters = []
    
    for char in starting_value:
        if char.isdigit():
            digits.append(char)
        elif char.isalpha():
            letters.append(char)
    
    # Join digits to form the number
    number = ''.join(digits)
    
    # Join letters to form the unit
    unit = ''.join(letters)
    
    # Convert the number to a float
    if number:
        number = float(number)
    
    ghostWriter(f"{green}Number: {number}\n", 0.05)
    ghostWriter(f"{green}Unit: {unit} \n", 0.05)
    
    # Example usage of convert_temp
    if unit in ["c", "f"]:
        to_unit = "f" if unit == "c" else "c"
        converted_temp = convert_temp(number, unit.upper(), to_unit.upper())
        ghostWriter(f"\n{blue}Converted temperature: {converted_temp} {to_unit.upper()}\n", 0.05)

if __name__ == "__main__":
    displayed = False
    run_count = 0
    skip_display = False
    while True:
        main()
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        seperate_digit_continue = input().lower().strip()
        if seperate_digit_continue == "no":
            exit()
        elif seperate_digit_continue != "yes":
            ghostWriter(f"{white}Invalid input! Please enter yes or no.\n", 0.05)