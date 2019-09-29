import pygame, sys,random
from pygame.locals import *
##used for drawing score
font_name = pygame.font.match_font('arial')

def draw_text(dis, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, (40,40, 0))
    text_rect = text_surface.get_rect()
    text_rect.x = x
    text_rect.y = y
    dis.blit(text_surface, text_rect)

##rectangle class
class Rectangle:
    ##local variables
    width = 24 ## width of the rectangle
    height = 24## height of the rectangle
    x = 250    ## x position of the rectangle
    y = 250    ## y position of the rectangle
    velX = 0   ## x velocity of the rectangle
    velY = -1  ## y velocity of the rectangle
    color = (255, 255, 255) ##color of the rectangle

    ##initalizes the rectangle called on creation of a rectangle object
    def __init__(self, color):
        self.color = color

    ##sets the position of the rectangle
    def set_pos(self, x, y):
        self.x = x
        self.y = y

    ##sets the velocity of the rectangle
    def set_vel(self, vx, vy):
        self.velX = vx
        self.velY = vy

    ##draw the rectangle based on the position and the color
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x + 1, self.y + 1 , self.width, self.height));

    ##udates rectangle based on velocity
    def update(self):
        self.x += (self.velX * 25)
        if self.x > 475:
            self.x = 0
        elif self.x < 0:
            self.x = 475
        self.y += (self.velY * 25)
        if self.y > 475:
            self.y = 0
        elif self.y < 0:
            self.y = 475
    ##checks for colision between rectangles
    def colision(self, x, y):
        if self.x < x + 25 and self.x + 25 > x and self.y < y + 25 and self.y + 25 > y: return 1
        else: return 0

##class that represents the apple extends rectangle class
class food(Rectangle):
    ## food initializing class called on creation of a food object
    def __init__(self, color):
        random.seed()
        self.x = random.randrange(0, 500, 25)
        self.y = random.randrange(0, 500, 25)
        super(food, self).__init__( color )## super is used in an init method to call the init for the class it extends

    ##sets the food to a new position when it is grabbed
    def new_pos(self):
        random.seed()
        self.x = random.randrange(0, 500, 25)
        self.y = random.randrange(0, 500, 25)

## class that represents the head of the snake is seperate from the rest of the body because it is controled
## by the user
class Head(Rectangle):
    ##local variables
    score = 0 ##score is a storage place to hold a number representing the players score

    ##handles controls
    def controls(self, keys):
        if keys[K_UP] == 1:
            if self.velY != 1:
                self.velX = 0
                self.velY = -1
        elif keys[K_DOWN] == 1:
            if self.velY != -1:
                self.velX = 0
                self.velY = 1
        elif keys[K_LEFT] == 1:
            if self.velX != 1:
                self.velX = -1
                self.velY = 0
        elif keys[K_RIGHT] == 1:
            if self.velX != -1:
                self.velX = 1
                self.velY = 0

    ##this is done when the snake dies resets snakes head and resets score
    def die(self):
        self.x = 250
        self.y = 250
        self.velY = -1
        self.velX = 0

##class that represents the body of the snake
class Body():
    body = [] ## this is a vector of rectagles named body holds all the segments of the snakes body

    def __init__(self):
        self.color = (0,255, 0)
        for i in range(1, 5):
            self.body.append(Rectangle(self.color))
            self.body[i - 1].set_pos(self.body[i - 1].x, self.body[i - 1].y + (i * 25))

    ##updates the body based on the rectangle class and velocity
    def update(self):
        for index in range(len(self.body)):
            self.body[index].update()

    ##draws the body of the snake on the screen
    def draw(self, display):
        for index in range(len(self.body)):
            self.body[index].draw(display)

    ##used to pass velocity between body parts so they stay togeather
    def vel_exchange(self, velX, velY):
        i = len(self.body) - 1
        while i >= 1:
            self.body[i].set_vel(self.body[i - 1].velX, self.body[i - 1].velY)
            i = i - 1
        self.body[0].set_vel(velX, velY)

    ##checks collision
    def collision(self, x, y):
        for index in range(len(self.body)):
           if self.body[index].colision(x, y) == 1:
               return 1
        return 0

    ##adds a segment to the body used when snake eats food
    def add_segment(self):
        self.body.append(Rectangle(self.color))
        self.body[len(self.body) - 1].set_pos(self.body[len(self.body) - 2].x,self.body[len(self.body) - 2].y)
        self.body[len(self.body) - 1].set_vel(0,0)

    ##used when the snake dies to reset the body
    def die(self, x , y):
        i = len(self.body) - 1
        while i >= 1:
            self.body[i].set_pos(250, 250 + ((i + 1) * 25))
            self.body[i].set_vel(0, -1)
            if i > 3:
                self.body.pop(i)
            i -= 1
        self.body[0].set_pos(x, y + 25)
        self.body[0].set_vel(0, -1)

## class to handle the level design around the snake
class Background:
    black = (0,0,0)## this is just the color black

    def __init__(self, color):
        self.black = color

    def draw(self, screen):
        for w in range (0, 20):
            pygame.draw.line(screen, self.black,(w * 25,0), (w * 25,500))
            pygame.draw.line(screen, self.black, (0, w * 25), (500, w * 25))


def main():
    pygame.init()##need to use pygame used for user input and display

    b = Background((0, 0, 0))##color for the background
    h = Head((255, 0, 0))##color for the snakes head
    body = Body()##color for the snakes body
    f = food((0,0,255))##color for the food

    ##sets up the display with a with and height of 500
    DISPLAY=pygame.display.set_mode((500,500),0,32)

    WHITE=(255,255,255)##the color white
    BLUE=(0,0,255)##the color blue

    DISPLAY.fill(WHITE)##clears the screen making it white

    clock = 0## holds a number representing time used to make the game run consistantly

    while True:##game loop start
        for event in pygame.event.get():
            if event.type == QUIT:## if the user quits this ends the program
                pygame.quit()
                sys.exit()
        clock += 1
        pygame.time.delay(50) ## delays game running by 50 miliseconds
        h.controls(pygame.key.get_pressed()) ##this gets keys pressed
        if clock % 2 == 0: ## this if statment happens every other time through the loop
            h.update()
            body.update()
            body.vel_exchange(h.velX, h.velY)
            if h.colision(f.x, f.y) == 1:
                body.add_segment()
                h.score += 100
                f.new_pos()
            if body.collision(h.x, h.y) == 1:
                h.die()
                body.die(h.x, h.y)
                h.score = 0
                pass
            DISPLAY.fill(WHITE)## clears the screen
            ## we start drawing here
            b.draw(DISPLAY)
            h.draw(DISPLAY)
            body.draw(DISPLAY)
            f.draw(DISPLAY)
            draw_text(DISPLAY, str(h.score), 14, 10, 10)
            pygame.display.update()
            ##we are done drawing here
            clock -= 2
            h.score += 10


main()## this is the call to run the main method at the start of the program