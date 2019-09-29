import random
import sys
import turtle
import time

# isso é só pra tentar deixar a criação de hud numa função só,
# se acharem merda podem apagar, mas já implementei na criação das parada tudo só lamento
def create_hud(shape,color):
    hud = turtle.Turtle()
    hud.speed(0)
    hud.shape(shape)
    hud.color(color)
    hud.penup()
    return hud

# Criando a tela.
screen = turtle.Screen()
screen.title(" Little Breakout ")
screen.bgcolor("black")
screen.setup(720, 480)
screen.tracer(0)

# pontuação
score = 0

# display de pontuação 
scoreboard = create_hud("square","white")
scoreboard.hideturtle()
scoreboard.goto(280, 200)
scoreboard.write("Score : {}".format(score),align="center", font=("Press Start 2P", 18, "normal"))

# Desenhando a bola.
ball = create_hud("circle","white")
ball.goto(0, 0)
ball.dx = random.choice((-1, 1)) * 1
ball.dy = random.choice((-1, 1)) * 1.7

# Desenhando raquete.
racket = create_hud("square","blue")
racket.turtlesize(1, 7)
racket.sety(-220)

# Movimentando a raquete esquerda
# Esquerda
def racket_left():
    x = racket.xcor()
    if x > -285:
        x -= 30
    else:
        x = -285
    racket.setx(x)

# Direita
def racket_right():
    x = racket.xcor()
    if x < 280:
        x += 30
    else:
        x = 280
    racket.setx(x)

# angulação da bola ao rebater na raquete
def angle():
    x1 = racket.xcor()
    x2 = ball.xcor()
    signal = 1 if ball.dx >= 0 else -1
    dist_of_points = ((x2-x1)**2)**(0.5)
    racket_angle = (dist_of_points//17.5)+1
    if(dist_of_points >=0 and dist_of_points < 1):
        return 0
    else:
        return signal*(1+(racket_angle/10))

screen.listen()
screen.onkeypress(racket_left, 'Left')
screen.onkeypress(racket_right, 'Right')

# desenhando os blocos
x = -300
y = 180
block_colors = ["red", "orange", "yellow", "green", "blue"]
for i in block_colors:
    while x <= 320:
        block = create_hud("square",i) 
        block.turtlesize(1, 4)
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

# aqui to setando a quantidade de vidas e criando a variavel que é testada no laço principal do jogo
hasLives = True
lives = 3

# criando uma lista de hud das vidinhas, botei uma tortuguinha pq é mt fofinho
lives_hud = []
for i in range(0,3):
    live_hud = create_hud("turtle","red")
    live_hud.goto(-330+(30*i),215) # isso se chama gambiarra, e sim vou mudar a posição das vidas pra cima, mas só quando arrumarem a parte superior da tela e tal
    lives_hud.append(live_hud)

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
    if(ball.ycor() < -200 and ball.ycor() > -205 and ball.xcor() < racket.xcor() + 70 and
            ball.xcor() > racket.xcor() - 70):
        ball.dy *= -1
        ball.dx = angle()

    # testanto se a bola passa da cory da raquete
    if(ball_pass()):
        lives -= 1
        lives_hud[lives].hideturtle()
        if(lives == 0):
            hasLives = False
        ball.goto(0,0)
