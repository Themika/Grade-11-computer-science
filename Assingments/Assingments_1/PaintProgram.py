from time import sleep
from datetime import datetime
from random import randint
"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program is a simple program that will allow a user to choose from various interior paint options. Then give you an invoice on the cost
of painting the room, providing you with 2 payment options.
Enumerate()
//https://www.w3schools.com/python/ref_func_enumerate.asp
"""
#TODO do this during the weekend
#Add sound effects
#Add discription to the paint 
#Add random discounts 
#Make it so you cna pick a custom color gloss amount

# TODO NEXT week
# Add an emailing system
# Take in any unit of measurement
# Credit card system

# ANSI color for output
white = "\033[1;37m"
green = "\033[0;32m"
blue = "\033[0;34m"
red = "\033[0;31m"

def ghostWriter(sentence: str, pause: float):
    for char in sentence:
        print(char, end='', flush=True)
        sleep(pause)

def get_input(prompt, input_type):
    while True:
        try:
            ghostWriter(f"{blue}{prompt}", 0.05)
            value = input().strip()

            # If the input type is str, check if the input consists only of alphabetical characters
            if input_type == str:
                if not value.isalpha():
                    raise ValueError  # Trigger error if non-alphabetical characters are found
            else:
                value = input_type(value)  # Convert the value to the required input type if not a string

            return value
        except ValueError:
            ghostWriter(f"{red}ERROR: {white}Enter a valid {input_type.__name__} (only alphabetical characters for names).\n", 0.05)


def display_program():
    display_lines = [
        r"                     ____          _                      ____       _       _         ",
        r"                    / ___|___  ___| |_   _ __  ___ _ __  |  _ \ __ _(_)_ __ | |_       ",
        r"                   | |   / _ \/ __| __|| '_ \ / _ \ '__| | |_) / _` | | '_ \| __|      ",
        r"                   | |__| (_) \__ \ |_ | |_) |  __/ |    |  __/ (_| | | | | | |_       ",
        r"                    \____\___/|___/\__|| .__/\___|_|     |_|   \__,_|_|_| |_|\__|       ",
        r"                                     __|_|  _           _                             ",
        r"                                     |  ___(_)_ __   __| | ___ _ __                    ",
        r"                                     | |_  | | '_ \ / _` |/ _ \ '__|                   ",
        r"                                     |  _| | | | | | (_| |  __/ |                      ",
        r"                                     |_|   |_|_| |_|\__,_|\___|_|                      "  
    ]
    for line in display_lines:
        ghostWriter(f"{green}{line}\n", 0.005)

def run_program():
    global displayed, run_count, skip_display
    if not displayed or (run_count >= 0 and not skip_display):
        display_program()
        displayed = True
        run_count += 1
        if run_count == 1:
            skip_display_input = get_input(f"\n{white}Would you like to skip the display in future runs (yes/no)?\n{blue}", str,).lower()
            while skip_display_input not in ["yes", "no"]:
                ghostWriter(f"{red}ERROR: {white}Invalid input! Please enter yes or no.\n", 0.05)
                skip_display_input = get_input(f"{white}Would you like to skip the display in future runs (yes/no)?\n{blue}", str).lower()
            skip_display = (skip_display_input == "yes")
def process_room(room_number: int):
    total_area = 0
    areas = []
    for i in range(room_number):
        length = get_input(f"{white}Enter the dimensions of room {i + 1} (length): {blue}", int)
        width = get_input(f"{white}Enter the dimensions of room {i + 1} (width): {blue}", int)
        area = length * width
        areas.append(area)
        total_area += area
    
    for i, area in enumerate(areas):
        ghostWriter(f"{green}Room {i + 1} area: {area} sq ft\n", 0.05)
    
    ghostWriter(f"{green}Total area: {total_area} sq feet\n", 0.05)
    global amount_of_paint
    amount_of_paint = round(total_area / 380,2)
    ghostWriter(f"You will need {amount_of_paint} gallon of paint", 0.05)
    return total_area

def process_paint(paints: dict):
    global paint_choice, paint_cost
    ghostWriter(f"\n{white}Here are your paint types:\n", 0.05)
    index = 1
    for paint in paints:
        price = paints[paint]
        ghostWriter(f"{green}{index}. {white}{paint}: ${green}{price} {white}per gallon\n", 0.05)
        index += 1
    
    paint_choice_index = get_input(f"{white}Enter the number corresponding to the paint type you would like to use: {blue}", int)
    while paint_choice_index < 1 or paint_choice_index > len(paints):
        ghostWriter(f"{red}ERROR: {white}Invalid paint type! Please enter a valid number.\n", 0.05)
        paint_choice_index = get_input(f"{white}Enter the number corresponding to the paint type you would like to use: {blue}", int)
    
    paint_choice = list(paints.keys())[paint_choice_index - 1]
    paint_cost = paints[paint_choice]
    cost_paint = paint_cost * amount_of_paint
    if paint_choice == "Custom Paint":
        custom_paint()
    ghostWriter(f"{green}You have chosen {paint_choice}\n", 0.05)
    ghostWriter(f"{white}The total cost of your purchase will be ${paint_cost} x {amount_of_paint} = ${cost_paint}(no tax) \n", 0.05)
    ghostWriter(f"{white}The total cost of your purchase will be ${cost_paint * 1.13}(with tax)\n", 0.05)

    return cost_paint * 1.13

def process_payment(total_cost):
    ghostWriter(f"\n{white}How are you paying:\n", 0.05)
    ghostWriter(f"{green}1. Cash\n", 0.05)
    ghostWriter(f"{green}2. Credit Card/Debit Card\n", 0.05)
    payment_method = get_input(f"{white}Enter the number corresponding to the payment method you would like to use: {blue}", int)
    
    while payment_method < 1 or payment_method > 2:
        ghostWriter(f"{red}ERROR: {white}Invalid payment method! Please enter a valid number.\n", 0.05)
        payment_method = get_input(f"{white}Enter the number corresponding to the payment method you would like to use: {blue}", int)
    
    ghostWriter(f"{green}You have chosen payment method {payment_method}\n", 0.05)
    amount = get_input(f"{white}Enter the amount you would like to pay: ", float)
    difference = amount - total_cost
    ghostWriter(f"{white}The total cost of your purchase is ${total_cost}. You paid ${amount}. Change: ${difference}\n{blue}", 0.05)
    process_change(difference)

def process_change(difference):
    money_map = {
        50: "Fifty Dollar bills",
        20: "Twenty Dollar bills",
        10: "Ten Dollar bills",
        5: "Five Dollar bills",
        2: "Toonies",
        1: "Loonies",
        0.25: "Quarters",
        0.10: "Dimes",
        0.05: "Nickels",
        0.01: "Pennies",
    }
    change = {}
    for value, name in money_map.items():
        count = int(difference // value)
        if count > 0:
            change[name] = count
            difference = round(difference - count * value, 2)
    
    ghostWriter(f"\n{blue}Here is your change:\n", 0.05)
    for name, count in change.items():
        ghostWriter(f"{name}: {count}\n", 0.05)

def display_receipt(name, paint_choice, paint_cost, total_cost):
    date_str = datetime.now().strftime("%b %d, %Y")
    tax = round(paint_cost * 0.13, 2)
    subtotal = paint_cost
    total = round(total_cost, 2)
    receipt = f"""
