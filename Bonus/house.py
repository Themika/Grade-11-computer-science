from turtle import *
import time
import random
from turtle import Screen, Turtle



class Bee:
    def __init__(self):
        self.t = Turtle()
        self.t.speed(10000)
        self.side = 25
        self.bee_w, self.bee_l = 7 * self.side, 10 * self.side
        self.setup()

    def setup(self):
        self.t.pensize(2)
        self.t.up()
        self.t.goto(0, -150)
        self.t.setheading(25)  # Set the heading to 25 degrees
        self.t.down()

    def draw_body(self):
        self.t.color('#FFEE5F')
        self.t.begin_fill()
        for i in range(2):
            self.t.forward(self.bee_l)
            self.t.left(60)
            self.t.forward(self.bee_w)
            self.t.left(60)
            self.t.forward(self.bee_w)
            self.t.left(60)
        self.t.end_fill()

    def draw_pollen(self):
        self.t.color('#FFD75E')
        self.t.begin_fill()
        for i in range(2):
            self.t.forward(self.bee_l)
            self.t.left(60)
            self.t.forward(self.side)
            self.t.left(120)
        self.t.end_fill()

        self.t.left(120)
        self.t.begin_fill()
        for i in range(2):
            self.t.forward(self.bee_w)
            self.t.right(60)
            self.t.forward(self.side)
            self.t.right(120)
        self.t.end_fill()

    def draw_stripes(self, thick):
        self.t.color('#7A3D13')
        self.t.begin_fill()
        self.t.forward(thick * self.side)
        self.t.left(60)
        self.t.forward(self.bee_w)
        self.t.left(60)
        self.t.forward(self.bee_w)
        self.t.left(60)
        self.t.forward(thick * self.side)
        self.t.left(120)
        self.t.forward(self.bee_w)
        self.t.right(60)
        self.t.forward(self.bee_w)
        self.t.left(120)
        self.t.end_fill()

    def draw_legs(self, length):
        self.t.begin_fill()
        self.t.forward(self.side)
        self.t.left(60)
        self.t.forward(self.side * (length - 1))
        self.t.left(60)
        self.t.forward(self.side)
        self.t.left(120)
        self.t.forward(self.side * length)
        self.t.left(120)
        self.t.end_fill()

    def draw_eyes_and_antennae(self):
        # Left side eye
        self.t.color('black')
        self.t.pendown()
        self.t.begin_fill()
        self.t.forward(self.side)
        self.t.left(60)
        self.t.forward(3 * self.side)
        self.t.left(120)
        self.t.forward(self.side)
        self.t.right(60)
        self.t.forward(self.side)
        self.t.left(120)
        self.t.forward(self.side)
        self.t.right(120)
        self.t.forward(self.side)
        self.t.left(120)
        self.t.forward(2 * self.side)
        self.t.end_fill()

        # Colored section of left eye
        self.t.left(180)
        self.t.forward(2 * self.side)
        self.t.color('#30C8BE')
        self.t.begin_fill()
        for i in range(2):
            for value in [120, 60]:
                self.t.forward(self.side)
                self.t.right(value)
        self.t.end_fill()

        # Left side antenna
        self.t.forward(self.side)
        self.t.penup()
        self.t.left(60)
        self.t.forward(self.side)
        self.t.right(120)
        self.t.color('black')
        self.t.pendown()
        self.t.begin_fill()
        self.t.forward(self.side)
        self.t.right(60)
        self.t.forward(self.side)
        self.t.left(120)
        self.t.forward(self.side)
        self.t.left(60)
        self.t.forward(self.side)
        self.t.left(60)
        self.t.forward(self.side)
        self.t.end_fill()

        self.t.right(120)
        self.t.begin_fill()
        self.t.forward(self.side)
        self.t.left(120)
        self.t.forward(2 * self.side)
        self.t.left(60)
        self.t.forward(self.side)
        self.t.end_fill()

        # Right side eye
        self.t.begin_fill()
        self.t.forward(2 * self.side)
        self.t.right(120)
        self.t.forward(2 * self.side)
        self.t.right(60)
        self.t.forward(3 * self.side)
        self.t.right(120)
        self.t.forward(self.side)
        self.t.right(60)
        self.t.forward(self.side)
        self.t.end_fill()

        # Right side antenna
        self.t.left(180)
        self.t.forward(2 * self.side)
        self.t.begin_fill()
        self.t.left(120)
        self.t.forward(2 * self.side)
        self.t.right(120)
        self.t.forward(self.side)
        self.t.right(60)
        self.t.forward(2 * self.side)
        for i in range(3):
            self.t.right(60)
            self.t.forward(self.side)
        self.t.end_fill()

        # Colored part of right eye
        self.t.left(60)
        self.t.color('#30C8BE')
        self.t.begin_fill()
        for i in range(2):
            for value in [60, 120]:
                self.t.forward(self.side)
                self.t.left(value)
        self.t.end_fill()

    def draw_outline(self):
        self.t.right(120)
        self.t.color('black')
        self.t.forward(self.side)
        self.t.right(60)
        self.t.forward(3 * self.side)
        for i in range(2):
            self.t.right(60)
            self.t.forward(10 * self.side)
            self.t.right(60)
            self.t.forward(7 * self.side)
            self.t.right(60)
            self.t.forward(7 * self.side)
        self.t.right(120)
        self.t.forward(7 * self.side)
        self.t.right(60)
        self.t.forward(7 * self.side)
        self.t.right(180)
        self.t.forward(7 * self.side)
        self.t.right(60)
        self.t.forward(10 * self.side)
    #TODO fix wings
    def draw_wings(self):
        pass

    def draw(self):
        self.draw_body()
        self.draw_pollen()
        self.t.right(120)
        self.t.forward(4 * self.side)
        self.draw_stripes(1)
        self.t.penup()
        self.t.forward(2 * self.side)
        self.t.pendown()
        self.draw_stripes(1)
        self.t.penup()
        self.t.forward(2 * self.side)
        self.t.pendown()
        self.draw_stripes(2)
        self.t.penup()
        self.t.left(180)
        self.t.forward(2 * self.side)
        self.t.pendown()
        self.draw_legs(2)
        self.t.forward(self.side * 2)
        self.draw_legs(2)
        self.t.forward(self.side * 2)
        self.draw_legs(1)
        self.t.penup()
        self.t.forward(2 * self.side)
        self.t.right(120)
        self.t.forward(self.side)
        self.t.right(60)
        self.draw_eyes_and_antennae()
        self.draw_outline()
        self.draw_wings()
        self.t.hideturtle()

