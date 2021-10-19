import pygame as pg
import sys

from .world import World
from settings import *
from .utils import  draw_text
from .camera import Camera
from .hud import Hud
from resource import *


class Game:


    #preparing the screen and coordinates for the game
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        #entities
        self.entities = []

        #hud 
        self.hud = Hud(self.width, self.height)

        #resource
        #self.resource = Resource(0,0,0,0)

        #create the world with 50 by 50 grid
        self.world = World(self.entities,self.hud, 50, 50, self.width, self.height )      # ,self.resource

        #camera
        self.camera = Camera(self.width, self.height)



    #running
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(60)    #we can change fps here by increasing this number. ATTENTION: be careful the configuration of the computer. 
            self.events()
            self.update()
            self.draw()


    #capture the events
    def events(self):
        for event in pg.event.get():
            #Exit the game by clicking the red cross
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            #Exit game by pressing escape (Echap in fr)  button on the keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        self.camera.update()
        for e in self.entities: e.update(CONSTRUCTION)
        self.hud.update()
        self.world.update(self.camera)

    def draw(self):
        #his method is used to fill the display with black 
        self.screen.fill(BLACK)
        self.world.draw(self.screen,self.camera)
        self.hud.draw(self.screen)
   
        draw_text(
            self.screen,                                    #print it on screen
            "fps={}".format(round(self.clock.get_fps())),   #get value
            25,                                             #text's size 
            WHITE,                                          #the text's colour
            (900, 3)                                       #position of the text (x, y)
        )
        

        pg.display.flip()