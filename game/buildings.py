import pygame as pg
from settings import *
from game.resource import *
from game.world import *
from os import path
#from units import *


class TownCenter:

    def __init__(self, pos,resource_manager):
        image = building01
        self.image = image
        self.name = "TownCenter"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
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

    def __init__(self, pos, resource_manager):
        image = building03
        self.image = image
        self.name = "Barracks"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
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

    def __init__(self, pos, resource_manager):
       image = building02
       self.image = image
       self.name = "LumberMill"
       self.rect = self.image.get_rect(topleft=pos)
       self.resource_manager = resource_manager
       self.resource_manager.cost_to_resource(self.name)
       self.health_max = 500
       self.health = 0
       self.resource_cooldown = pg.time.get_ticks()

    def update(self, action):

        if action == 0:
            if self.health != 0:
                self.health -= 1
        elif action == 1:
            if self.health < self.health_max:
                self.health += 1
            elif self.health == self.health_max:
                now = pg.time.get_ticks()
                if now - self.resource_cooldown > 2000:
                    self.resource_manager.resources["wood"] += 1
                    self.resource_cooldown = now


    