class Swarm:
    def __init__(self, num_bees):
        self.num_bees = num_bees
        self.bees = []

    def create_swarm(self):
        positions = []
        for _ in range(self.num_bees):
            bee = Bee()
            bee.side = random.randint(10,15)  # Random size for each bee
            bee.bee_w, bee.bee_l = 7 * bee.side, 10 * bee.side
            bee.t.penup()
            while True:
                x, y = random.randint(-650, 650), random.randint(-400, 400)
                if all(abs(x - px) > 20 and abs(y - py) > 20 for px, py in positions):
                    positions.append((x, y))
                    break
            bee.t.goto(x, y)
            bee.t.pendown()
            self.bees.append(bee)

    def draw_swarm(self):
        for bee in self.bees:
            bee.draw()
            bee.t.penup()
            bee.t.goto(random.randint(-200, 200), random.randint(-200, 200))
            bee.t.pendown()

class Tree:
    def __init__(self, x, y, side):
        self.t = Turtle()
        self.t.speed(10000)
        self.side = side
        self.x = x
        self.y = y
        self.setup()

    def setup(self):
        self.t.pensize(2)
        self.t.up()
        self.t.goto(self.x, self.y)
        self.t.down()

    def draw_trunk(self):
        """Draw the trunk of the tree as a rectangle."""
        self.t.color('#8B4513')
        self.t.begin_fill()
        for _ in range(2):
            self.t.forward(self.side * 2)
            self.t.left(90)
            self.t.forward(self.side * 4)
            self.t.left(90)
        self.t.end_fill()

    def draw_square(self, side_length):
        """Draw a square with the given side length."""
        for _ in range(4):
            self.t.forward(side_length)
            self.t.left(90)

    def draw_leaves(self):
        """Draw the leaves of the tree as stacked squares."""
        self.t.color('#228B22')
        self.t.left(90)
        self.t.forward(self.side * 4)
        self.t.right(90)
        for i in range(3):
            self.t.begin_fill()
            self.t.penup()
            self.t.backward(self.side * 2)
            self.t.pendown()
            self.draw_square(self.side * 6)
            self.t.end_fill()
            self.t.penup()
            self.t.forward(self.side * 2)
            self.t.left(90)
            self.t.forward(self.side * 2)
            self.t.right(90)
            self.t.pendown()
    def draw_honey_square(self):
        """Draw a yellow honey square on the tree."""
        self.t.color('#FFD700')
        self.t.begin_fill()
        self.draw_square(self.side)
        self.t.end_fill()
    def draw(self):
        self.draw_trunk()
        self.draw_leaves()
        if random.randint(1, 25) == 1:
            self.t.penup()
            self.t.goto(self.x + self.side, self.y + self.side * 4)
            self.t.pendown()
            self.draw_honey_square()
        self.t.hideturtle()

