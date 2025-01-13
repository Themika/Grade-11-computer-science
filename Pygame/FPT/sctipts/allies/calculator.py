import tkinter as tk
from tkinter import ttk
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("400x600")

        self.expression = ""
        self.previous_answer = ""
        self.input_text = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.Frame(self.root)
        input_frame.pack(expand=True, fill='both')

        input_field = ttk.Entry(input_frame, textvariable=self.input_text, font=('arial', 18, 'bold'), justify='right')
        input_field.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=8, sticky='nsew')

        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(expand=True, fill='both')

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('sin', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('cos', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('tan', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3), ('log', 4, 4),
            ('C', 5, 0), ('(', 5, 1), (')', 5, 2), ('^', 5, 3), ('sqrt', 5, 4),
            ('Graph', 6, 0, 5)
        ]

        for button in buttons:
            text, row, col = button[:3]
            colspan = button[3] if len(button) == 4 else 1
            button = ttk.Button(buttons_frame, text=text, command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, columnspan=colspan, ipadx=10, ipady=10, padx=5, pady=5, sticky='nsew')

        for i in range(7):
            buttons_frame.grid_rowconfigure(i, weight=1)
            buttons_frame.grid_columnconfigure(i, weight=1)

    def on_button_click(self, char):
        if char == '=':
            try:
                self.expression = self.expression.replace('^', '**')
                result = str(eval(self.expression))
                self.input_text.set(result)
                self.previous_answer = result
                self.expression = result
            except:
                self.input_text.set("Error")
                self.expression = ""
        elif char == 'C':
            self.expression = ""
            self.input_text.set("")
        elif char in ('sin', 'cos', 'tan', 'log', 'sqrt'):
            try:
                if char == 'sin':
                    result = str(math.sin(math.radians(float(self.expression))))
                elif char == 'cos':
                    result = str(math.cos(math.radians(float(self.expression))))
                elif char == 'tan':
                    result = str(math.tan(math.radians(float(self.expression))))
                elif char == 'log':
                    result = str(math.log10(float(self.expression)))
                elif char == 'sqrt':
                    result = str(math.sqrt(float(self.expression)))
                self.input_text.set(result)
                self.previous_answer = result
                self.expression = result
            except:
                self.input_text.set("Error")
                self.expression = ""
        elif char == 'Graph':
            self.plot_graph()
        else:
            if self.expression == self.previous_answer:
                self.expression = ""
            self.expression += str(char)
            self.input_text.set(self.expression)

    def plot_graph(self):
        try:
            x = np.linspace(-10, 10, 400)
            y = eval(self.expression.replace('^', '**'))
            fig, ax = plt.subplots()
            ax.plot(x, y)
            ax.set(xlabel='x', ylabel='y', title='Graph of ' + self.expression)
            ax.grid()

            graph_window = tk.Toplevel(self.root)
            graph_window.title("Graph")
            graph_window.geometry("600x600")

            canvas = FigureCanvasTkAgg(fig, master=graph_window)
            canvas.draw()
            canvas.get_tk_widget().pack(expand=True, fill='both')
        except:
            self.input_text.set("Error")
            self.expression = ""

if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()