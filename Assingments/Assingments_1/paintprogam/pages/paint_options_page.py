import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import colorchooser
from tkinter import messagebox

# Translations for different languages
translations = {
    "English": {
        "select_paint": "Select Your Paint",
        "confirm_paint_selection": "Confirm Paint Selection",
        "custom_paint_options": "Custom Paint Options",
        "choose_paint_color": "Choose Paint Color:",
        "select_color": "Select Color",
        "confirm_color": "Confirm Color",
        "choose_finish_type": "Choose Finish Type:",
        "water_resistance_amount": "Water Resistance Amount:",
        "choose_durability_level": "Choose Durability Level:",
        "uv_protection_level": "UV Protection Level:",
        "scratch_resistance": "Scratch Resistance:",
        "eco_friendly": "Eco-Friendly:",
        "drying_time": "Drying Time (hours):",
        "voc_level": "VOC Level (g/L):",
        "confirm_custom_paint_options": "Confirm Custom Paint Options",
        "cost_before_tax": "Cost Before Tax",
        "cost_after_tax": "Cost After Tax",
        "matte": "Matte",
        "glossy": "Glossy",
        "satin": "Satin",
        "low": "Low",
        "medium": "Medium",
        "high": "High",
        "standard": "Standard",
        "premium": "Premium",
        "ultra": "Ultra",
        "no": "No",
        "yes": "Yes"
    },
    "French": {
        "select_paint": "Sélectionnez votre peinture",
        "confirm_paint_selection": "Confirmer la sélection de peinture",
        "custom_paint_options": "Options de peinture personnalisées",
        "choose_paint_color": "Choisissez la couleur de la peinture:",
        "select_color": "Choisir la couleur",
        "confirm_color": "Confirmer la couleur",
        "choose_finish_type": "Choisissez le type de finition:",
        "water_resistance_amount": "Quantité de résistance à l'eau:",
        "choose_durability_level": "Choisissez le niveau de durabilité:",
        "uv_protection_level": "Niveau de protection UV:",
        "scratch_resistance": "Résistance aux rayures:",
        "eco_friendly": "Écologique:",
        "drying_time": "Temps de séchage (heures):",
        "coverage_per_gallon": "Couverture par gallon (pi²):",
        "voc_level": "Niveau de COV (g/L):",
        "confirm_custom_paint_options": "Confirmer les options de peinture personnalisées",
        "cost_before_tax": "Coût avant taxes",
        "cost_after_tax": "Coût après taxes",
        "matte": "Mat",
        "glossy": "Brillant",
        "satin": "Satiné",
        "low": "Faible",
        "medium": "Moyenne",
        "high": "Haute",
        "standard": "Standard",
        "premium": "Premium",
        "ultra": "Ultra",
        "no": "Non",
        "yes": "Oui"
    }
}


