import pygame as pg
from settings import *
from game.resource import *
from game.world import *
from os import path
#from units import *


class TownCenter:

    def __init__(self, pos):
        image = image_T
        self.image = image
        self.name = "Town center"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.pos = pos

        self.health_max = 1000
        self.health = 0

    def update(self, action):
        if action == 0:
            if self.health != 0:
                self.health -= 1

        elif action == 1:
            if self.health < self.health_max:
                self.health += 1


class Barracks:

    def __init__(self, pos):
        image = image_B
        self.image = image
        self.name = "Barracks"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.res = [125, 0, 0, 0]
        self.health_max = 350
        self.health = 0
        self.pos = pos

    def update(self, action):
        if action == 0:
            if self.health != 0:
                self.health -= 1
        elif action == 1:

            if self.health < self.health_max:
                self.health += 1

class LumberMill:

    def __init__(self, pos):
       image = image_M
       self.image = image
       self.name = "Lumber mill"
       self.rect = self.image.get_rect(topleft=pos)
       self.res = [150, 0, 0, 0]
       self.health_max = 500
       self.health = 0
       self.pos = pos

    def update(self, action):
        if action == 0:
            if self.health != 0:
                self.health -= 1
        elif action == 1:
            if self.health < self.health_max:
                self.health += 1

    