*****************************************************
SIR MIXALOT PAINT
5353 Fake street, Burlington ON, N4C 4M2
invoice #: {randint(100000, 999999)}
Receiver Name: {name}
Date: {date_str}
Description: {paint_choice}
Quantity: {amount_of_paint}
Price per gallon: ${paint_cost}
Subtotal: ${subtotal}
Tax (13%): ${tax}
Total: ${total}
Balance Due: $0.00
Thank you for your business!
*****************************************************
"""
    ghostWriter(receipt, 0.01)

def custom_paint():
    properties = ["Color", "Gloss", "Water Resistant"]

    ghostWriter("You have picked a custom paint. Let's customize your paint", 0.05)
    for i in range(len(properties)):
        ghostWriter(f"{i+1}.) {properties[i]}:\n",0.05)






def main():
    run_program()
    paints = {
        "Custom Paint": 250,
        "Luxury Paint": 200,
        "Designer Paint": 150,
        "Premium Paint": 105,
        "Low Odor Paint": 90,
        "Regular Paint": 75,
        "Value Paint": 40,
    }
    ghostWriter(f"{green}Welcome to the Paint Program!\n", 0.05)
    name = get_input(f"{white}Enter your name: {blue}", str)    
    room_amount = get_input(f"{white}Enter the number of rooms you would like to paint: ", int)
    while room_amount < 1 or room_amount > 5:
        if room_amount < 1:
            ghostWriter(f"{red}ERROR: {white}At least one room must be painted.\n", 0.05)
        elif room_amount > 5:
            ghostWriter(f"{red}ERROR: {white}The maximum number of rooms that can be painted is 5. You need to do another order.\n", 0.05)
        room_amount = get_input(f"{white}Enter the number of rooms you would like to paint: ", int)
    total_area = process_room(room_amount)
    total_cost = process_paint(paints)
    process_payment(total_cost)
    display_receipt(name, paint_choice, paint_cost, total_cost)

if __name__ == "__main__":
    displayed = False
    run_count = 0
    skip_display = False
    while True:
        main()
        continue_choice = get_input(f"\n{white}Would you like to continue (yes/no)\n", str).lower()
        if continue_choice == "no":
            exit()
        elif continue_choice != "yes":
            ghostWriter(f"{red}ERROR: {white}Invalid input! Please enter yes or no.\n", 0.05)
            break