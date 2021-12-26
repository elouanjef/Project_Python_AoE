import pygame as pg
from settings import *
from game.resource import *
from game.world import *
from os import path


# from units import *

class Building:
    def __init__(self, pos, resource_manager, team, beginning):
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.resource_manager = resource_manager
        self.health_bar_length = HEALTH_BAR_LENGTH_BUILDING
        self.health_ratio = self.health_max / self.health_bar_length
        self.team = team
        self.pos = pos
        if not beginning:
            self.resource_manager.buy(self)

    def update(self):
        if self.health < self.health_max:
            self.health += 2

    def health_bar(self):
        for i in range(4):
            # pg.draw.rect(sprite, BLACK, (1+i, 1+i,entity.health_bar_length, 5), 4)
            pg.draw.rect(self.bar_image, BLACK, (-i, -i, self.health_bar_length, 5), 5)

        pg.draw.rect(self.bar_image, GREEN, (1, 1, (self.health / self.health_ratio) - 9, 5))
        return self.bar_image


class TownCenter(Building):
    bar_image = towncenter.copy()
    image = towncenter
    name = "TownCenter"
    game_name = "Forum"
    health = 0
    health_max = 1000


class Barracks(Building):
    bar_image = barracks.copy()
    image = barracks
    name = "Barracks"
    game_name = "Caserne"
    health = 0
    health_max = 500


class Archery(Building):
    bar_image = archery.copy()
    image = archery
    name = "Archery"
    game_name = "Camp de tir à l'arc"
    health = 0
    health_max = 500
