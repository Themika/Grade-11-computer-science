from turtle import *
import time
import random
from turtle import Screen, Turtle

"""
    Deleted the Desmos stuff and have nothing saved
    This program shows a night sky and a mountain range 
    with a forest of trees and a swarm of bees flying around.
"""
class Bee:
    def __init__(self):
        self.t = Turtle()
        self.t.speed(10000)
        self.side = 25
        self.bee_w, self.bee_l = 7 * self.side, 10 * self.side
        self.setup()

    def setup(self):
        # Set the initial position and heading of the turtle
        self.t.pensize(2)
        self.t.up()
        self.t.goto(0, -150)
        self.t.setheading(25) 
        self.t.down()

    def draw_body(self):
        # Draw the body of the bee
        self.t.color('#FFEE5F')
        self.t.begin_fill()
        # Draw the body of the bee
        for i in range(2):
            # Draw the body of the bee
            self.t.forward(self.bee_l)
            self.t.left(60)
            # Draw the head of the bee
            self.t.forward(self.bee_w)
            self.t.left(60)
            # Draw the body of the bee
            self.t.forward(self.bee_w)
            self.t.left(60)
        self.t.end_fill()

    def draw_pollen(self):
        # Draw the pollen on the bee's legs
        self.t.color('#FFD75E')
        self.t.begin_fill()
        # Draw the pollen on the bee's legs
        for i in range(2):
            self.t.forward(self.bee_l)
            self.t.left(60)
            self.t.forward(self.side)
            self.t.left(120)
        self.t.end_fill()
        # Draw the pollen on the bee's legs
        self.t.left(120)
        self.t.begin_fill()
        # Draw the pollen on the bee's legs
        for i in range(2):
            self.t.forward(self.bee_w)
            self.t.right(60)
            self.t.forward(self.side)
            self.t.right(120)
        self.t.end_fill()
        # Draw the pollen on the bee's legs
    
    def draw_stripes(self, thick):
        # Draw the stripes on the bee's body
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
        # Draw the legs of the bee
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
        # Colored section of left eye
        for i in range(2):
            # Colored section of left eye
            for value in [120, 60]:
                # Colored section of left eye
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
        # Colored part of right eye
        for i in range(3):
            # Colored part of right eye
            self.t.right(60)
            self.t.forward(self.side)
        self.t.end_fill()

        # Colored part of right eye
        self.t.left(60)
        self.t.color('#30C8BE')
        self.t.begin_fill()
        # Colored part of right eye
        for i in range(2):
            for value in [60, 120]:
                self.t.forward(self.side)
                self.t.left(value)
        self.t.end_fill()

    def draw_outline(self):
        # Draw the outline of the bee
        self.t.right(120)
        self.t.color('black')
        self.t.forward(self.side)
        self.t.right(60)
        self.t.forward(3 * self.side)
        # Draw the outline of the bee
        for i in range(2):
            # Draw the outline of the bee
            self.t.right(60)
            self.t.forward(10 * self.side)
            # Draw the outline of the bee
            self.t.right(60)
            self.t.forward(7 * self.side)
            # Draw the outline of the bee
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

    def draw(self):
        # Draw the bee
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
        self.t.hideturtle()
class Swarm:
    # Create a swarm of bees
    def __init__(self, num_bees):
        self.num_bees = num_bees
        self.bees = []

    def create_swarm(self):
        # Create a swarm of bees
        positions = []
        # Create a swarm of bees
        for _ in range(self.num_bees):
            # Create a swarm of bees
            bee = Bee()
            # Create a swarm of bees
            bee.side = random.randint(10,15)  # Random size for each bee
            bee.bee_w, bee.bee_l = 7 * bee.side, 10 * bee.side
            bee.t.penup()
            # Create a swarm of bees
            while True:
                # Create a swarm of bees
                x, y = random.randint(-650, 650), random.randint(-400, 400)
                # Check if the bees are too close to each other
                if all(abs(x - px) > 20 and abs(y - py) > 20 for px, py in positions):
                    positions.append((x, y))
                    break
            
            bee.t.goto(x, y)
            bee.t.pendown()
            # Create a swarm of bees
            self.bees.append(bee)

    def draw_swarm(self):
        # Draw the swarm of bees
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
    # Draw the tree
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
        # Create a forest of trees
        for _ in range(self.num_trees):
            # Create a forest of trees
            x = random.randint(-650, 650)
            y = random.randint(-410, -400)
            side = random.randint(10, 20)  # Random size for each tree
            tree = Tree(x, y, side)
            self.trees.append(tree)

    def draw_forest(self):
        # Draw the forest of trees
        for tree in self.trees:
            tree.draw()