class Forest:
    def __init__(self, num_trees):
        self.num_trees = num_trees
        self.trees = []

    def create_forest(self):
        for _ in range(self.num_trees):
            x = random.randint(-650, 650)
            y = random.randint(-410, -400)
            side = random.randint(10, 20)  # Random size for each tree
            tree = Tree(x, y, side)
            self.trees.append(tree)

    def draw_forest(self):
        for tree in self.trees:
            tree.draw()
def draw_grass():
    grass_turtle = Turtle()
    grass_turtle.speed(10000)
    grass_turtle.color('green')
    grass_turtle.penup()
    grass_turtle.goto(-800, -400)
    grass_turtle.pendown()
    grass_turtle.begin_fill()
    for _ in range(2):
        grass_turtle.forward(1600)
        grass_turtle.right(90)
        grass_turtle.forward(75)
        grass_turtle.right(90)
    grass_turtle.end_fill()
    grass_turtle.hideturtle()

def draw_mountain_range():
    mountain_turtle = Turtle()
    mountain_turtle.speed(10)
    mountain_turtle.penup()
    mountain_turtle.goto(-800, -250)  # Position the mountains just above the grass level
    mountain_turtle.pendown()

    # Base colors for different mountain layers
    base_colors = ["dim gray", "slate gray", "dark gray", "light slate gray", "gray", "light steel blue", "cadet blue"]

    
    # List of base positions for start, peak, and end of mountains, scaled by 1.2 for size increase
    mountain_positions = [
        (-800 * 1.2, -450 * 1.2, -600 * 1.2, -150 * 1.2, -400 * 1.2), 
        (-750 * 1.2, -450 * 1.2, -500 * 1.2, -120 * 1.2, -250 * 1.2), 
        (-700 * 1.2, -450 * 1.2, -450 * 1.2, -170 * 1.2, -200 * 1.2), 
        (-600 * 1.2, -450 * 1.2, -400 * 1.2, -100 * 1.2, -200 * 1.2),
        (-500 * 1.2, -450 * 1.2, -300 * 1.2, -80 * 1.2, -100 * 1.2),
        (-450 * 1.2, -450 * 1.2, -200 * 1.2, -140 * 1.2, -50 * 1.2),   
        (-300 * 1.2, -450 * 1.2, -100 * 1.2, -100 * 1.2, 100 * 1.2),
        (-200 * 1.2, -450 * 1.2, 0 * 1.2, -120 * 1.2, 200 * 1.2),    
        (0 * 1.2, -450 * 1.2, 100 * 1.2, -160 * 1.2, 300 * 1.2),      
        (100 * 1.2, -450 * 1.2, 250 * 1.2, -150 * 1.2, 400 * 1.2),   
        (250 * 1.2, -450 * 1.2, 400 * 1.2, -180 * 1.2, 550 * 1.2),    
        (400 * 1.2, -450 * 1.2, 600 * 1.2, -200 * 1.2, 800 * 1.2)     
    ]

    # Draw each layer of mountains, starting from the back (layer 7) to the front (layer 0)
    for layer in range(3, -1, -1):
        # Offset position to simulate depth
        y_offset = -250 + layer * 30  # Increase y position with each layer
        color = base_colors[layer % len(base_colors)]
        
        # Draw each mountain in mountain_positions for the current layer
        for x_start, y_start, x_peak, y_peak, x_end in mountain_positions:
            # Apply random variation to peak and base positions for shape variety
            x_peak_variation = x_peak + random.randint(-50, 50)
            y_peak_variation = y_peak + random.randint(-30, 30)
            x_end_variation = x_end + random.randint(-50, 50)

            mountain_turtle.penup()
            mountain_turtle.goto(x_start, y_start + y_offset)
            mountain_turtle.pendown()

            mountain_turtle.color(color)
            mountain_turtle.begin_fill()
            mountain_turtle.goto(x_peak_variation, y_peak_variation + y_offset)  # Varying peak of the mountain
            mountain_turtle.goto(x_end_variation, y_start + y_offset)  # Varying base of the mountain
            mountain_turtle.end_fill()

    mountain_turtle.hideturtle()

