from time import sleep
from statistics import median, mode, StatisticsError
from collections import Counter
import matplotlib.pyplot as plt

"""
    Name: Themika Weerasuriya
    Date: 2024-10-01
    Description: This program takes in any floating point digit and displays the digits, the median value and the mode of the digits.
    In addtion there is now CHART VISUALIZATION for most frequent numbers. It has error handling 
"""

white = "\033[0;37m"
codder_green = "\033[0;32m"

# Ghost writer method
def ghostWriter(sentence: str, pause: float):
    for i in range(len(sentence)):
        print(sentence[i], end='', flush=True)
        sleep(pause)

# Display method print out the welcome message
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
        ghostWriter(f"{codder_green}{line}\n", 0.005)

def display_chart(digit_counts):
    digits, counts = zip(*digit_counts.items())
    plt.bar(digits, counts, color='tab:blue')
    plt.xlabel('Digits')
    plt.ylabel('Frequency')
    plt.title('Frequency of Each Digit')
    plt.show()

def main():
    # Displays the message 
    display_program()
    # Input is taken here
    ghostWriter("Enter the number you want to be separated: ", 0.05)
    intake = input("Enter a number: ")
    ghostWriter(f"The digits of {intake} are ", 0.05)
    output = [x for x in intake.replace("-", "") if x.isdigit()]
    
    # Parses the inputs and separates them 
    for i, digit in enumerate(output):
        if i == len(output) - 1:
            ghostWriter(f"and {digit}. ", 0.005)
        else:
            ghostWriter(f"{digit}, ", 0.005)

    # Calculate and display the median and mode
    if output:
        # Convert digits to integers for calculations
        int_output = list(map(int, output))
        
        # Calculate median
        med = median(int_output)
        ghostWriter(f"\nThe median of the digits is: {med}\n", 0.05)
        
        # Calculate mode
        try:
            most_common = mode(int_output)
            ghostWriter(f"The most common digit is: {most_common}\n", 0.05)
        except StatisticsError:
            ghostWriter("There is no unique mode (multiple digits appear with the same highest frequency).\n", 0.05)
        
        # Calculate and display digits ordered from most to least common
        counter = Counter(int_output)
        sorted_digits = sorted(counter.items(), key=lambda x: x[1], reverse=True)
        ghostWriter("Digits ordered from most to least common:\n", 0.05)
        for digit, count in sorted_digits:
            ghostWriter(f"Digit {digit} appears {count} times.\n", 0.05)
        
        # Display the bar chart
        display_chart(counter)

    print()  

# Runs the main method continuously 
if __name__ == "__main__":
    while True:
        main()
        # Asks user for input 
        ghostWriter(f"\n{white}Would you like to continue (yes/no)? ", 0.05)
        seperate_digit_continue = input().lower().strip()
        if seperate_digit_continue == "no":
            exit()
        # Checks user input if it is a yes or no
        elif seperate_digit_continue != "yes":
            ghostWriter("Invalid input! Please enter yes or no.", 0.05)