class PaintOptionsPage(ttk.Frame):
    def __init__(self, container, parent):
        super().__init__(container)
        self.parent = parent
        # Set the language to the parent's current language
        self.language = parent.current_language
        """Paint options page for selecting paint type and customizing paint options."""    
        self.color_var = tk.StringVar(value="Red")
        self.finish_type_var = tk.StringVar(value=translations[self.language]["matte"])
        self.water_resistance_var = tk.StringVar(value=translations[self.language]["low"])
        self.durability_var = tk.StringVar(value=translations[self.language]["standard"])
        self.uv_protection_var = tk.StringVar(value=translations[self.language]["low"])
        self.scratch_resistance_var = tk.StringVar(value=translations[self.language]["low"])
        self.eco_friendly_var = tk.StringVar(value="No")
        self.drying_time_var = tk.StringVar(value="1")
        self.coverage_var = tk.StringVar(value="400")
        self.voc_var = tk.StringVar(value="50")
        self.create_widgets()
    # Create the widgets for the paint options page
    def create_widgets(self):
        self.label = ttk.Label(self, text=translations[self.language]["select_paint"], font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)
        # Dictionary of paint options and their prices
        self.paints = {
            "Value Paint": 40,
            "Regular Paint": 75,
            "Low Odor Paint": 90,
            "Premium Paint": 105,
            "Designer Paint": 150,
            "Luxury Paint": 200,
            "Custom Paint": 250,
        }
        # Create radio buttons for selecting paint type
        self.paint_choice_var = tk.StringVar(value="Value Paint")
        self.paint_choice_var.trace("w", self.on_paint_selection_change)
        row = 1
        # Create radio buttons for each paint type
        for paint, price in self.paints.items():
            ttk.Radiobutton(self, text=f"{paint}: ${price} per gallon", variable=self.paint_choice_var, value=paint).grid(row=row, column=0, sticky=tk.W, pady=5, padx=50)
            row += 1
        # Add a button to confirm paint selection
        self.confirm_button = ttk.Button(self, text=translations[self.language]["confirm_paint_selection"], command=self.on_confirm_paint, bootstyle="success")
        self.confirm_button.grid(row=row, column=0, columnspan=2, pady=10)

    def create_custom_paint_panel(self, selected_paint):
        # Remove the previous custom paint panel if it exists
        if hasattr(self, 'custom_paint_frame'):
            self.custom_paint_frame.grid_remove()
        # Create a frame for custom paint options
        self.custom_paint_frame = ttk.Frame(self)
        self.custom_paint_frame.grid(row=0, column=2, rowspan=len(self.paints) + 4, padx=20, pady=10, sticky=tk.N)
    
        # Add a label for the paint preview
        label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["custom_paint_options"], font=("Helvetica", 16, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=10)
    
        # Add a canvas for paint preview
        self.preview_canvas = tk.Canvas(self.custom_paint_frame, width=200, height=300, bg="white")
        self.preview_canvas.grid(row=0, column=2, rowspan=10, padx=10, pady=10)
        
        self.update_paint_preview()
        # Add options for paint color
        color_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["choose_paint_color"])
        color_label.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)
        color_button = ttk.Button(self.custom_paint_frame, text=translations[self.language]["select_color"], command=self.choose_color, bootstyle="info")
        color_button.grid(row=1, column=1, pady=5, padx=5)
        # Add a button to confirm the selected color
        color_button_confirm = ttk.Button(self.custom_paint_frame, text=translations[self.language]["confirm_color"], bootstyle="info")
        color_button_confirm.grid(row=2, column=1, pady=5, padx=5)
        color_button_confirm.bind("<ButtonRelease-1>", lambda e: self.update_paint_preview())
        
        # Add options for finish type
        finish_type_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["choose_finish_type"])
        finish_type_label.grid(row=3, column=0, pady=5, padx=5, sticky=tk.W)
        finish_type_options = [translations[self.language]["matte"], translations[self.language]["glossy"], translations[self.language]["satin"]]
        finish_type_combobox = ttk.Combobox(self.custom_paint_frame, values=finish_type_options, textvariable=self.finish_type_var, bootstyle="info", state="readonly")
        finish_type_combobox.grid(row=3, column=1, pady=5, padx=5)
        finish_type_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_paint_preview())
    
        # Determine the number of options based on the selected paint
        paint_options = {
            "Value Paint": 1,
            "Regular Paint": 2,
            "Low Odor Paint": 3,
            "Premium Paint": 4,
            "Designer Paint": 5,
            "Luxury Paint": 6,
            "Custom Paint": 7,
        }
        num_options = paint_options.get(selected_paint, 1)
    
        if num_options >= 2:
            # Add options for water resistance amount
            water_resistance_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["water_resistance_amount"])
            water_resistance_label.grid(row=4, column=0, pady=5, padx=5, sticky=tk.W)
            water_resistance_options = [translations[self.language]["low"], translations[self.language]["medium"], translations[self.language]["high"]]
            self.water_resistance_combobox = ttk.Combobox(self.custom_paint_frame, values=water_resistance_options, textvariable=self.water_resistance_var, bootstyle="info", state="readonly")
            self.water_resistance_combobox.grid(row=4, column=1, pady=5, padx=5)
            self.water_resistance_combobox.bind("<<ComboboxSelected>>", lambda e: self.update_paint_preview())
        
        if num_options >= 3:
            # Add options for durability level
            durability_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["choose_durability_level"])
            durability_label.grid(row=5, column=0, pady=5, padx=5, sticky=tk.W)
            durability_options = [translations[self.language]["standard"], translations[self.language]["premium"], translations[self.language]["ultra"]]
            self.durability_combobox = ttk.Combobox(self.custom_paint_frame, values=durability_options, textvariable=self.durability_var, bootstyle="info")
            self.durability_combobox.grid(row=5, column=1, pady=5, padx=5)
        
        if num_options >= 4:
            # Add options for UV protection level
            uv_protection_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["uv_protection_level"])
            uv_protection_label.grid(row=6, column=0, pady=5, padx=5, sticky=tk.W)
            uv_protection_options = [translations[self.language]["low"], translations[self.language]["medium"], translations[self.language]["high"]]
            self.uv_protection_combobox = ttk.Combobox(self.custom_paint_frame, values=uv_protection_options, textvariable=self.uv_protection_var, bootstyle="info")
            self.uv_protection_combobox.grid(row=6, column=1, pady=5, padx=5)
        
        if num_options >= 5:
            # Add options for scratch resistance
            scratch_resistance_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["scratch_resistance"])
            scratch_resistance_label.grid(row=7, column=0, pady=5, padx=5, sticky=tk.W)
            scratch_resistance_options = [translations[self.language]["low"], translations[self.language]["medium"], translations[self.language]["high"]]
            self.scratch_resistance_combobox = ttk.Combobox(self.custom_paint_frame, values=scratch_resistance_options, textvariable=self.scratch_resistance_var, bootstyle="info")
            self.scratch_resistance_combobox.grid(row=7, column=1, pady=5, padx=5)
        
        if num_options >= 6:
            # Add options for eco-friendly
            eco_friendly_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["eco_friendly"])
            eco_friendly_label.grid(row=8, column=0, pady=5, padx=5, sticky=tk.W)
            eco_friendly_options = [translations[self.language]["no"], translations[self.language]["yes"]]
            self.eco_friendly_combobox = ttk.Combobox(self.custom_paint_frame, values=eco_friendly_options, textvariable=self.eco_friendly_var, bootstyle="info")
            self.eco_friendly_combobox.grid(row=8, column=1, pady=5, padx=5)
        
        if num_options >= 7:
            # Add options for drying time
            drying_time_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["drying_time"])
            drying_time_label.grid(row=9, column=0, pady=5, padx=5, sticky=tk.W)
            drying_time_entry = ttk.Entry(self.custom_paint_frame, textvariable=self.drying_time_var, bootstyle="info")
            drying_time_entry.grid(row=9, column=1, pady=5, padx=5)
            # Add options for VOC level
            voc_label = ttk.Label(self.custom_paint_frame, text=translations[self.language]["voc_level"])
            voc_label.grid(row=11, column=0, pady=5, padx=5, sticky=tk.W)
            voc_entry = ttk.Entry(self.custom_paint_frame, textvariable=self.voc_var, bootstyle="info")
            voc_entry.grid(row=11, column=1, pady=5, padx=5)
    
        # Add a button to confirm custom paint options
        confirm_custom_paint_button = ttk.Button(self.custom_paint_frame, text=translations[self.language]["confirm_custom_paint_options"], command=self.on_confirm_custom_paint, bootstyle="success")
        confirm_custom_paint_button.grid(row=12, column=0, columnspan=2, pady=10)    

    def choose_color(self):
        # Open a color chooser dialog and set the selected color
        color_code = colorchooser.askcolor(title="Choose color")[1]
        # Set the selected color if a color is chosen
        if color_code:
            self.color_var.set(color_code)
            print(f"Selected Color: {color_code}")  

    def update_paint_preview(self):
        """Update the paint preview based on selected options."""
        print("Updating paint preview...")  # Debugging statement
        # Clear previous preview
        self.preview_canvas.delete("all")

        # Get the selected color and finish type
        selected_color = self.color_var.get() if self.color_var.get() != "Red" else "#FF0000"  # Default Red
        selected_finish_type = self.finish_type_var.get()
        
        # Draw a rectangle to represent the paint
        self.preview_canvas.create_rectangle(20, 20, 180, 280, fill=selected_color, outline="")

        # Add effects based on finish type
        if selected_finish_type == ("Glossy"):
            # Simulate gloss with white highlights
            self.preview_canvas.create_line(20, 20, 180, 100, fill="white", width=5)
        elif selected_finish_type == ("Satin"):
            # Add some sheen with a lighter shade
            lighter_color = self.lighter_color(selected_color)
            self.preview_canvas.create_rectangle(20, 20, 180, 280, fill=lighter_color, outline="")

    def lighter_color(self, color):
        """Return a lighter shade of the given color."""
        # Get the RGB values of the color and increase each value by 20%
        r, g, b = self.winfo_rgb(color)
        # Increase each value by 20% and ensure it is within the valid range
        r = min(255, int(r / 256 * 1.2))
        g = min(255, int(g / 256 * 1.2))
        b = min(255, int(b / 256 * 1.2))
        # Convert the RGB values to hexadecimal and return the color
        return f'#{r:02x}{g:02x}{b:02x}'

    def on_confirm_custom_paint(self):
        # Get the selected options
        selected_color = self.color_var.get()
        selected_water_resistance = self.water_resistance_var.get()
        selected_finish_type = self.finish_type_var.get()
        selected_durability = self.durability_var.get()

        # Validate VOC level, and drying time
        try:
            voc_level = float(self.voc_var.get())
            coverage = float(self.coverage_var.get())
            drying_time = float(self.drying_time_var.get())
            # Validate input
            if voc_level < 0:
                messagebox.showerror("Input Error", "VOC Level cannot be negative.")
                return
            if drying_time < 0:
                messagebox.showerror("Input Error", "Drying time cannot be negative.")
                return
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")
            return
        # Update user data with selected options
        self.parent.user_data.update({
            "color": selected_color,
            "water_resistance": selected_water_resistance,
            "finish_type": selected_finish_type,
            "durability": selected_durability,
            "uv_protection": self.uv_protection_var.get(),
        })
        # Display the selected options
        print(f"Selected Color: {selected_color}")
        print(f"Selected Water Resistance: {selected_water_resistance}")
        print(f"Selected Finish Type: {selected_finish_type}")
        print(f"Selected Durability: {selected_durability}")
        
        # Create the payment page
        self.parent.create_payment_page(self.parent.user_data["cost_before_tax"], self.parent.user_data["cost_after_tax"])

    def on_paint_selection_change(self, *args):
        # Get the selected paint
        selected_paint = self.paint_choice_var.get()
        self.create_custom_paint_panel(selected_paint)

    def on_confirm_paint(self):
        # Get the selected paint and its price
        selected_paint = self.paint_choice_var.get()
        paint_price = self.paints[selected_paint]
        
        # Ensure wall_entries is accessible
        wall_entries = self.parent.pages['Rooms'].wall_entries
        self.parent.user_data.update({"paint_choice": selected_paint})
        # Calculate total square footage
        total_square_footage = 0
        # Iterate over each room's wall entries
        for room_entries in wall_entries.values():
            # Calculate the square footage of each wall and add it to the total
            for i in range(0, len(room_entries), 2):
                # Get the length and width of the wall
                length = float(room_entries[i].get().strip())
                width = float(room_entries[i + 1].get().strip())
                total_square_footage += length * width
        
        # Calculate paint cans needed
        coverage_per_gallon = 400  # Assuming 400 sq ft per gallon
        self.paint_cans_needed = int(total_square_footage / coverage_per_gallon) + (total_square_footage % coverage_per_gallon > 0)
        
        # Calculate cost before and after tax
        cost_before_tax = round(self.paint_cans_needed * paint_price,3)
        print(f"Cost Before Tax: {cost_before_tax}")
        cost_after_tax = cost_before_tax * 1.13  # Assuming a tax rate of 13%
        self.parent.user_data.update({"cost_before_tax": cost_before_tax, "cost_after_tax": cost_after_tax})
        
        # Display the costs
        self.cost_label_before_tax = ttk.Label(self.parent.pages['PaintOptions'], text=f"{translations[self.language]['cost_before_tax']}: ${round(cost_before_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_before_tax.grid(row=len(self.paints) + 2, column=0, columnspan=2, pady=10, padx=50)
        # Display the costs
        self.cost_label_after_tax = ttk.Label(self.parent.pages['PaintOptions'], text=f"{translations[self.language]['cost_after_tax']}: ${round(cost_after_tax, 2)}", font=("Helvetica", 12, "bold"))
        self.cost_label_after_tax.grid(row=len(self.paints) + 3, column=0, columnspan=2, pady=10, padx=50)
        
        print(f"Selected Paint: {selected_paint}")
        print(f"Cost Before Tax: ${round(cost_before_tax, 2)}")
        print(f"Cost After Tax: ${round(cost_after_tax, 2)}")
        
        # Create custom paint panel if the selected paint is "Custom Paint"
        self.create_custom_paint_panel(selected_paint)

    def update_language(self, language):
        # Update the language of the page
        self.language = language
        # Update the label with the new language
        self.label.config(text=translations[language]["select_paint"])
        self.confirm_button.config(text=translations[language]["confirm_paint_selection"])
        # Update the custom paint panel if it exists
        if hasattr(self, 'custom_paint_frame'):
            self.custom_paint_frame.grid_remove()
        # Update the cost labels
        self.create_custom_paint_panel(self.paint_choice_var.get())
        self.cost_label_before_tax.config(text=translations[language]["cost_before_tax"])
        self.cost_label_after_tax.config(text=translations[language]["cost_after_tax"])