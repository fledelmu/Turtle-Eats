import turtle
import random
import sys

# Screen
screen = turtle.Screen()
screen.screensize(500, 500)
screen.title("Turtle Eats")
screen.bgpic("ocean.gif")

# Main Menu
menu_text = turtle.Turtle()
menu_text.penup()
menu_text.hideturtle()
menu_text.color('white')
menu_text.goto(0, 100)
menu_text.write("Turtle Eats", align="center", font=("Arial", 30, "normal"))
menu_text.goto(0,0)
menu_text.write("Press 'p' to play", align="center", font=("Arial", 24, "normal"))
menu_text.goto(0,-100)
menu_text.write("Press 'v' to view scoreboard", align="center", font=("Arial", 24, "normal"))
menu_text.goto(0,-200)
menu_text.write("Press 'i' for instructions", align="center", font=("Arial", 24, "normal"))
menu_text.goto(0,-300)
menu_text.write("Press 'l' to quit", align="center", font=("Arial", 24, "normal"))

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

turtle.register_shape("Untitled-2.gif")
turtle.register_shape("Turtle-resized.gif")
turtle.register_shape("turtlefood.gif")
turtle.register_shape("straw.gif")

# Player Object
player = turtle.Turtle()
player.penup()
player.shape("Turtle-resized.gif")
player.hideturtle()


# Home Base Object
home_base = turtle.Turtle()
home_base.penup()
home_base.shape("Untitled-2.gif")
home_base.goto(-300, -300)
home_base.hideturtle()

gameover = False

# Objectives
objectives = []

def create_objective():
    if not gameover:
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
    if not gameover:
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
    global stamina, gameover
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
        gameover = True
        screen.clear()
        screen.bgcolor("black")
        game_over_text = turtle.Turtle()
        game_over_text.penup()
        game_over_text.hideturtle()
        game_over_text.color("white")
        game_over_text.write("Game Over", align="center", font=("Arial", 30, "normal"))
        game_over_text.goto(0,-100)
        game_over_text.write("GG", align="center", font=("Arial", 30, "normal"))
        game_end()
        return
    screen.ontimer(decrease_stamina, 1000)

speed = 20
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

def game_end():
    player_name = turtle.textinput("Game Over", "Enter your name:")

    if player_name:
        with open("scores.txt", "a") as file:
            file.write(f"Player: {player_name}, Score: {score}\n")

def player_left():
    player.left(90)

def player_right():
    player.right(90)


def read_scores():
    try:
        with open("scores.txt", "r") as file:
            scores = file.readlines()
            score_message = "Scores:\n"
            for score in scores:
                score_message += score
            return score_message
    except FileNotFoundError:
        return "No scores found."

def show_scores():
    global score_display
    leaderboard = turtle.Turtle()
    leaderboard.penup()
    leaderboard.color('white')
    leaderboard.hideturtle()
    leaderboard.goto(0, 200)
    leaderboard.write(read_scores(), align="center", font=("Arial", 24, "normal"))
    leaderboard.goto(0, -200)
    leaderboard.write("Press 'p' to play", align="center", font=("Arial", 24, "normal"))

def instructions():
    global instruction
    instruction = turtle.Turtle()
    menu_text.clear()
    instruction.penup()
    instruction.color('white')
    instruction.hideturtle()
    instruction.goto(0, 100)
    instruction.write("Controls:\nLeft:\t\t'a'\nRight:\t\t'd'", align="center", font=("Arial", 24, "bold"))
    instruction.goto(0,0)
    instruction.write("How to play game:", align="center", font=("Arial", 24, "normal"))
    instruction.goto(0,-50)
    instruction.write("1. Collect food items to score points.", align="center", font=("Arial", 20, "normal"))
    instruction.goto(0,-100)
    instruction.write("2. Your stamina constantly, depletes go back to your cave to replenish it.", align="center", font=("Arial", 20, "normal"))
    instruction.goto(0,-150)
    instruction.write("3. Avoid the straws.", align="center", font=("Arial", 20, "normal"))
    instruction.goto(0,-300)
    instruction.write("Press 'p' to play", align="center", font=("Arial", 20, "normal"))

def view_scoreboard():
    menu_text.clear()
    show_scores()
    
def start_game():
    try:
        menu_text.clear()
        score_display.clear()
        instruction.clear()
        player.showturtle()
        home_base.showturtle()
        create_objective()
        create_trash()
        player_forward()
        decrease_stamina()
    except NameError:
        menu_text.clear()
        score_display.clear()
        player.showturtle()
        home_base.showturtle()
        create_objective()
        create_trash()
        player_forward()
        decrease_stamina()
    

def close_game():
    screen.bye()
    sys.exit()

screen.listen()
screen.onkey(player_left, 'a')
screen.onkey(player_right, 'd')
screen.onkey(start_game, 'p')
screen.onkey(instructions, 'i')
screen.onkey(view_scoreboard, 'v')
screen.onkey(close_game, 'l')

screen.mainloop()
