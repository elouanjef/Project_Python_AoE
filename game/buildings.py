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
            self.health -= 1


class Barracks:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "building02.png"))
        self.image = image
        self.name = "Barracks"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.res = [125, 0, 0, 0]
        self.health = 350

    def update(self):
        if self.health != 0:
            self.health -= 1

class LumberMill:

    def __init__(self, pos):
       image = pg.image.load(path.join(graphics_folder,"building03.png"))
       self.image = image
       self.name = "LumberMill"
       self.rect = self.image.get_rect(topleft=pos)
       self.res = [150, 0, 0, 0]
       self.health = 500
    
    def update(self):
        if self.health != 0:
            self.health -= 1

class Siege:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "building04.png"))
        self.image = image
        self.name = "Siege"
        self.rect = self.image.get_rect(topleft=pos)
        self.res = [200, 0, 0, 0]
        self.health = 350

    def update(self):
        if self.health != 0:
            self.health -= 1

class Stable:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "building05.png"))
        self.image = image
        self.name = "Stable"
        self.rect = self.image.get_rect(topleft=pos)
        self.res = [150, 0, 0, 0]
        self.health = 350

    def update(self):
        if self.health != 0:
            self.health -= 1

class House:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "building06.png"))
        self.image = image
        self.name = "LumberMill"
        self.rect = self.image.get_rect(topleft=pos)
        self.res = [25, 0, 0, 0]
        self.health = 550

    def update(self):
        if self.health != 0:
            self.health -= 1




#class TownCenter(Unite):
    # def __init__(self,pos):
    #     super.__init__("centre_ville","batiment")
    #     self.res = self.unite_res["centre_ville"]
    #     image = pg.image.load(path.join(graphics_folder,"building01.png"))
    #     self.image = image
    #     self.counter = 0
    #     self.rect = self.image.get_rect(topleft=pos)

    
