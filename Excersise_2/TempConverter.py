from time import sleep

"""
    Name: Themika Weerasuriya
    Date: 2024-10-01
    Description: This program takes in any floating point number.Converts it between both celsisus and Farinheit It has error handeling 
"""

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"

# Ghost writer method
def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def get_positive_integer(prompt):
    while True:
        try:
            value = float(input(prompt).strip().upper())
            if value >= 0:
                return value
            else:
                print("ERROR: Enter a positive integer value.")
        except ValueError:
            print("ERROR: Enter a valid positive integer.")

# Display method to print out the welcome message
def display_program():
    display_lines = [r"__        __   _                            _                           ",
                     r"\ \      / /__| | ___ ___  _ __ ___   ___  | |_ ___    _ __ ___  _   _  ",
                     r" \ \ /\ / / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | '_ ` _ \| | | | ",
                     r"  \ V  V /  __/ | (_| (_) | | | | | |  __/ | || (_) | | | | | | | |_| | ",
                     r"   \_/\_/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/  |_| |_| |_|\__, | ",
                     r"            | '_ \| '__/ _ \ / _` | '__/ _` | '_ ` _ \           |___/  ",
                     r"            | |_) | | | (_) | (_| | | | (_| | | | | | |                 ",
                     r"            | .__/|_|  \___/ \__, |_|  \__,_|_| |_| |_|                 ",
                     r"            |_|              |___/                                      "
                     ]
    for line in display_lines:
        ghostWriter(f"{green}{line}\n", 0.0005)

# Converts the temperature from either Celsius to Fahrenheit or vice versa
def convert_temp(temp, from_unit, to_unit):
    #Converting between celsius and farienheit respectivly 
    if from_unit == "c" and to_unit == "f":
        return temp * 9/5 + 32
    elif from_unit == "f" and to_unit == "c":
        return (temp - 32) * 5/9
    #Converting between kelvin and farienheit respectivly 
    elif from_unit == "f" and to_unit == "k":
        return (temp - 32) * 5/9 +273.15
    elif from_unit == "k" and to_unit == "f":
        return (temp - 273.15) * 9/5 + 32
    #Converting between celsius and kelvin respectivly 
    elif from_unit == "c" and to_unit == "k":
        return temp + 273.15
    elif from_unit == "k" and to_unit == "c":
        return temp - 273.15
    

def main():
    #This handles the display method checking whether the user wants to see it again for furture runs
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

    # Ask for the starting and ending values of the range
    ghostWriter(f"{green}Input the starting value of the range: ", 0.05)
    start_value = get_positive_integer("")
    ghostWriter(f"{green}Input the ending value of the range: ", 0.05)
    end_value = get_positive_integer("")
    #This is where i keep track of the valyes for later
    starting_unit = []
    ending_values = []
    unit_mapping = {
    "c": "Celsius",
    "f": "Fahrenheit",
    "k": "Kelvin"
    }
    while True:
        # Ask for the unit to convert from and to
        ghostWriter(f"{green}Input the unit you are converting from (C/F/K): ", 0.05)
        from_unit = input().strip().lower()
        starting_unit.append(from_unit)
        ghostWriter(f"{green}Input the unit you are converting to (C/F/K): ", 0.05)
        to_unit = input().strip().lower()
        ending_values.append(to_unit)
        #Error handleing to check whether the units are the same not inclcuded in the converted units and if the starting value is greater then the end value
        if from_unit == to_unit:
            ghostWriter(f"\n{white}ERROR: The starting unit and the converted unit cannot be the same. Please enter different units.\n", 0.05)
        elif from_unit not in ["c", "f", "k"] or to_unit not in ["c", "f","k"]:
            ghostWriter(f"\n{white}ERROR: Enter a valid unit to convert to.\n", 0.05)
        elif start_value > end_value:
            ghostWriter(f"\n{white}ERROR: The starting value should be less then the end value.\n", 0.05)
        else:
            break
    #Display the full names of the units
    from_unit_string = unit_mapping.get(starting_unit[0], "Unknown")
    to_unit_string = unit_mapping.get(ending_values[0], "Unknown")
    #Printing out the table 
    ghostWriter(f"\n{green}Converting from {from_unit_string} to {to_unit_string}\n", 0.05)
    ghostWriter(f"{'Value':<10} | {'Converted':<10}\n", 0.05)
    ghostWriter(f"{'-'*10}-+-{'-'*10}\n", 0.05)

    # Calculate and print the conversion for each value in the range
    for value in range(int(start_value), int(end_value) + 1):
        converted_value = convert_temp(value, from_unit, to_unit)
        ghostWriter(f"{value:<10} | {converted_value:<10.2f}\n", 0.05)

# Runs the main method continuously
if __name__ == "__main__":
    displayed = False
    run_count = 0
    skip_display = False
    while True:
        main()
        #Checks for the users input on whether they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        continue_choice = input().lower().strip()
        #Ends the code 
        if continue_choice == "no":
            exit()
        #Checks if the answer is not yes or no
        elif continue_choice != "yes":
            ghostWriter(f"{white}Invalid input! Please enter yes or no.\n", 0.05)
            continue