def draw_gradient_background():
    screen = Screen()
    screen.setup(width=1600, height=900)
    
    gradient_turtle = Turtle()
    gradient_turtle.hideturtle()
    gradient_turtle.speed(0)
    
    # Define the starting and ending colors for the gradient
    start_color = (135, 206, 250)  # Light sky blue
    end_color = (25, 25, 112)      # Midnight blue
    
    # Split the gradient into layers for the effect
    num_layers = 20
    screen.tracer(0)
    for i in range(num_layers):
        r = start_color[0] + i * (end_color[0] - start_color[0]) // num_layers
        g = start_color[1] + i * (end_color[1] - start_color[1]) // num_layers
        b = start_color[2] + i * (end_color[2] - start_color[2]) // num_layers
        color = (r, g, b)
        screen.colormode(255)
        gradient_turtle.color(color)
        
        # Draw a rectangle layer from top to bottom
        gradient_turtle.penup()
        gradient_turtle.goto(-800, 450 - (i * 45))
        gradient_turtle.pendown()
        gradient_turtle.begin_fill()
        for _ in range(2):
            gradient_turtle.forward(1600)
            gradient_turtle.right(90)
            gradient_turtle.forward(45)
            gradient_turtle.right(90)
        gradient_turtle.end_fill()
    
    screen.tracer(1)

def draw_stars():
    screen = Screen()
    star_turtle = Turtle()
    star_turtle.hideturtle()
    star_turtle.speed(0)
    star_turtle.color("white")
    screen.tracer(0)

    # Draw random stars at the top portion of the screen
    for _ in range(50):  # Increase or decrease the number of stars as desired
        x = random.randint(-800, 800)
        y = random.randint(150, 450)
        star_turtle.penup()
        star_turtle.goto(x, y)
        star_turtle.pendown()
        star_turtle.dot(random.randint(2, 4))  # Varying dot size for star effect

    screen.tracer(1)

# Set up the gradient background and stars before drawing the other elements
draw_gradient_background()
draw_stars()

# Call the function to add an 8-layer mountain range with varied shapes
draw_mountain_range()

# Call the function to add mountains
draw_mountain_range()

draw_grass()
forest = Forest(25)  # Number of trees in the forest
forest.create_forest()
forest.draw_forest()
swarm = Swarm(15)  # Number of bees in the swarm
swarm.create_swarm()
swarm.draw_swarm()

done()