#Space Invaders
#Python, just for fun
import turtle
import os
import math
import random

#Set up screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

#Register the shapes
turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")


#Draw border
border_pen = turtle.Turtle()
border_pen.speed(0) #speed
border_pen.color("White")
border_pen.penup() #draws a pen on the screen pointing upwards
border_pen.setposition(-300, -300) #pen position in pixels
border_pen.pensize(3)
border_pen.pendown()
for side in range(4): #draws a square and doesn't go away because of a for loop
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

#Set the score to 0
score = 0

#Draw score
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" %score
score_pen.write(scorestring, False, align = "left", font = ("Arial", 14, "normal"))
score_pen.hideturtle()

#Create the player Turtle
player = turtle.Turtle() #creating turtle object
player.color("blue")
player.shape("player.gif")
player.penup() #positioning of the pen
player.speed(0) #speed of the game
player.setposition(0, -250) #towards the bottom of the border
player.setheading(90)


#playerspeed = 15 #speed of the player, can be tweaked for optimization

#Choose number of enemies
number_of_enemies = 5
#Create an empty list of enemies
enemies = [] #lists denoted by []

#Add enemies to the list
for i in range(number_of_enemies):
    #Create the enemy, add them to the enemies list
    enemies.append(turtle.Turtle())

for enemy in enemies: #for each of the enemy in enemies
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup() #won't draw anything
    enemy.speed(0) #speed of game
    x = random.randint(-200, 200)
    y = random.randint(100, 250)
    enemy.setposition(x, y)

enemyspeed = 2 #speed of enemy is slower than player

#Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90) #pointing up
bullet.shapesize(0.5, 0.5) #size of bullet
bullet.hideturtle() #will be hidden

bulletspeed = 20

#global N
N = 10

#Define bullet state
#ready - ready to fire
#fire - bullet is firing
bulletstate = "ready"

#Move the player left and right
def move_left(): #creates a function
    isLeft = True #xcoordinate starts at 0
    friction = 0
    global N
    N = 10
    if isLeft == True:
        if N > 0:
            friction += .01
        else:
            friction = 0
    x = player.xcor()
    x -= N - friction #x is now subtracting by the friction
    print(x)
    if x < -280: #sets boundaries in order for player to stop at the -280 mark
        x = - 280
    player.setx(x) #set current player x to the new x
    N-=1

def move_right(): #creates a function to move right
    isRight = True
    friction = 0
    global N
    N = 10
    if isRight == True:
        #N = 10
        if N > 0:
            friction -= .01
        else:
            friction = 0
    x = player.xcor()
    x += N + friction
	#friction += 1
    print(x)
    if x > 280: #sets boundaries in order for player to stop at the 280 mark
        x = + 280
    player.setx(x)
    N -= 1

def fire_bullet():
    #Declare bulletstate as a global/local variable(defined in the function, like a Private in Java) if it needs changed
    global bulletstate #changes bulletstate, making it a local/private variable
    if bulletstate == "ready":
        #changes bulletstate to fire
        bulletstate = "fire"
        #Move the bullet to just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setposition(x, y)
        bullet.showturtle()

def isCollision(t1, t2): #returning true or false
#pythagorean theorem
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False

#Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left") #when push left arrow key, calls the function move_left
turtle.onkey(move_right, "Right") #moves right
turtle.onkey(fire_bullet, "space")

#Main game loop
while True: #loops forever until we break out of it

    for enemy in enemies:
    #Move enemy
        x = enemy.xcor() #get current position of enemy
        x += enemyspeed #increment the enemy's speed
        enemy.setx(x) #moves from current enemy xpos to new enemy xpos

        #Move the enemt back and down
        if enemy.xcor() > 280:
            y = enemy.ycor()
            #Every time enemy hits border, drops down by 40 pixels. Getting closer to the player.
            y -= 40
            #in math, it would be 2 * -1 every time until it reaches 280 or -280 pixels
            enemyspeed *= -1
            enemy.sety(y) #sets enemy y position

        if enemy.xcor() < -280:
            y = enemy.ycor()
            y -= 40
            enemyspeed *= -1
            enemy.sety(y)

        if isCollision(bullet, enemy):
            #Reset bullet
            bullet.hideturtle()
            #to fire again
            bulletstate = "ready"
            #position of bullet after fired
            bullet.setposition(0, -400)
            #Reset the enemy
            x = random.randint(-200, 200)
            y = random.randint(100, 250)
            enemy.setposition(x, y)

            #Update the score
            score += 10
            scorestring = "Score %s" %score
            #clears previous score number in order for the numbers to not overlap
            score_pen.clear()
            score_pen.write(scorestring, False, align = "left", font = ("Arial", 14, "normal"))

        if isCollision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            print("Game Over, bub.")
            break

    #Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed #increases bulletspeed
        bullet.sety(y)

    #Check to see if bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        #goes back to bulletstate "ready"
        bulletstate = "ready"

    #Check for a collision between the bullet and the enemy

delay = raw_input("Press enter to finish.")
