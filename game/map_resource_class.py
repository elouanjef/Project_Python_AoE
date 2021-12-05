import pygame as pg
from settings import *
from game.world import *
from os import path



class Map_Tree:
    def __init__(self):
        self.the_rest = 1000

    def mine(self):
        self.the_rest -= 5
        return 5
    def get_rest(self):
        return self.the_rest

class Map_Rock:
    def __init__(self):
        self.the_rest = 1000

    def mine(self):
        self.the_rest -= 1
        return 1
    def get_rest(self):
        return self.the_rest

class Map_Tile:
    def __init__(self):
        self.the_rest = 0
    def _____(self):
        pass
    def get_rest(self):
        return self.the_rest
