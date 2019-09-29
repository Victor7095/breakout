import random
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
ball.dx = random.choice((-1, 1)) * 1
ball.dy = random.choice((-1, 1)) * 1.7

# Desenhando raquete.
racket = turtle.Turtle("square")
racket.speed(0)
racket.turtlesize(1, 7)
racket.color("blue")
racket.penup()
racket.sety(-220)

# Movimentando a raquete esquerda
# Esquerda
def racket_left():
    x = racket.xcor()
    if x > -290:
        x -= 20
    else:
        x = -290
    racket.setx(x)

# Direita
def racket_right():
    x = racket.xcor()
    if x < 290:
        x += 20
    else:
        x = 290
    racket.setx(x)

screen.listen()
screen.onkeypress(racket_left, 'a')
screen.onkeypress(racket_right, 'd')

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

# função que testa se a bola passou da raquete
def ball_pass():
    global ball
    global racket
    if(ball.ycor() < racket.ycor()):
        return True
    return False

# isso é só pra tentar deixar a criação de hud numa função só, se acharem merda podem apagar
def create_hud(shape,color):
    hud = turtle.Turtle()
    hud.speed(0)
    hud.shape(shape)
    hud.color(color)
    hud.penup()
    return hud

# acho que o nome da variável fala por si só né 
hasLives = True
lives = 3

while hasLives:
    screen.update()

    # movimentando a bola
    ball.sety(ball.ycor() + ball.dy)
    ball.setx(ball.xcor() + ball.dx)

    # Colisão com a parede superior
    if(ball.ycor() > 230):
        ball.dy *= -1

    # Colisão com a parede direita
    if(ball.xcor() > 350):
        ball.dx *= -1

    # Colisão com a parede esquerda
    elif(ball.xcor() < -350):
        ball.dx *= -1

    # Colisão com a raquete
    if(ball.ycor() < -200 and ball.xcor() < racket.xcor() + 70 and
            ball.xcor() > racket.xcor() - 70):
        ball.dy *= -1

    # testanto se a bola passa da cory da raquete
    if(ball_pass()):
        lives -= 1
        if(lives < 1):
            hasLives = False
        ball.goto(0,0)