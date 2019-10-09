import random
import sys
import turtle
import time
import simpleaudio as sa
import threading
from menu import create_menu

# Variável de controle do laço principal
hasLives = True
# Quantidade de vidas
lives = 3
# Estado do jogo
state = "menu"
# Velocidade de inicio de X
vel_inicial = 1

selected_sound = None
bg_thread = None


screen = None           # Instância da tela
score = 0               # Pontuação do jogador
scoreboard = None       # Objeto do placar de pontuação
racket = None           # Objeto da raquete
ball = None             # Objeto da bola
blocks = []             # Matriz de objetos dos tijolos
destroyed_blocks = []   # Matriz de controle de vida dos tijolos
block_colors = ["red", "orange", "yellow", "green", "blue", "purple"]
lives_hud = []          # Objeto do placar de pontuação
option = []             # Opção selecionada no menu

SOUNDS_PATH = "sounds/"
beep = SOUNDS_PATH+'beep.wav'
peep = SOUNDS_PATH+'peep.wav'
plop = SOUNDS_PATH+'plop.wav'
game_over = SOUNDS_PATH+'game_over.wav'
victory = SOUNDS_PATH+'victory.wav'
sounds = ['song1.wav', 'song2.wav', 'song3.wav', 'song4.wav']
sounds = [SOUNDS_PATH+song for song in sounds]


# Criando a tela.
def create_screen():
    global screen
    screen = turtle.Screen()
    screen.clear()
    screen.title("Little Breakout ")
    screen.bgcolor("black")
    screen.setup(720, 580)  # 720,480 antigo
    screen.tracer(0)


# Alterar variáavel que mantém o estado do jogo
# playing - Jogo em execução (comandos permitidos)
# paused - Jogo pausado (possível apenas despausar)
# starting/gameover - Jogo iniciando/terminando (sem comandos disponíveis)
def set_state(new_state):
    global state
    state = new_state


# função para tocar som
def play(sound):
    wave_obj = sa.WaveObject.from_wave_file(sound)
    wave_obj.play()


def loop_play():
    global selected_sound
    if not selected_sound:
        selected_sound = random.choice(sounds)
    wave_obj = sa.WaveObject.from_wave_file(selected_sound)
    play_obj = wave_obj.play()
    while state == "playing":
        print(selected_sound)
        if not play_obj.is_playing():
            play_obj = wave_obj.play()
    play_obj.stop()


def play_background():
    global bg_thread
    if not bg_thread:
        bg_thread = threading.Thread(target=loop_play)
        bg_thread.setDaemon(True)
        bg_thread.start()


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


# display de pontuação
def update_score_display():
    scoreboard.clear()
    scoreboard.write("Score : {}".format(score), align="center",
                     font=("Press Start 2P", 18, "normal"))


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
    ball.goto(0, -235)
    screen.update()
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
    play_background()


# Pausar o jogo
def pause():
    if state == "playing":
        set_state("paused")
        bg_thread.join()
    elif state == "paused":
        set_state("playing")
        play_background()


# Controle para movar raquete com o mouse/touchpad
def onmove(self, racket):
    def moveracket(event):
        if(state == "playing"):
            if self.cv.canvasx(event.x) < -285:
                racket.setx(-285)
            elif self.cv.canvasx(event.x) > 285:
                racket.setx(285)
            else:
                racket.setx(self.cv.canvasx(event.x) / self.xscale)
    self.cv.bind('<Motion>', moveracket)


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
        ball.dy *= -1
        return True
    return False


# função que testa se a bola passou da raquete
def ball_pass():
    if (ball.ycor() < racket.ycor() - 20):
        return True
    return False