class Background():
    def __init__(self):
        self.t = Turtle()
        self.t.speed(10000)
        self.t.hideturtle()
    def draw_gradient_background(self):
        # Draw a gradient background from light blue to dark blue
        screen = Screen()
        screen.setup(width=1600, height=800)
        
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
    def draw_stars(self):
        # Draw stars in the sky
        screen = Screen()
        star_turtle = Turtle()
        star_turtle.hideturtle()
        star_turtle.speed(0)
        star_turtle.color("white")
        screen.tracer(0)
        # Draw stars at random positions in the sky
        for _ in range(400):  
            x = random.randint(-900, 900)
            y = random.randint(150, 450)
            star_turtle.penup()
            star_turtle.goto(x, y)
            star_turtle.pendown()
            star_turtle.dot(random.randint(2, 4))  

        screen.tracer(1)
    def draw_constellations(self):
        # Draw constellations in the sky
        screen = Screen()
        constellation_turtle = Turtle()
        constellation_turtle.hideturtle()
        constellation_turtle.speed(0)
        constellation_turtle.color("white")
        screen.tracer(1)
        # Define the constellations with relative positions
        ursa_major = [
            (-172, 21), (-94, 51.3), (-30, 23), (46.4, -6), (77, -54), (172, -45.6), (165, 39), (48, -6.6), 
        ]
        ursa_minor = [
            (-372, 248), (-405, 204), (-415, 134), (-412, 58), (-449, 35), (-395, -30), (-359, 5), (-410, 56),
        ]
        hercules = [
            (-59, 438.7), (-89, 360), (-23, 351), (31, 371), (46, 410), (62, 453), (32, 371.3), (39.1, 301.2), (39.1, 301.2), (67.6,199.3), (-25,121), (68,199),(39,300),(3,288),(-23.3,350.5),(3.4,287.9),(-23.2,225),(-105,277),(-120.3,275.2)
        ]
        cyginius = [
            (231,137.5),(311,131),(381,162.4),(444,228.5),(523.6,275.4),(550.4,351.5),(570,367),(550.4,353.5),(523.2,275.6),(444.3,228.6),(444,228.5),(412.6,286.5),(444,228.5),(497.2,159.6),(558.2,79)
        ]
        # Draw the constellations
        for constellation in [ursa_major, ursa_minor, hercules,cyginius]:
            constellation_turtle.penup()
            for i, (x, y) in enumerate(constellation):
                constellation_turtle.goto(x, y)
                constellation_turtle.pendown()
                constellation_turtle.dot(5)
                if i > 0:
                    constellation_turtle.penup()
                    constellation_turtle.goto(constellation[i-1])
                    constellation_turtle.pendown()
                    constellation_turtle.goto(x, y)
    def draw_mountain_range(self):
        # Draw the mountain range in the background
        mountain_turtle = Turtle()
        mountain_turtle.speed(0)
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
                # Draw the mountain
                mountain_turtle.penup()
                mountain_turtle.goto(x_start, y_start + y_offset)
                mountain_turtle.pendown()
                # Draw the mountain
                mountain_turtle.color(color)
                mountain_turtle.begin_fill()
                mountain_turtle.goto(x_peak_variation, y_peak_variation + y_offset)  # Varying peak of the mountain
                mountain_turtle.goto(x_end_variation, y_start + y_offset)  # Varying base of the mountain
                mountain_turtle.end_fill()

        mountain_turtle.hideturtle()
    def draw_grass(self):
        # Draw the grass at the bottom of the screen
        grass_turtle = Turtle()
        grass_turtle.speed(10000)
        grass_turtle.color('green')
        grass_turtle.penup()
        grass_turtle.goto(-800, -400)
        grass_turtle.pendown()
        grass_turtle.begin_fill()
        # Draw the grass at the bottom of the screen
        for _ in range(2):
            # Draw the grass at the bottom of the screen
            grass_turtle.forward(1600)
            grass_turtle.right(90)
            grass_turtle.forward(75)
            grass_turtle.right(90)
        grass_turtle.end_fill()
        grass_turtle.hideturtle()
    def draw(self):
        self.draw_gradient_background()
        self.draw_stars()
        self.draw_constellations()
        self.draw_mountain_range()
        self.draw_grass()

background = Background()
background.draw()
forest = Forest(25)  
forest.create_forest()
forest.draw_forest()
swarm = Swarm(15)  
swarm.create_swarm()
swarm.draw_swarm()

done()