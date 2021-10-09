import pygame as pg
from pygame.constants import MOUSEBUTTONDOWN
from math import  acos, sqrt, cos, sin
pg.init()

clock = pg.time.Clock()
current_time = 0
win = pg.display.set_mode((0, 0), pg.NOFRAME)
pg.display.toggle_fullscreen()
#win = pg.display.set_mode((1000, 500))

pg.display.set_caption("First Game")
class character:
    def __init__(self):
        self.x = 50
        self.y = 50
        self.radius = 5
        self.step_size = 5
        self.color = (150, 150, 150)
        self.tempx = 0
        self.tempy = 0

    #this will return the angle between 2 line: the line from player position and to the end point and the horizontal line
    def findDegrees(self,start_x,start_y,target_x,target_y):
        if target_x!=start_x and target_y!= start_y:
            a=sqrt((target_x-start_x)*(target_x-start_x)+(target_y-start_y)*(target_y-start_y))
            b=10 #  a random number
            c=sqrt((target_x-start_x-10)*(target_x-start_x-10)+(target_y-start_y)*(target_y-start_y))
            if target_y <=start_y :
                return acos((a * a + b * b - c * c)/(2.0 * a * b))
            else:
                return -acos((a * a + b * b - c * c)/(2.0 * a * b))
    #Capture mouse click position
    # def mouse_click(self):
    #   x,y = pg.mouse.get_pos()
    #   return x,y

    def move(self, target_x, target_y):
        moving = True
        if abs(target_x-self.x)<10**(-3): 
            velocity_x=0
        else: 
            velocity_x=(self.step_size*abs(target_x-self.x))/sqrt(abs(target_x-self.x)*abs(target_x-self.x)+abs(target_y-self.y)*abs(target_y-self.y))
        if abs(target_y-self.y)<10**(-3): 
            velocity_y=0
        else: 
            velocity_y=(self.step_size*abs(target_y-self.y))/sqrt(abs(target_x-self.x)*abs(target_x-self.x)+abs(target_y-self.y)*abs(target_y-self.y))
        while moving:
            if not(target_x - velocity_x < self.x and self.x < target_x + velocity_x):
                if target_x >= self.x:
                    self.x += velocity_x
                else:
                    self.x -= velocity_x

            if not(target_y-velocity_y < self.y and self.y < target_y + velocity_y):
                if target_y >= self.y:
                    self.y+=velocity_y
                else:
                    self.y-=velocity_y
            if((abs(target_x-self.x) < self.step_size)and (abs(target_y-self.y) < self.step_size)):
                moving=False
            pg.time.delay(100)
            win.fill((0, 0, 0))
            pg.draw.circle(win, crts.color, (crts.x, crts.y), crts.radius)
            pg.display.update()
            print("position: (%f, %f)" % (self.x,self.y))

    def cha_move(self):
        pass
            

    
crts = character()
run = True
while run:
    #pg.time.delay(200)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            pg.quit()
        if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                    #pg.quit()

    #keys = pg.key.get_pressed()
    if event.type == MOUSEBUTTONDOWN:
        x,y = pg.mouse.get_pos()
        crts.move(x,y)

        
    win.fill((0, 0, 0))

    pg.draw.circle(win, crts.color, (crts.x, crts.y), crts.radius)
    pg.display.update()



pg.quit()