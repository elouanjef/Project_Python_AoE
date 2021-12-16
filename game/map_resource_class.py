import pygame as pg
from settings import *
from game.world import *
from os import path


class Map_Tree:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.resource_cooldown = pg.time.get_ticks()
        self.the_rest = 400
        self.the_rest_max = 400
        self.available = True

    def mine(self):
        if self.the_rest > 0 and self.available:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                self.the_rest -= 1
                self.resource_cooldown = now
                self.resource_manager.starting_resources["Wood"] += 1

            return 1
        else:
            self.available = False

    def get_rest(self):
        return self.the_rest


class Map_Rock:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.resource_cooldown = pg.time.get_ticks()
        self.the_rest = 1000
        self.the_rest_max = 1000
        self.available = True

    def mine(self):
        if self.the_rest > 0 and self.available:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                self.the_rest -= 1
                self.resource_cooldown = now
                self.resource_manager.starting_resources["Rock"] += 1

            return 1
        else:
            self.available = False

    def get_rest(self):
        return self.the_rest


class Map_Gold:
    def __init__(self, resource_manager):
        self.resource_manager = resource_manager
        self.resource_cooldown = pg.time.get_ticks()
        self.the_rest = 100
        self.the_rest_max = 100
        self.available = True

    def mine(self):
        if self.the_rest > 0 and self.available:
            now = pg.time.get_ticks()
            if now - self.resource_cooldown > 2000:
                self.the_rest -= 1
                self.resource_cooldown = now
                self.resource_manager.starting_resources["Gold"] += 1

            return 1
        else:
            self.available = False

    def get_rest(self):
        return self.the_rest


class Map_Tile:
    def __init__(self):
        self.the_rest = 0

    def _____(self):
        pass

    def get_rest(self):
        return self.the_rest
