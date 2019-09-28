import sys
import turtle
import time

# Criando a tela.
screen = turtle.Screen()
screen.title(" Little Breakout ")
screen.bgcolor("black")
screen.setup(720, 480)
screen.tracer(0)

# Desenhando a bola.
ball = turtle.Turtle("circle")
ball.speed(0)
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0.2
ball.dy = -0.2

# Desenhando raquete.
racket = turtle.Turtle("square")
racket.speed(0)
racket.turtlesize(1, 7)
racket.color("blue")
racket.penup()
racket.sety(-220)

# desenhando os blocos
x = -300
y = 220
block_colors = ["red", "orange", "yellow", "green", "blue"]
for i in block_colors:
    while x <= 320:
        block = turtle.Turtle("square")
        block.speed(0)
        block.color(i)
        block.turtlesize(1, 4)
        block.penup()
        block.goto(x, y)
        x += 85
    y -= 30
    x = -300

while True:
    screen.update()
