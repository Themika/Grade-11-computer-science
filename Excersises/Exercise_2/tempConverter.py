from time import sleep

"""
    Name: Themika Weerasuriya
    Date: 2024-10-01
    Description: This program takes in any floating point number.Converts it between five units Celsisus, Farinheit, Kelvin, Newton, Rankine. 
    It has error handeling and a display method that can be skipped for future runs.
"""

white = "\033[0;37m"
green = "\033[0;32m"
blue = "\033[0;34m"

# Ghost writer method
def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

def get_positive_float(prompt):
    # Get a positive floating-point value from the user
    while True:
        try:
            value = float(input(prompt).strip())
            return value
        except ValueError:
            print("ERROR: Enter a valid positive number.")

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
    # Display the program name
    for line in display_lines:
        ghostWriter(f"{green}{line}\n", 0.0005)

# Converts the temperature between various units
def convert_temp(temp, from_unit, to_unit):
    conversions = {
        #Celsius conversions
        ("c", "f"): lambda t: t * 9/5 + 32,
        ("c", "n"): lambda t: t * 33/100,
        ("c", "r"): lambda t: t * 9/5 + 491.67,
        ("c", "k"): lambda t: t + 273.15,
        #Fahrenheit conversions
        ("f", "n"): lambda t: (t - 32) * 11/60,
        ("f", "c"): lambda t: (t - 32) * 5/9,
        ("f", "r"): lambda t: t + 459.67,
        ("f", "k"): lambda t: (t - 32) * 5/9 + 273.15,
        #Newton conversions
        ("n", "c"): lambda t: t * 100/33,
        ("n", "f"): lambda t: t * 60/11 + 32,
        ("n", "k"): lambda t: t * 100/33 + 273.15,
        ("n", "r"): lambda t: t * 60/11 + 491.67,
        #Kelvin conversions
        ("k", "n"): lambda t: (t - 273.15) * 33/100,
        ("k", "f"): lambda t: (t - 273.15) * 9/5 + 32,
        ("k", "c"): lambda t: t - 273.15,
        ("k", "r"): lambda t: t,
        #Rankine conversions
        ("r", "n"): lambda t: (t - 491.67) * 11/60,
        ("r", "c"): lambda t: (t - 491.67) * 5/9,
        ("r", "f"): lambda t: t - 459.67,
        ("r", "k"): lambda t: t * 5/9,
    }
    try:
        return conversions[(from_unit, to_unit)](temp)
    except KeyError:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} is not supported.")

def main():
    #This handles the display method checking whether the user wants to see it again for furture runs
    global displayed, run_count, skip_display
    if not displayed or (run_count >= 0 and not skip_display):
        display_program()
        displayed = True
        run_count += 1
        #Checks if the code has run once
        if run_count == 1:
            #Checks if the user wants to skip
            ghostWriter(f"\n{white}Would you like to skip the display in future runs (yes/no)?\n", 0.05)
            skip_display_input = input().lower().strip()
            while True:
                #Checks if the input is yes or no
                if skip_display_input == "yes":
                    skip_display = True
                    break
                elif skip_display_input == "no":
                    break
                else:
                    ghostWriter(f"{white}Invalid input! Please enter yes or no.\n", 0.05)
                    skip_display_input = input().lower().strip()

    # Ask for the starting and ending values of the range
    ghostWriter(f"{green}Input the starting value of the range: ", 0.05)
    start_value = get_positive_float("")
    ghostWriter(f"{green}Input the ending value of the range: ", 0.05)
    end_value = get_positive_float("")

    #This is where i keep track of the valyes for later
    starting_unit = []
    ending_values = []
    #This is where i keep track of the units
    unit_mapping = {
        "c": "Celsius",
        "f": "Fahrenheit",
        "k": "Kelvin",
        "n": "Newton",
        "r": "Rankine"
    }
    #This is where the user inputs the units they want to convert between
    while True:
        # Ask for the unit to convert from and to
        ghostWriter(f"{green}Input the unit you are converting from (C/F/K/N/R): ", 0.05)
        from_unit = input().strip().lower()
        starting_unit.append(from_unit)
        #Ask for the unit to convert to
        ghostWriter(f"{green}Input the unit you are converting to (C/F/K/N/R): ", 0.05)
        to_unit = input().strip().lower()
        ending_values.append(to_unit)

        #Error handleing to check whether the units are the same not inclcuded in the converted units
        if from_unit == to_unit:
            ghostWriter(f"\n{white}ERROR: The starting unit and the converted unit cannot be the same. Please enter different units.\n", 0.05)
        elif from_unit not in ["c", "f", "k","n","r"] or to_unit not in ["c", "f", "k","n","r"]:
            ghostWriter(f"\n{white}ERROR: Enter a valid unit to convert to.\n", 0.05)
            starting_unit.clear()
            ending_values.clear()
        else:
            break
    #Display the full names of the units
    from_unit_string = unit_mapping.get(starting_unit[0], "Unknown")
    to_unit_string = unit_mapping.get(ending_values[0], "Unknown")

    #Printing out the table 
    ghostWriter(f"\n{green}Converting from {from_unit_string} to {to_unit_string}\n", 0.05)
    #Printing out the table headers
    ghostWriter(f"{'Value':<10} | {'Converted':<10}\n", 0.05)
    #Printing out the table seperator
    ghostWriter(f"{'-'*10}-+-{'-'*10}\n", 0.05)

    # Calculate and print the conversion for each value in the range
    if start_value <= end_value:
        step = 1
    else:
        step = -1

    for value in range(int(start_value), int(end_value) + step, step):
        #Converting the values
        converted_value = convert_temp(value, from_unit, to_unit)
        #Printing out the values
        ghostWriter(f"{value:<10.2f} | {converted_value:<10.2f}\n", 0.05)

# Runs the main method continuously
if __name__ == "__main__":
    displayed = False
    run_count = 0
    skip_display = False
    while True:
        main()
        #Checks for the users input on whether they want to continue
        ghostWriter(f"\n{white}Would you like to continue (yes/no)\n", 0.05)
        #Checks for the users input
        continue_choice = input().lower().strip()
        #Ends the code 
        if continue_choice == "no":
            exit()
        #Checks if the answer is not yes or no
        elif continue_choice != "yes":
            ghostWriter(f"{white}Invalid input! Please enter yes or no.\n", 0.05)
            break