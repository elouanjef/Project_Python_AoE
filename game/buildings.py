import pygame as pg
from settings import *
from game.resource import *
from game.world import *
from os import path


# from units import *


class TownCenter:

    def __init__(self, pos, resource_manager, events):
        image = building01
        self.image = image
        self.events = events
        self.name = "TownCenter"
        self.game_name = "Town center"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
        self.health_max = 1000
        self.health = 0

    def update(self):
        if self.health < self.health_max:
            self.health += 1

    def destroy(self):
        self.events.destroy = True


class Barracks:

    def __init__(self, pos, resource_manager):
        image = building03
        self.image = image
        self.name = "Barracks"
        self.game_name = "Barracks"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
        self.health_max = 350
        self.health = 0

    def update(self):
        if self.health < self.health_max:
            self.health += 1


class LumberMill:

    def __init__(self, pos, resource_manager):
        image = building02
        self.image = image
        self.name = "LumberMill"
        self.game_name = "Lumber mill"
        self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
        self.health_max = 500
        self.health = 0
        self.resource_cooldown = pg.time.get_ticks()

    def update(self):
        if self.health < self.health_max:
            self.health += 1
        elif self.health == self.health_max:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                self.resource_manager.resources["wood"] += 1
                self.resource_cooldown = now



