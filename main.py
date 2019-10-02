import random
import sys
import turtle
import time
import os


# Variável de controle do laço principal
hasLives = True
# Quantidade de vidas
lives = 3
# Estado do jogo
state = "starting"
# Velocidade de inicio de X
vel_inicial = 1

beep = 'beep.wav'
peep = 'peep.wav'
plop = 'plop.wav'
game_over = 'game_over.wav'


# Alterar variáavel que mantém o estado do jogo
# playing - Jogo em execução (comandos permitidos)
# paused - Jogo pausado (possível apenas despausar)
# starting/gameover - Jogo iniciando/terminando (sem comandos disponíveis)
def set_state(new_state):
    global state
    state = new_state


# função para tocar som
def play(sound):
    os.system('aplay '+sound+'&')


# isso é só pra tentar deixar a criação de hud numa função só,
# se acharem merda podem apagar
# Mas já implementei na criação das parada tudo só lamento
def create_hud(shape, color):
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
screen.setup(720, 580) # 720,480 antigo
screen.tracer(0)

# pontuação
score = 0
scoreboard = create_hud("square", "white")
scoreboard.hideturtle()
scoreboard.goto(280, 250) # 280,200 antigo
scoreboard.write("Score : {}".format(score), align="center",
                 font=("Press Start 2P", 18, "normal"))


# display de pontuação
def update_score_display():
    scoreboard.clear()
    scoreboard.write("Score : {}".format(score), align="center",
                     font=("Press Start 2P", 18, "normal"))


# Desenhando a bola.
ball = create_hud("circle", "white")
ball.goto(0, 50)
ball.dx = random.choice((-1, 1)) * vel_inicial
ball.dy = -1.7

# Desenhando raquete.
racket = create_hud("square", "blue")
racket.turtlesize(1, 7)
racket.sety(-260)


blocks = []
destroyed_blocks = []


# Movimentando a raquete esquerda
# Esquerda
def racket_left():
    if state == "playing":
        x = racket.xcor()
        if x > -285:
            x -= 30
        else:
            x = -285
        racket.setx(x)


# Direita
def racket_right():
    if state == "playing":
        x = racket.xcor()
        if x < 280:
            x += 30
        else:
            x = 280
        racket.setx(x)


