import pygame as pg
from settings import *
from os import path
#from units import *


class TownCenter:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder,"building01.png"))
        self.image = image
        self.name = "TownCenter"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.res = [600, 0, 0, 0]
        self.health = 1000
    
    def update(self):
        if self.health != 0:
            self.health -= 10


class LumberMill:

    def __init__(self, pos):
       image = pg.image.load(path.join(graphics_folder,"building02.png"))
       self.image = image
       self.name = "LumberMill"
       self.rect = self.image.get_rect(topleft=pos)
       self.res = [150, 0, 0, 0]
       self.health = 500
    
    def update(self):
        if self.health != 0:
            self.health -= 10



#class TownCenter(Unite):
    # def __init__(self,pos):
    #     super.__init__("centre_ville","batiment")
    #     self.res = self.unite_res["centre_ville"]
    #     image = pg.image.load(path.join(graphics_folder,"building01.png"))
    #     self.image = image
    #     self.counter = 0
    #     self.rect = self.image.get_rect(topleft=pos)

    