import pygame as pg
from settings import *
from game.resource import *
from game.world import *
from os import path


# from units import *


class TownCenter:

    def __init__(self, pos, resource_manager, team):
        image = towncenter
        self.image = image
        self.name = "TownCenter"
        self.game_name = "Forum"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.resource_manager.buy(self.name)
        self.health_max = 1000
        self.health = 0
        self.team = team

    def update(self):
        if self.health < self.health_max:
            self.health += 100


class Barracks:

    def __init__(self, pos, resource_manager, team):
        image = barracks
        self.image = image
        self.name = "Barracks"
        self.game_name = "Caserne"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.resource_manager.buy(self.name)
        self.health_max = 350
        self.health = 0
        self.team = team

    def update(self):
        if self.health < self.health_max:
            self.health += 1


class Archery:

    def __init__(self, pos, resource_manager, team):
        image = archery
        self.image = image
        self.name = "Archery"
        self.game_name = "Camp de tir à l'arc"
        self.pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.resource_manager.buy(self.name)
        self.health_max = 350
        self.health = 0
        self.team = team

    def update(self):
        if self.health < self.health_max:
            self.health += 15

"""
class LumberMill:

    def __init__(self, pos, resource_manager, team):
        image = lumbermill
        self.image = image
        self.name = "LumberMill"
        self.game_name = "Lumber mill"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.buy(self.name)
        self.health_max = 500
        self.health = 0
        self.resource_cooldown = pg.time.get_ticks()
        self.team = team

    def update(self):
        if self.health < self.health_max:
            self.health += 1
        elif self.health == self.health_max:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                self.resource_manager.starting_resources["wood"] += 1
                self.resource_cooldown = now"""