# Função para angulo
def angle(x1, x2, div=17.5):
    signal = 1 if ball.dx >= 0 else -1
    dist_of_points = ((x2-x1)**2)**(0.5)
    racket_angle = (dist_of_points//div)+1
    if(dist_of_points >= 0 and dist_of_points < 1):
        return 0
    else:
        return signal*(vel_inicial+(racket_angle/10))


# tempo entre as derrotas
def wait():
    ball.goto(0, 50)
    timer = create_hud("square", "white")
    timer.hideturtle()
    timer.goto(0, -30)
    i = 3
    while i > 0:
        timer.write("{}".format(i), align="center",
                    font=("Press Start 2P", 30, "normal"))
        timer.clear()
        time.sleep(1)
        i -= 1
    set_state("playing")
    


# Pausar o jogo
def pause():
    if state == "playing":
        set_state("paused")
    elif state == "paused":
        set_state("playing")


# controles
screen.listen()
screen.onkeypress(racket_left, 'a')
screen.onkeypress(racket_right, 'd')
screen.onkeypress(racket_left, 'Left')
screen.onkeypress(racket_right, 'Right')
screen.onkeypress(pause, 'p')


# diz se houve colisão entre dois objetos
def colide(a, b):
    widthA = a.turtlesize()[1] * 20
    widthB = b.turtlesize()[1] * 20
    heightA = a.turtlesize()[0] * 20
    heightB = b.turtlesize()[0] * 20

    xA = a.xcor() - widthA/2
    yA = a.ycor() + heightA/2
    xB = b.xcor() - widthB/2
    yB = b.ycor() + heightB/2

    if (a.dx > 0):
        if (xA + widthA >= xB and xA <= xB and
            ((yA + heightA >= yB and yA <= yB) or
             (yA + heightA >= yB + heightB and yA <= yB + heightB))):
            ball.dx = angle(xA, xB, 10)
            return True

    elif (a.dx < 0):
        if (xA <= xB + widthB and xA + widthA >= xB + widthB and
            ((yA + heightA >= yB and yA <= yB) or
             (yA + heightA >= yB + heightB and yA <= yB + heightB))):
            ball.dx = angle(xA, xB, 10)
            return True

    if(xA + widthA >= xB and xA <= xB + widthB and
       yA + heightA >= yB and yA <= yB + heightB):
        ball.dx = angle(xA, xB, 10)
        return True
    return False


# desenhando os blocos
x = -300
y = 230 # antigo 180
block_colors = ["red", "orange", "yellow", "green", "blue"]
for i in range(len(block_colors)):
    line_of_blocks = []
    line_of_destroyed_blocks = [False] * 8
    destroyed_blocks.append(line_of_destroyed_blocks)
    for j in range(8):
        block = create_hud("square", block_colors[i])
        block.turtlesize(1, 4)
        block.goto(x, y)
        block.color = block_colors[i]
        line_of_blocks.append(block)
        x += 85
    y -= 30
    blocks.append(line_of_blocks)
    x = -300


# função que testa se a bola passou da raquete
def ball_pass():
    if (ball.ycor() < racket.ycor() - 20):
        return True
    return False


# criando uma lista de hud das vidinhas, botei uma tortuguinha pq é mt fofinho
lives_hud = []
for i in range(0, 3):
    live_hud = create_hud("turtle", "red")
    live_hud.goto(-330+(30*i), 265)
    lives_hud.append(live_hud)

i = 0
while hasLives:
    screen.update()

    if (i == 0):
        wait()
        i = 1

    if state == "playing":

        # movimentando a bola
        ball.sety(ball.ycor() + ball.dy)
        ball.setx(ball.xcor() + ball.dx)

        # Colisão com a parede superior
        if (ball.ycor() > 315):
            ball.dy *= -1
            play(plop)

        # Colisão com a parede direita
        if (ball.xcor() > 350):
            ball.dx *= -1
            play(plop)

        # Colisão com a parede esquerda
        elif(ball.xcor() < -350):
            ball.dx *= -1
            play(plop)

        # Colisão com a raquete
        if (ball.ycor() < -250 and ball.ycor() > -255 and # antigo -200, -205
            ball.xcor() < racket.xcor() + 74 and
                ball.xcor() > racket.xcor() - 74):
            ball.dy *= -1
            ball.dx = angle(racket.xcor(), ball.xcor())
            play(beep)

        # colisão do canto esquerdo da raquete
        if (ball.ycor() <= -250 and ball.ycor() > -280 and # antigo -200, -230
            ball.xcor() <= racket.xcor() - 74 and
                ball.xcor() > racket.xcor() - 76):
            ball.dy *= -1
            ball.dx *= -1
            play(beep)

        # colisão do canto direito da raquete
        if (ball.ycor() <= -250 and ball.ycor() > -280 and # antigo -200, -230
            ball.xcor() < racket.xcor() + 77 and
                ball.xcor() >= racket.xcor() + 74):
            ball.dy *= -1
            ball.dx *= -1
            play(beep)

        # Testa colisão quando a bola acima da metade da tela
        if ball.ycor() > 0:
            for (i, line) in enumerate(blocks):
                for (j, block) in enumerate(line):
                    if not destroyed_blocks[i][j] and colide(ball, block):
                        destroyed_blocks[i][j] = True
                        block.hideturtle()
                        score += 1
                        update_score_display()
                        ball.dy *= -1

                        # Se todos os tijolos estiverem destruídos
                        if all([all(line) for line in destroyed_blocks]):
                            message = create_hud("square", "white")
                            message.hideturtle()
                            play(game_over)
                            message.write("Game Win", align="center",
                                          font=(
                                              "Press Start 2P",
                                              40,
                                              "normal")
                                          )
                            time.sleep(3)

        # testando se a bola passa da cory da raquete
        if (ball_pass()):
            lives -= 1
            lives_hud[lives].hideturtle()
            play(peep)
            if (lives == 0):
                set_state("gameover")
                hasLives = False
                message = create_hud("square", "white")
                message.hideturtle()
                play(game_over)
                message.write("Game Over", align="center",
                              font=("Press Start 2P", 40, "normal"))
                time.sleep(3)
            ball.goto(0, 50)
            racket.setx(0)
            if (lives > 0):
                i = 0
