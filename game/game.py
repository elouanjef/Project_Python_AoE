import pygame as pg
import sys

from .world import World
from settings import *
from .utils import draw_text
from .camera import Camera
from .hud import Hud
from .resource import ResourceManager
from .units import Archer, Infantryman, Villager
from .buildings import TownCenter
from .events import *
from .AI import *

class Game:

    # preparing the screen and coordinates for the game
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        #event
        self.events = Event(clock)

        # resource
        self.resource_manager = ResourceManager()

        # entities
        self.entities = []

        # hud
        self.hud = Hud(self.resource_manager, self.width, self.height, self.events)


        # create the world with 50 by 50 grid
        self.world = World(self.resource_manager, self.entities, self.hud, 50, 50, self.width, self.height,self.events)
        #Archer(self.world.world[25][25], self.world, self.resource_manager)
        #Infantryman(self.world.world[26][26], self.world, self.resource_manager)
        #create_unit(Archer)
        # camera3
        self.camera = Camera(self.width, self.height)
        #print(self.world.world[25][25])

        self.game_time = Game_time()

        self.AI = AI(self.game_time)



    # running
    def run(self):
        self.playing = True
        while self.playing:
            tick = self.clock.tick(60)  # we can change fps here by increasing this number. ATTENTION: be careful the configuration of the computer.
            #self.events()
            self.game_time.second += tick/1000
            self.update()
            self.draw()
            self.events.events()
            self.AI.action()



    # capture the events
    def events(self):
        for event in pg.event.get():
            # Exit the game by clicking the red cross
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            # Exit game by pressing escape (Echap in fr)  button on the keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

    def update(self):
        self.camera.update()
        for e in self.entities: e.update()
        self.hud.update()
        self.world.update(self.camera)
        self.game_time.update()


    def draw(self):
        # his method is used to fill the display with black
        self.screen.fill(BLACK)
        self.world.draw(self.screen, self.camera)
        self.hud.draw(self.screen)
        draw_text(
            self.screen,  # print it on screen
            "fps={}".format(round(self.clock.get_fps())),  # get value
            25,  # text's size
            WHITE,  # the text's colour
            (900, 3)  # position of the text (x, y)
        )

        draw_text(
            self.screen,  # print it on screen
            f"%02d : %02d"%(self.game_time.minute,self.game_time.second),
            25,  # text's size
            PURPLE,  # the text's colour
            (1100, 3)  # position of the text (x, y)
        )

        pg.display.flip()


