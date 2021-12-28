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
        self.age_2 = False
        self.age = 'Firstage'
        if not beginning:
            self.resource_manager.buy(self)

    def update(self):
        if self.health < self.health_max:
            self.health += 10

    def health_bar(self):
        for i in range(4):
            # pg.draw.rect(sprite, BLACK, (1+i, 1+i,entity.health_bar_length, 5), 4)
            pg.draw.rect(self.bar_image, BLACK, (-i, -i, self.health_bar_length, 5), 5)

        pg.draw.rect(self.bar_image, GREEN, (1, 1, (self.health / self.health_ratio) - 9, 5))
        return self.bar_image

    def passer_age(self):
        if self.game_name == 'Forum':
            self.age = 'Secondage'
            if self.resource_manager.buy_age(self) != -1 and not self.age_2:
                self.bar_image = self.secondage_image.copy()
                self.image = self.secondage_image
                self.age_2 = True
                self.health_max += 1000
                if self.health == self.health_max:
                    self.health += 1000
            else:
                self.age = 'Firstage'
        else:
            self.age = 'Secondage'
            if not self.age_2:
                self.bar_image = self.secondage_image.copy()
                self.image = self.secondage_image
                self.age_2 = True
                self.health_max += 1000
                if self.health == self.health_max:
                    self.health += 1000


class TownCenter(Building):
    bar_image = firstage_towncenter.copy()
    image = firstage_towncenter
    secondage_image = secondage_towncenter
    name = "TownCenter"
    game_name = "Forum"
    health = 0
    health_max = 1000


class Barracks(Building):
    bar_image = firstage_barracks.copy()
    image = firstage_barracks
    secondage_image = secondage_barracks
    name = "Barracks"
    game_name = "Caserne"
    health = 0
    health_max = 500


class Archery(Building):
    bar_image = firstage_archery.copy()
    image = firstage_archery
    secondage_image = secondage_archery
    name = "Archery"
    game_name = "Camp de tir à l'arc"
    health = 0
    health_max = 500
