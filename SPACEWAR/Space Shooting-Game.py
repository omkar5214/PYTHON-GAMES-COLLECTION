import os
import random
import time
import math
#Import the Turtle module
import turtle
#Required by MacOSX to show the window
turtle.fd(0)
#Set the animations speed to the maximum
turtle.speed(0)
#Change the background color
turtle.bgcolor("black")
#Change the window title
turtle.title("SpaceWar")
#Change the background image
#######turtle.bgpic("starfield.gif")
#Hide the default turtle
turtle.ht()
#This saves memory
turtle.setundobuffer(1)
#This speeds up drawing
turtle.tracer(0)
# ---------------- SPACESHIP SHAPE ----------------
spaceship_shape = (
    (0, 25),
    (-10, 10),
    (-20, 0),
    (-10, -5),
    (-5, -20),
    (0, -10),
    (5, -20),
    (10, -5),
    (20, 0),
    (10, 10),
)

turtle.register_shape("spaceship", spaceship_shape)

class Sprite(turtle.Turtle):
 def __init__(self, spriteshape, color, startx, starty):
  turtle.Turtle.__init__(self, shape = spriteshape)
  self.speed(0)
  self.penup()
  self.color(color)
  self.fd(0)
  self.goto(startx, starty)
  self.speed = 1
  
 def move(self):
  self.fd(self.speed)
  
  #Boundary detection
  if self.xcor() > 290:
   self.setx(290)
   self.rt(60)
  
  if self.xcor() < -290:
   self.setx(-290)
   self.rt(60)
  
  if self.ycor() > 290:
   self.sety(290)
   self.rt(60)
  
  if self.ycor() < -290:
   self.sety(-290)
   self.rt(60)
   
 def is_collision(self, other):
  if (self.xcor() >= (other.xcor() - 20)) and \
  (self.xcor() <= (other.xcor() + 20)) and \
  (self.ycor() >= (other.ycor() - 20)) and \
  (self.ycor() <= (other.ycor() + 20)):
   return True
  else:
   return False
    
class Player(Sprite):
 def __init__(self, spriteshape, color, startx, starty):
  Sprite.__init__(self, spriteshape, color, startx, starty)
  self.shapesize(stretch_wid=0.8, stretch_len=1.1, outline=None)
  self.speed = 4
  self.lives = 3

 def turn_left(self):
  self.lt(45)
  
 def turn_right(self):
  self.rt(45)

 def accelerate(self):
  self.speed += 1
  
 def decelerate(self):
  self.speed -= 1


# ---------------- PACMAN SHAPE GENERATOR ----------------
def create_enemy_shape(radius=20, mouth_angle=60):
    points = []

    # Start at center (important for pie shape)
    points.append((0, 0))

    # First edge of mouth
    start_angle = mouth_angle
    rad = math.radians(start_angle)
    points.append((radius * math.cos(rad), radius * math.sin(rad)))

    # Arc
    for angle in range(mouth_angle, 360 - mouth_angle, 2):
        rad = math.radians(angle)
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        points.append((x, y))

    # Second edge back to center
    end_angle = 360 - mouth_angle
    rad = math.radians(end_angle)
    points.append((radius * math.cos(rad), radius * math.sin(rad)))

    points.append((0, 0))  # close shape

    return tuple(points)

# Register smooth shapes
turtle.register_shape("enemy_closed", create_enemy_shape(20, 0))
turtle.register_shape("enemy_open", create_enemy_shape(20, 65))


class Enemy(Sprite):
    def __init__(self, shape, color, x, y):
        super().__init__(shape, color, x, y)
        self.shapesize(0.8, 0.8)
        self.speed = random.randint(3, 5)
        self.setheading(random.randint(0, 360))

        # animation
        self.frames = ["enemy_closed", "enemy_open"]
        self.frame_index = 0
        self.delay = 0
        self.animation_speed = 20
        self.color("firebrick")  # enemy color

    def move(self):
        self.fd(self.speed)

        # animate mouth
        self.delay += 1
        if self.delay % self.animation_speed == 0:
            self.frame_index = (self.frame_index + 1) % 2
            self.shape(self.frames[self.frame_index])

        # boundary
        if self.xcor() > 290:
            self.setx(290)
            self.rt(60)

        if self.xcor() < -290:
            self.setx(-290)
            self.rt(60)

        if self.ycor() > 290:
            self.sety(290)
            self.rt(60)

        if self.ycor() < -290:
            self.sety(-290)
            self.rt(60)

class Ally(Sprite):
 def __init__(self, spriteshape, color, startx, starty):
  Sprite.__init__(self, spriteshape, color, startx, starty)
  self.speed = 8
  self.setheading(random.randint(0,360))

 def move(self):
  self.fd(self.speed)
  
  #Boundary detection
  if self.xcor() > 290:
   self.setx(290)
   self.lt(60)
  
  if self.xcor() < -290:
   self.setx(-290)
   self.lt(60)
  
  if self.ycor() > 290:
   self.sety(290)
   self.lt(60)
  
  if self.ycor() < -290:
   self.sety(-290)
   self.lt(60)


  
