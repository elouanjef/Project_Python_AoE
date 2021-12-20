import pygame as pg
from settings import *
from game.resource import *
from game.world import *
from os import path


# from units import *

class Building:
    def __init__(self, pos, resource_manager, team):
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.health_bar_length = HEALTH_BAR_LENGTH
        self.health_ratio = self.health_max / self.health_bar_length
        self.team = team
        self.resource_manager.buy(self)

    def update(self):
        if self.health < self.health_max:
            self.health += 2


class TownCenter(Building):
    image = towncenter
    name = "TownCenter"
    game_name = "Forum"
    health = 0
    health_max = 1000


class Barracks(Building):
    image = barracks
    name = "Barracks"
    game_name = "Caserne"
    health = 0
    health_max = 500


class Archery(Building):
    image = archery
    name = "Archery"
    game_name = "Camp de tir à l'arc"
    health = 0
    health_max = 500
