import pygame as pg
import sys

from .world import World
from pygame.constants import K_ESCAPE
from .settings import BLACK, BLUE, RED, WHITE ,TILE_SIZE, TILE_SIZE_MINI_MAP
from .utils import  draw_text
from .camera import Camera
from .hud import Hud


class Game:


    #preparing the screen and coordinates for the game
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.width, self.height = self.screen.get_size()

        #create the world with 50 by 50 grid
        self.world = World(50, 50, self.width, self.height)

        #camera
        self.camera = Camera(self.width, self.height)

        #hud
        self.hud = Hud(self.width, self.height)


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
        self.hud.update()

    def draw(self):
        #his method is used to fill the display with black 
        self.screen.fill(BLACK)

        self.screen.blit(self.world.grass_tiles, (self.camera.scroll.x, self.camera.scroll.y))

        #draw coordinate lines 
        for x in range(self.world.grid_length_x):
            for y in range(self.world.grid_length_y):

                #on rect minimap (draw with blue color)
                #sq = self.world.world[x][y]["cart_rect_mini_map"]
                #rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE_MINI_MAP, TILE_SIZE_MINI_MAP)
                #pg.draw.rect(self.screen,BLUE, rect, 1)


                #on iso_poly minimap (draw with blue color)
                mini = self.world.world[x][y]["iso_poly_mini"]
                mini = [(x + 200, y + 20) for x,y in mini]        # position x + ...., y  + ...
                pg.draw.polygon(self.screen, BLUE, mini, 1)

                
                #on our isometric map (red color)
                #create the world's block
                render_pos = self.world.world[x][y]["render_pos"]

                #this is the world merged with the computer's screen
                #self.screen.blit(self.world.tiles["block"], (render_pos[0] + self.width/2, render_pos[1] + self.height/4))


                #create the other world's object
                tile = self.world.world[x][y]["tile"]
                if tile != "":
                    self.screen.blit(self.world.tiles[tile], 
                                    (render_pos[0] + self.world.grass_tiles.get_width()/2 + self.camera.scroll.x, 
                                     render_pos[1] - (self.world.tiles[tile].get_height() - TILE_SIZE) + self.camera.scroll.y))



                #Grid on the main map
                #p = self.world.world[x][y]["iso_poly"]
                #p = [(x + self.width/2, y + self.height/4) for x,y in p]
                #pg.draw.polygon(self.screen, RED, p, 1)


        self.hud.draw(self.screen)
   
        draw_text(
            self.screen,                                    #print it on screen
            "fps={}".format(round(self.clock.get_fps())),   #get value
            25,                                             #text's size 
            WHITE,                                          #the text's colour
            (900, 3)                                       #position of the text (x, y)
        )
        

        pg.display.flip()