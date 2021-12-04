import pygame as pg
from settings import *
from game.world import *
from os import path



class Map_Tree:
    def __init__(self):
        self.the_rest = 1000

    def couper(self):
        self.the_rest -= 50
        return 50
    def get_rest(self):
        return self.the_rest

class Map_Rock:
    def __init__(self):
        self.the_rest = 1000

    def miner(self):
        self.the_rest -= 10
        return 10
    def get_rest(self):
        return self.the_rest

class Map_Tile:
    def __init__(self):
        self.the_rest = 0
    def _____(self):
        pass
    def get_rest(self):
        return self.the_rest
