import turtle

# Criando a tela.
screen = turtle.Screen()
screen.title(" Little Breakout ")
screen.bgcolor("black")
screen.setup(720, 580)  # 720,480 antigo
screen.tracer(0)


def create_menu():
    options = ["Iniciar", "Sair"]
    for i in range(len(options)):
        message = turtle.Turtle()
        message.penup()
        message.hideturtle()
        message.sety(150 - 100*i)
        message.color("white")
        message.write(options[i], align='center',
                      font=('DS-Digital', 50, 'normal'))
        message.write(options[i], align='center',
                      font=('DS-Digital', 50, 'normal'))
        message.write(options[i], align='center',
                      font=('DS-Digital', 50, 'normal'))

    cursor = turtle.Turtle()
    cursor.penup()
    cursor.hideturtle()
    cursor.color("white")
    positions = [150, 50]
    cursor_index = [0]
    cursor.setx(-200)
    cursor.sety(positions[cursor_index[0]])
    cursor.write(">", align='center',
                 font=('DS-Digital', 50, 'normal'))

    def cursor_up():
        if(cursor_index[0] > 0):
            cursor_index[0] -= 1
            cursor.sety(positions[cursor_index[0]])
            cursor.clear()
            cursor.write(">", align='center',
                         font=('DS-Digital', 50, 'normal'))

    def cursor_down():
        if(cursor_index[0] < 1):
            cursor_index[0] += 1
            cursor.sety(positions[cursor_index[0]])
            cursor.clear()
            cursor.write(">", align='center',
                         font=('DS-Digital', 50, 'normal'))

    def select_option():
        print(options[cursor_index[0]])
    screen.listen()
    screen.onkeypress(cursor_up, "Up")
    screen.onkeypress(cursor_down, "Down")
    screen.onkeypress(select_option, "Return")


create_menu()

while True:
    screen.update()
