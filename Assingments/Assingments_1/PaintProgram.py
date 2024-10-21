from time import sleep
from datetime import datetime
from random import randint
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

"""
Date: 2024-09-18
Name: Themika Weerasuriya
This program is a simple program that will allow a user to choose from various interior paint options. Then give you an invoice on the cost
of painting the room, providing you with 2 payment options.

Functions used
Enumerate()
//https://www.w3schools.com/python/ref_func_enumerate.asp
isInstance()
//https://www.w3schools.com/python/ref_func_isinstance.asp
"""
# TODO do this during the weekend
# Add sound effects
# Add description to the paint 
# Add random discounts  


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

def process_payment(total_cost : float):
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
    properties = ["Color", "Gloss", "Water Resistant", "Finish Type", "Durability","Exit/Finish"]
    selected_properties = {}

    ghostWriter("You have picked a custom paint. Let's customize your paint\n", 0.05)
    for i in range(len(properties)):
        ghostWriter(f"{i+1}.) {properties[i]}:\n", 0.05)

    def create_window(title, label_text, widget, description_func):
        root = tk.Tk()
        root.title(title)
        root.attributes('-topmost', True)  # Ensure the window appears on top
        root.configure(bg="#2c3e50")
        frame = tk.Frame(root, bg="#ecf0f1", padx=20, pady=20, relief=tk.RAISED, bd=10)
        frame.pack(padx=10, pady=10)
        tk.Label(frame, text=label_text, font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=10)
        widget.pack(pady=10)
        tk.Button(frame, text="OK", command=root.quit, font=("Helvetica", 12), bg="#27ae60", fg="white", relief=tk.GROOVE).pack(pady=10)
        root.mainloop()
        value = widget.get() if isinstance(widget, tk.Scale) else widget.get()
        root.destroy()
        description, pros, cons = description_func(value)
        ghostWriter(f"{green}You have chosen {label_text.lower()} {value}\n", 0.05)
        ghostWriter(f"{white}{description}\n", 0.05)
        ghostWriter(f"{green}{pros}\n", 0.05)
        ghostWriter(f"{red}{cons}\n", 0.05)
        return value

    def gloss_description(gloss):
        description = f"Gloss amount {gloss} will give your paint a {'high' if gloss > 50 else 'low'} shine."
        pros = "Pros: High gloss provides a shiny finish that is easy to clean."
        cons = "Cons: High gloss can highlight imperfections on the surface."
        return description, pros, cons

    def water_resistant_description(water_resistant):
        description = f"Water resistance amount {water_resistant} will make your paint {'highly' if water_resistant > 50 else 'moderately'} resistant to water."
        pros = "Pros: High water resistance protects against moisture and mold."
        cons = "Cons: High water resistance may reduce breathability of the paint."
        return description, pros, cons

    def finish_description(finish_type):
        description = f"Finish type {finish_type} will give your paint a {finish_type.lower()} look."
        pros = f"Pros: {finish_type} finish provides a {finish_type.lower()} appearance."
        cons = f"Cons: {finish_type} finish may require more maintenance."
        return description, pros, cons

    def durability_description(durability_level):
        description = f"Durability level {durability_level} will make your paint {'extremely' if durability_level == 'Ultra' else 'highly' if durability_level == 'High' else 'moderately'} durable."
        pros = f"Pros: {durability_level} durability provides long-lasting protection."
        cons = f"Cons: {durability_level} durability may increase the cost."
        return description, pros, cons

    def show_tooltip(widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.wm_overrideredirect(True)
        tooltip.wm_geometry(f"+{widget.winfo_rootx() + 20}+{widget.winfo_rooty() + 20}")
        label = tk.Label(tooltip, text=text, bg="#ffffe0", relief=tk.SOLID, borderwidth=1, font=("Helvetica", 10))
        label.pack()
        widget.bind("<Enter>", lambda e: tooltip.deiconify())
        widget.bind("<Leave>", lambda e: tooltip.withdraw())
        tooltip.withdraw()

    while True:
        choice = get_input(f"{white}Enter the number corresponding to the property you would like to customize: {blue}", int)
        if choice < 1 or choice > len(properties):
            ghostWriter(f"{red}ERROR: {white}Invalid property! Please enter a valid number.\n", 0.05)
        elif choice == 1:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            root.attributes('-topmost', True)  # Ensure the window appears on top
            color = colorchooser.askcolor(title="Choose a color")[1]
            root.destroy()
            ghostWriter(f"{green}You have chosen color {color}\n", 0.05)
            selected_properties["Color"] = color
        elif choice == 2:
            root = tk.Tk()
            root.title("Choose Gloss Amount")
            root.attributes('-topmost', True)  # Ensure the window appears on top
            root.configure(bg="#2c3e50")
            frame = tk.Frame(root, bg="#ecf0f1", padx=20, pady=20, relief=tk.RAISED, bd=10)
            frame.pack(padx=10, pady=10)
            tk.Label(frame, text="Gloss Amount", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=10)
            gloss_slider = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300, bg="#ecf0f1", troughcolor="#27ae60", sliderlength=20)
            gloss_slider.pack(pady=10)
            gloss_value_label = tk.Label(frame, text="50", font=("Helvetica", 14), bg="#ecf0f1")
            gloss_value_label.pack(pady=10)
            gloss_slider.set(50)  # Set default value to 50

            def update_gloss_value(val):
                gloss_value_label.config(text=val)

            gloss_slider.config(command=update_gloss_value)
            tk.Button(frame, text="OK", command=root.quit, font=("Helvetica", 12), bg="#27ae60", fg="white", relief=tk.GROOVE).pack(pady=10)
            show_tooltip(gloss_slider, "Adjust the gloss level of the paint.")
            root.mainloop()
            gloss = gloss_slider.get()
            root.destroy()
            gloss_description = f"Gloss amount {gloss} will give your paint a {'high' if gloss > 50 else 'low'} shine."
            gloss_pros = "Pros: High gloss provides a shiny finish that is easy to clean."
            gloss_cons = "Cons: High gloss can highlight imperfections on the surface."
            ghostWriter(f"{green}You have chosen gloss amount {gloss}\n", 0.05)
            ghostWriter(f"{white}{gloss_description}\n", 0.05)
            ghostWriter(f"{green}{gloss_pros}\n", 0.05)
            ghostWriter(f"{red}{gloss_cons}\n", 0.05)
            selected_properties["Gloss"] = gloss
        elif choice == 3:
            root = tk.Tk()
            root.title("Choose Water Resistance Amount")
            root.attributes('-topmost', True)  # Ensure the window appears on top
            root.configure(bg="#2c3e50")
            frame = tk.Frame(root, bg="#ecf0f1", padx=20, pady=20, relief=tk.RAISED, bd=10)
            frame.pack(padx=10, pady=10)
            tk.Label(frame, text="Water Resistance Amount", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=10)
            water_resistant_slider = tk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL, length=300, bg="#ecf0f1", troughcolor="#27ae60", sliderlength=20)
            water_resistant_slider.pack(pady=10)
            water_resistant_value_label = tk.Label(frame, text="50", font=("Helvetica", 14), bg="#ecf0f1")
            water_resistant_value_label.pack(pady=10)
            water_resistant_slider.set(50)  # Set default value to 50

            def update_water_resistant_value(val):
                water_resistant_value_label.config(text=val)

            water_resistant_slider.config(command=update_water_resistant_value)
            tk.Button(frame, text="OK", command=root.quit, font=("Helvetica", 12), bg="#27ae60", fg="white", relief=tk.GROOVE).pack(pady=10)
            show_tooltip(water_resistant_slider, "Adjust the water resistance level of the paint.")
            root.mainloop()
            water_resistant = water_resistant_slider.get()
            root.destroy()
            water_resistant_description = f"Water resistance amount {water_resistant} will make your paint {'highly' if water_resistant > 50 else 'moderately'} resistant to water."
            water_resistant_pros = "Pros: High water resistance protects against moisture and mold."
            water_resistant_cons = "Cons: High water resistance may reduce breathability of the paint."
            ghostWriter(f"{green}You have chosen water resistant amount {water_resistant}\n", 0.05)
            ghostWriter(f"{white}{water_resistant_description}\n", 0.05)
            ghostWriter(f"{green}{water_resistant_pros}\n", 0.05)
            ghostWriter(f"{red}{water_resistant_cons}\n", 0.05)
            selected_properties["Water Resistant"] = water_resistant
        elif choice == 4:
            root = tk.Tk()
            root.title("Choose Finish Type")
            root.attributes('-topmost', True)  # Ensure the window appears on top
            root.configure(bg="#2c3e50")
            frame = tk.Frame(root, bg="#ecf0f1", padx=20, pady=20, relief=tk.RAISED, bd=10)
            frame.pack(padx=10, pady=10)
            tk.Label(frame, text="Finish Type", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=10)
            finish_var = tk.StringVar(value="Matte")
            finishes = ["Matte", "Eggshell", "Satin", "Semi-Gloss", "Gloss"]
            finish_dropdown = ttk.Combobox(frame, textvariable=finish_var, values=finishes, font=("Helvetica", 12))
            finish_dropdown.pack(pady=10)
            tk.Button(frame, text="OK", command=root.quit, font=("Helvetica", 12), bg="#27ae60", fg="white", relief=tk.GROOVE).pack(pady=10)
            show_tooltip(finish_dropdown, "Select the finish type of the paint.")
            root.mainloop()
            finish_type = finish_var.get()
            root.destroy()
            finish_description = f"Finish type {finish_type} will give your paint a {finish_type.lower()} look."
            finish_pros = f"Pros: {finish_type} finish provides a {finish_type.lower()} appearance."
            finish_cons = f"Cons: {finish_type} finish may require more maintenance."
            ghostWriter(f"{green}You have chosen finish type {finish_type}\n", 0.05)
            ghostWriter(f"{white}{finish_description}\n", 0.05)
            ghostWriter(f"{green}{finish_pros}\n", 0.05)
            ghostWriter(f"{red}{finish_cons}\n", 0.05)
            selected_properties["Finish Type"] = finish_type
        elif choice == 5:
            root = tk.Tk()
            root.title("Choose Durability Level")
            root.attributes('-topmost', True)  # Ensure the window appears on top
            root.configure(bg="#2c3e50")
            frame = tk.Frame(root, bg="#ecf0f1", padx=20, pady=20, relief=tk.RAISED, bd=10)
            frame.pack(padx=10, pady=10)
            tk.Label(frame, text="Durability Level", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=10)
            durability_var = tk.StringVar(value="Standard")
            durabilities = ["Standard", "High", "Ultra"]
            durability_dropdown = ttk.Combobox(frame, textvariable=durability_var, values=durabilities, font=("Helvetica", 12))
            durability_dropdown.pack(pady=10)
            tk.Button(frame, text="OK", command=root.quit, font=("Helvetica", 12), bg="#27ae60", fg="white", relief=tk.GROOVE).pack(pady=10)
            show_tooltip(durability_dropdown, "Select the durability level of the paint.")
            root.mainloop()
            durability_level = durability_var.get()
            root.destroy()
            durability_description = f"Durability level {durability_level} will make your paint {'extremely' if durability_level == 'Ultra' else 'highly' if durability_level == 'High' else 'moderately'} durable."
            durability_pros = f"Pros: {durability_level} durability provides long-lasting protection."
            durability_cons = f"Cons: {durability_level} durability may increase the cost."
            ghostWriter(f"{green}You have chosen durability level {durability_level}\n", 0.05)
            ghostWriter(f"{white}{durability_description}\n", 0.05)
            ghostWriter(f"{green}{durability_pros}\n", 0.05)
            ghostWriter(f"{red}{durability_cons}\n", 0.05)
            selected_properties["Durability"] = durability_level
        elif choice == 6:
            break
        

    # Show final preview
    root = tk.Tk()
    root.title("Paint Preview")
    root.attributes('-topmost', True)  # Ensure the window appears on top
    root.configure(bg="#2c3e50")
    frame = tk.Frame(root, bg="#ecf0f1", padx=20, pady=20, relief=tk.RAISED, bd=10)
    frame.pack(padx=10, pady=10)
    tk.Label(frame, text="Paint Preview", font=("Helvetica", 16, "bold"), bg="#ecf0f1").pack(pady=10)
    for prop, value in selected_properties.items():
        tk.Label(frame, text=f"{prop}: {value}", font=("Helvetica", 14), bg="#ecf0f1").pack(pady=5)
    tk.Button(frame, text="Finish", command=root.quit, font=("Helvetica", 12), bg="#27ae60", fg="white", relief=tk.GROOVE).pack(pady=10)
    root.mainloop()
    root.destroy()

def main():
    # run_program()
    # paints = {
    #     "Custom Paint": 250,
    #     "Luxury Paint": 200,
    #     "Designer Paint": 150,
    #     "Premium Paint": 105,
    #     "Low Odor Paint": 90,
    #     "Regular Paint": 75,
    #     "Value Paint": 40,
    # }
    # ghostWriter(f"{green}Welcome to the Paint Program!\n", 0.05)
    # name = get_input(f"{white}Enter your name: {blue}", str)    
    # room_amount = get_input(f"{white}Enter the number of rooms you would like to paint: ", int)
    # while room_amount < 1 or room_amount > 5:
    #     if room_amount < 1:
    #         ghostWriter(f"{red}ERROR: {white}At least one room must be painted.\n", 0.05)
    #     elif room_amount > 5:
    #         ghostWriter(f"{red}ERROR: {white}The maximum number of rooms that can be painted is 5. You need to do another order.\n", 0.05)
    #     room_amount = get_input(f"{white}Enter the number of rooms you would like to paint: ", int)
    # total_area = process_room(room_amount)
    # total_cost = process_paint(paints)
    # process_payment(total_cost)
    # display_receipt(name, paint_choice, paint_cost, total_cost)
    custom_paint()

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