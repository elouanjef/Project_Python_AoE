import pygame as pg
from settings import *
from game.world import *
from os import path


class MapResource:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.resource_cooldown = pg.time.get_ticks()

        self.available = True

    def mine(self):
        if self.the_rest > 0 and self.available:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                self.the_rest -= 1
                self.resource_cooldown = now
                self.resource_manager.starting_resources[self.resource_type] += 1

            return 1
        else:
            self.available = False

    def get_rest(self):
        return self.the_rest


class Map_Tree(MapResource):
    game_name = "Arbre"
    image = Tree_img
    the_rest = 400
    the_rest_max = 400
    resource_type = "Wood"


class Map_Rock(MapResource):
    game_name = "Carrière de pierre"
    image = Rock_img
    the_rest = 5000
    the_rest_max = 5000
    resource_type = "Rock"


class Map_Gold(MapResource):
    game_name = "Or"
    image = Gold_img
    the_rest = 250
    the_rest_max = 250
    resource_type = "Gold"


class Map_Bush(MapResource):
    game_name = "Buisson"
    image = Bush_img
    the_rest = 250
    the_rest_max = 250
    resource_type = "Food"

class Map_Tile:
    def __init__(self):
        self.the_rest = 0

    def _____(self):
        pass

    def get_rest(self):
        return self.the_rest