class Missile(Sprite):
 def __init__(self, spriteshape, color, startx, starty):
  Sprite.__init__(self, spriteshape, color, startx, starty)
  self.shapesize(stretch_wid=0.2, stretch_len=0.4, outline=None)
  self.speed = 15
  self.status = "ready"
  self.goto(-1000, 1000)
  
 def fire(self):
  if self.status == "ready":
   #Play missile sound
   ####os.system("afplay laser.mp3&")
   self.goto(player.xcor(), player.ycor())
   self.setheading(player.heading())
   self.status = "firing"
   
 def move(self):
	
  if self.status == "ready":
   self.goto(-1000, 1000)
  
  if self.status == "firing":
   self.fd(self.speed) 
   
  #Border check
  if self.xcor() < -290 or self.xcor() > 290 or \
   self.ycor()< -290 or self.ycor()> 290:
   self.goto(-1000,1000)
   self.status = "ready"

class Particle(Sprite):
 def __init__(self, spriteshape, color, startx, starty):
  Sprite.__init__(self, spriteshape, color, startx, starty)
  self.shapesize(stretch_wid=0.1, stretch_len=0.1, outline=None)
  self.goto(-1000,-1000)
  self.frame = 0
  
 def explode(self, startx, starty):
  self.goto(startx,starty)
  self.setheading(random.randint(0,360))
  self.frame = 1

 def move(self):
  if self.frame > 0:
   self.fd(10)
   self.frame += 1

  if self.frame > 15:
   self.frame = 0
   self.goto(-1000, -1000)

class Game():
 def __init__(self):
  self.level = 1
  self.score = 0
  self.state = "playing"
  self.pen = turtle.Turtle()
  self.lives = 3
  
 def draw_border(self):
  #Draw border
  self.pen.speed(0)
  self.pen.color("white")
  self.pen.pensize(3)
  self.pen.penup()
  self.pen.goto(-300, 300)
  self.pen.pendown()
  for side in range(4):
   self.pen.fd(600)
   self.pen.rt(90)
  self.pen.penup()
  self.pen.ht()
  self.pen.pendown()
  
 def show_status(self):
  self.pen.undo()
  msg = "Score: %s" %(self.score)
  self.pen.penup()
  self.pen.goto(-300, 310)
  self.pen.write(msg, font=("Arial", 16, "normal"))


#Create game object
game = Game()

#Draw the game border
game.draw_border()

#Show the game status
game.show_status()

#Create my sprites
player = Player("spaceship", "cyan", 0, 0)
#enemy = Enemy("circle", "red", -100, 0)
missile = Missile("triangle", "yellow", 0, 0)
#ally = Ally("square", "blue", 100, 0)

enemies =[]
for i in range(4):
    x = random.randint(-200, 200)
    y = random.randint(-200, 200)
    enemies.append(Enemy("enemy_closed", "yellow", x, y))

allies =[]
for i in range(3):
 allies.append(Ally("square", "blue", 100, 0))

particles = []
for i in range(20):
 particles.append(Particle("circle", "orange", 0, 0))

#Keyboard bindings
turtle.onkey(player.turn_left, "Left")
turtle.onkey(player.turn_right, "Right")
turtle.onkey(player.accelerate, "Up")
turtle.onkey(player.decelerate, "Down")
turtle.onkey(missile.fire, "space")
turtle.listen()

#Main game loop
while True:
 turtle.update()
 time.sleep(0.04)

 player.move()
 missile.move()
	
 for enemy in enemies:
  enemy.move()
  
  #Check for a collision with the player
  if player.is_collision(enemy):
   #Play explosion sound
   #####os.system("afplay explosion.mp3&")
   x = random.randint(-250, 250)
   y = random.randint(-250, 250)
   enemy.goto(x, y)
   game.score += 100
   game.show_status()
   
  #Check for a collision between the missile and the enemy
  if missile.is_collision(enemy):
   #Play explosion sound
   ######os.system("afplay explosion.mp3&")
   x = random.randint(-250, 250)
   y = random.randint(-250, 250)
   enemy.goto(x, y)
   missile.status = "ready"
   #Increase the score
   game.score += 100
   game.show_status()
   #Do the explosion
   for particle in particles:
    particle.explode(missile.xcor(), missile.ycor())
   

  
 for ally in allies:
  ally.move()

  #Check for a collision between the missile and the ally
  if missile.is_collision(ally):
   #Play explosion sound
   #####.system("afplay explosion.mp3&")
   x = random.randint(-250, 250)
   y = random.randint(-250, 250)
   ally.goto(x, y)
   missile.status = "ready"
   #Decrease the score
   game.score -= 50
   game.show_status() 


 for particle in particles:
  particle.move()



delay = input("Press enter to finish. > ")