def draw_game():
    create_screen()

    # pontuação
    global score
    score = 0
    global scoreboard
    scoreboard = create_hud("square", "white")
    scoreboard.hideturtle()
    scoreboard.goto(280, 250)  # 280,200 antigo
    scoreboard.write("Score : {}".format(score), align="center",
                     font=("Press Start 2P", 18, "normal"))

    # Desenhando a bola.
    global ball
    ball = create_hud("circle", "white")
    ball.goto(0, -235)
    ball.dx = random.choice((-1, 1)) * vel_inicial
    ball.dy = 1.7

    # Desenhando raquete.
    global racket
    racket = create_hud("square", "blue")
    racket.turtlesize(1, 7)
    racket.sety(-260)

    # controles
    screen.listen()
    screen.onkeypress(racket_left, 'a')
    screen.onkeypress(racket_right, 'd')
    screen.onkeypress(racket_left, 'Left')
    screen.onkeypress(racket_right, 'Right')
    screen.onkeypress(pause, 'p')
    onmove(screen, racket)

    # desenhando os blocos
    global destroyed_blocks
    destroyed_blocks = []
    global blocks
    blocks = []
    x = -310
    y = 230  # antigo 180
    for i in range(len(block_colors)):
        line_of_blocks = []
        line_of_destroyed_blocks = [6-i] * 8
        destroyed_blocks.append(line_of_destroyed_blocks)
        for _ in range(8):
            block = create_hud("square", block_colors[i])
            block.turtlesize(1, 4)
            block.goto(x, y)
            block.color(block_colors[i])
            line_of_blocks.append(block)
            x += 88
        blocks.append(line_of_blocks)
        y -= 30
        x = -310
    block_colors.reverse()

    # criando uma lista de hud das vidinhas, botei uma tortuguinha
    global lives_hud
    lives_hud = []
    for i in range(0, 3):
        live_hud = create_hud("turtle", "red")
        live_hud.goto(-330+(30*i), 265)
        lives_hud.append(live_hud)
    screen.update()


i = 0
while hasLives:
    if state == "menu":
        option = []
        create_screen()
        create_menu(screen, option)
        state = "waiting"

    screen.update()
    if len(option) > 0:
        if option[0] == "Iniciar" and state == "waiting":
            draw_game()
            wait()
            set_state("playing")
        if option[0] == "Sair" and state == "waiting":
            sys.exit(0)

    if state == "starting":
        if (i == 0):
            wait()
            set_state("playing")
            i = 1

    if state == "playing":
        # movimentando a bola
        ball.sety(ball.ycor() + ball.dy)
        ball.setx(ball.xcor() + ball.dx)

        # Colisão com a parede superior
        if (ball.ycor() > 290):
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
        if (ball.ycor() < -240 and ball.ycor() > -245 and  # antigo -200, -205
            ball.xcor() < racket.xcor() + 74 and
                ball.xcor() > racket.xcor() - 74):
            ball.dy *= -1
            ball.dx = angle(racket.xcor(), ball.xcor())
            play(beep)

        # colisão do canto esquerdo da raquete
        if (ball.ycor() <= -240 and ball.ycor() > -270 and  # antigo -200, -230
            ball.xcor() <= racket.xcor() - 74 and
                ball.xcor() > racket.xcor() - 80):
            ball.dy *= -1
            if ball.dx > 0:
                ball.dx *= -1
            play(beep)

        # colisão do canto direito da raquete
        if (ball.ycor() <= -240 and ball.ycor() > -270 and  # antigo -200, -230
            ball.xcor() < racket.xcor() + 80 and
                ball.xcor() >= racket.xcor() + 74):
            ball.dy *= -1
            if ball.dx < 0:
                ball.dx *= -1
            play(beep)

        # Testa colisão quando a bola acima da metade da tela
        if ball.ycor() > 0:
            for i in range(6):
                for j in range(8):
                    if(destroyed_blocks[i][j] > 0 and
                       colide(ball, blocks[i][j])):
                        play(plop)
                        score += (6-i)
                        update_score_display()
                        destroyed_blocks[i][j] -= 1
                        blocks[i][j].color(
                            block_colors[destroyed_blocks[i][j]-1])
                        if destroyed_blocks[i][j] == 0:
                            blocks[i][j].hideturtle()

        soma = 0
        for i in range(6):
            for j in range(8):
                soma += destroyed_blocks[i][j]

        # Se todos os tijolos estiverem destruídos
        if soma == 0:
            message = create_hud("square", "white")
            message.hideturtle()
            play(victory)
            message.write("Victory", align="center",
                          font=("Press Start 2P", 40, "normal"))
            time.sleep(8)
            message.clear()
            set_state("menu")

        # testando se a bola passa da cory da raquete
        if (ball_pass()):
            lives -= 1
            lives_hud[lives].hideturtle()
            play(peep)
            set_state("starting")
            ball.dy *= -1
            if (lives > 0):
                i = 0
            else:
                set_state("gameover")
                message = create_hud("square", "white")
                message.hideturtle()
                play(game_over)
                message.write("Game Over", align="center",
                              font=("Press Start 2P", 40, "normal"))
                time.sleep(7)
                message.clear()
                set_state("menu")
