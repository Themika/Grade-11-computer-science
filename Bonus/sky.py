import turtle
import random

# Setup the screen
turtle.setup(width=800, height=600)
turtle.bgcolor("dark blue")
turtle.title("Night Sky Background")

# Initialize the turtle
pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

# Function to draw a pixelated block
def draw_block(x, y, size, color):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    for _ in range(4):
        pen.forward(size)
        pen.right(90)
    pen.end_fill()

# Draw pixelated clouds
cloud_color = "black"
cloud_positions = [
    (-200, 100), (-160, 110), (-120, 120), (-100, 100),
    (-60, 110), (0, 120), (40, 100), (80, 110),
    (160, 130), (200, 120), (240, 100)
]
for x, y in cloud_positions:
    draw_block(x, y, 40, cloud_color)

# Draw stars
pen.color("white")
star_positions = [(random.randint(-390, 390), random.randint(-290, 290)) for _ in range(30)]
for x, y in star_positions:
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.dot(3)

# Draw pixelated moon
moon_color = "light gray"
moon_positions = [(150, 200), (170, 200), (150, 180), (170, 180), (190, 180)]
for x, y in moon_positions:
    draw_block(x, y, 20, moon_color)

# Hide the turtle and display the result
turtle.done()
