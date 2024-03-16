import turtle
import random

# Screen
screen = turtle.Screen()
screen.screensize(500, 500)
screen.title("My Turtle Screen")
screen.bgpic("ocean.gif")

turtle.register_shape("Untitled-2.gif")
turtle.register_shape("Turtle-resized.gif")
turtle.register_shape("turtlefood.gif")
turtle.register_shape("straw.gif")

# Player Object
player = turtle.Turtle()
player.penup()
player.shape("Turtle-resized.gif")


# Home Base Object

home_base = turtle.Turtle()
home_base.penup()
home_base.color('red')
home_base.shape("Untitled-2.gif")
home_base.goto(-300, -300)

# Score
score = 0
score_display = turtle.Turtle()
score_display.penup()
score_display.color('white')
score_display.goto(screen.window_width() / 2 - 50, screen.window_height() / 2 - 50)
score_display.hideturtle()

# Stamina
stamina = 100
stamina_display = turtle.Turtle()
stamina_display.penup()
stamina_display.color('green')
stamina_display.goto(screen.window_width() / 2 - 50, screen.window_height() / 2 - 100)
stamina_display.hideturtle()

# Objectives
objectives = []

def create_objective():
    objective = turtle.Turtle()
    objective.penup()
    objective.hideturtle()
    objective.color('blue')
    objective.shape("turtlefood.gif")
    x = random.randint(-screen.window_width() / 2, screen.window_width() / 2)
    y = random.randint(-screen.window_height() / 2, screen.window_height() / 2)
    objective.goto(x, y)
    objective.showturtle()
    objectives.append(objective)

def collision(player, objective):
    distance = player.distance(objective)
    return distance < 50

# Trash
trash_list = []

def create_trash():
    trash = turtle.Turtle()
    trash.penup()
    trash.hideturtle()
    trash.color('blue')
    trash.shape("straw.gif")
    x = random.randint(-screen.window_width() / 2, screen.window_width() / 2)
    y = random.randint(-screen.window_height() / 2, screen.window_height() / 2)
    trash.goto(x, y)
    trash.showturtle()
    trash_list.append(trash)
    screen.ontimer(create_trash, 10000)

# Player Movement
def decrease_stamina():
    global stamina
    decrease = 1
    if score > 5:
        decrease = 2
    if score > 10:
        decrease = 4
    if stamina > 0:
        stamina -= decrease
        stamina_display.clear()
        stamina_display.write(f"Stamina: {stamina}", align="right", font=("Arial", 16, "normal"))
    else:
        # Game over condition
        screen.clear()
        screen.bgcolor("black")
        game_over_text = turtle.Turtle()
        game_over_text.penup()
        game_over_text.hideturtle()
        game_over_text.color("white")
        game_over_text.write("Game Over", align="center", font=("Arial", 30, "normal"))
        game_over_text.goto(0,-100)
        game_over_text.write("ggs lil cuh", align="center", font=("Arial", 30, "normal"))
        game_end()
        return
    screen.ontimer(decrease_stamina, 1000)

speed = 10
def player_forward():
    global score, stamina
    player.forward(speed)
    for objective in objectives:
        if collision(player, objective):
            for obj in objectives:
                obj.hideturtle()  
            objectives.clear()  
            create_objective()
            score += 1
            score_display.clear()
            score_display.write(f"Score: {score}", align="right", font=("Arial", 16, "normal"))

    for trash in trash_list:
        if collision(player, trash):
            trash.hideturtle()  
            trash_list.remove(trash)  
            stamina -= 10
            stamina_display.clear()  
            stamina_display.write(f"Stamina: {stamina}", align="right", font=("Arial", 16, "normal"))  

    if collision(player, home_base):
        stamina = 100  
        stamina_display.clear()  
        stamina_display.write(f"Stamina: {stamina}", align="right", font=("Arial", 16, "normal"))
    screen.ontimer(player_forward, 100)  

def save_score():
    with open("score.txt", "w") as file:
        file.write(str(score))

def game_end():
    save_score()

    player_name = turtle.textinput("Game Over", "Enter your name:")

    if player_name:
        with open("scores.txt", "a") as file:
            file.write(f"Player: {player_name}, Score: {score}\n")

def player_left():
    player.left(90)

def player_right():
    player.right(90)

screen.listen()
screen.onkey(player_left, 'a')
screen.onkey(player_right, 'd')

create_objective()
create_trash()
player_forward()
decrease_stamina()
screen.mainloop()