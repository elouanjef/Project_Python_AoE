import time
import pygame as pg
from settings import *
from os import path
#from units import *
from game.resource import *
# from tqdm import tqdm

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import random

class Archer:

    def __init__(self, tile, world, resource_manager):
        image = archer
        self.world = world
#        self.world.entities.append(self)
        self.tile = tile
        self.image = image
        self.name = "Archer"
        self.game_name = "Archer"
        self.attack = 5
        #self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
         #self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
       # self.resource_manager = resource_manager
       # self.resource_manager.cost_to_resource(self.name)
        self.health = 35

        self.world.units[tile["grid"][0]][tile["grid"][1]] = self
        self.move_timer = pg.time.get_ticks()

    def get_health(self):
        return self.health

    def change_tile(self, pos):
        x = pos[0]
        y = pos[1] - 1
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]

    def create_path(self, new_tile):
        searching_for_path = True
        while searching_for_path:
            x = new_tile[0]
            y = new_tile[1]
            dest_tile = self.world.world[x][y]
            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x, y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path_index = 0
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False

    def change_tile2(self, new_tile):
        self.world.archer[self.tile["grid"][0][self.tile["grid"][1]]] = None
        self.world.archer[new_tile[0]][new_tile[1]] = self
        self.tile = self.world.world[new_tile[0][new_tile][1]]

    def update(self):
        now = pg.time.get_ticks()
        """if now - self.move_timer > 1000:
            new_pos = self.path[self.path_index]
            self.change_tile2(new_pos)
            self.path_index += 1
            self.move_timer = now
            if self.path_index == len(self.path) - 1:
                self.create_path()"""
        #on pourra mettre ici attaquer, perdre de la vie etc..

class Villager:

    def __init__(self, tile, world, resource_manager):
        image = villager
        self.world = world
        #        self.world.entities.append(self)
        self.tile = tile
        self.image = image
        self.name = "Villager"
        self.game_name = "Villager"
        self.attack = 1
        # self.rect = self.image.get_rect(topleft=pos)
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
        # self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        # self.resource_manager = resource_manager
        # self.resource_manager.cost_to_resource(self.name)
        self.health = 20

        self.world.units[tile["grid"][0]][tile["grid"][1]] = self
        self.move_timer = pg.time.get_ticks()

    def get_health(self):
        return self.health

    def change_tile(self, pos):
        x = pos[0]
        y = pos[1] - 1
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]

class Infantryman:

    def __init__(self, tile, world, resource_manager):
        image = infantryman
        self.world = world
        self.world.entities.append(self)
        self.tile = tile
        self.image = image
        self.name = "Infantryman"
        self.game_name = "Infantryman"
        self.resource_manager = resource_manager
        self.resource_manager.cost_to_resource(self.name)
         #self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
       # self.resource_manager = resource_manager
       # self.resource_manager.cost_to_resource(self.name)
        self.health = 50

        self.world.units[tile["grid"][0]][tile["grid"][1]] = self
        self.move_timer = pg.time.get_ticks()


    def get_health(self):
        return self.health

    def change_tile(self, pos):
        x = pos[0]
        y = pos[1]-1
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]

    def update(self):
        now = pg.time.get_ticks()

class Cavalry:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "unit04.png"))
        self.image = image
        self.name = "Cavalry"
        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.attack = 8
        self.range = 0
        self.res = [0, 0, 80, 70]
        self.health = 150

    def update(self):
        if self.health != 0:
            self.health -= 1

class Catapult:

    def __init__(self, pos):
        image = pg.image.load(path.join(graphics_folder, "unit05.png"))
        self.image = image
        self.name = "Catapult"

        self.rect = self.image.get_rect(topleft=pos)
        # [ WOOD , ROCK , GOLD , FOOD ]
        self.attack = 60
        self.range = 12
        self.res = [180, 0, 80, 0]
        self.health = 75

    def update(self):
        if self.health != 0:
            self.health -= 1

#Pour l'instant j'ai mis unit0?.png pour le sprite de chaque unité, il faudra renommer les sprites de cette manière.






class Unite:
    batiment = False
    soldat = False
    villageois = False
    alive = False
    type = False
    name = False
    res = [0, 0, 0, 0]

    def __init__(self, name, type):
        self.name = name
        self.type = type
        if str(self.type) in ("cavalerie", "infanterie", "artillerie"):
            self.soldat = True
            self.alive = True
        elif str(self.type) in ("batiment"):
            self.batiment = True
            self.alive = True
        elif str(self.type) in ("villageois"):
            self.villageois = True
            self.alive = True
        else:
            print("Il faut choisir un type valable")


def militaire(nb, troop, type, res, t):
    # test_resource(res)
    armee = {}
    for i in range(nb):
        time.sleep(t)
        armee[i] = Unite(troop, type)
        print("Vous avez enrôlé", i + 1, str(troop), "de type", str(type), "pour", res[0], "de bois",
              res[1], "de pierre", res[2], "d'or et", res[3], "de nourriture")
    return armee


def villager_test(nb):
    # test_resource(res)
    villageois = {}
    res = [0, 0, 0, 50]
    for i in range(nb):
        time.sleep(3)
        villageois[i] = Unite("villageois", "villageois")
        print("Villageois créé pour", res[3], "de nourriture")
    return villageois


def construire(name, res, t):
    # test_resource(res)
    time.sleep(t)
    construction = Unite(name, 'batiment')
    print("Vous avez bâti un(e)", str(name), "pour", res[0], "de bois",
          res[1], "de pierre", res[2], "d'or et", res[3], "de nourriture")
    return construction


# [ WOOD , ROCK , GOLD , FOOD ]
units_res = {
    # caserne
    'archer': [0, 0, 30, 20],
    'arbaletrier': [0, 0, 20, 45],
    'piquier': [30, 0, 0, 30],
    'fantassin': [25, 0, 35, 0],

    # usine
    'canon_lourd': [150, 0, 80, 0],
    'couleuvrine': [200, 0, 80, 0],

    # ecurie
    'chevalier': [0, 0, 100, 75],
    'uhlan': [0, 0, 75, 60],

    # batiments
    'centre_ville': [600, 0, 0, 0],
    'caserne': [150, 0, 0, 0],
    'usine': [200, 0, 0, 0],
    'moulin': [150, 0, 0, 0],
    'ecurie': [175, 0, 0, 0],
    'plantation': [800, 0, 0, 0]
}

units_time = {
    # caserne
    'archer': 3,
    'arbaletrier': 3,
    'piquier': 4,
    'fantassin': 5,

    # usine
    'canon_lourd': 30,
    'couleuvrine': 30,

    # ecurie
    'chevalier': 12,
    'uhlan': 10,

    # batiments
    'centre_ville': 60,
    'caserne': 40,
    'usine': 40,
    'moulin': 30,
    'ecurie': 40,
    'plantation': 30
}

units_age = {
    # caserne
    'archer': 1,
    'arbaletrier': 1,
    'piquier': 1,
    'fantassin': 2,

    # usine
    'canon_lourd': 2,
    'couleuvrine': 2,

    # ecurie
    'chevalier': 2,
    'uhlan': 1,

    # batiments
    'centre_ville': 1,
    'caserne': 1,
    'usine': 2,
    'moulin': 1,
    'ecurie': 1,
    'plantation': 2
}


def caserne(nb, troop):
    militaire(nb, troop, 'infanterie', units_res[str(troop)], units_time[str(troop)])


def usine(nb, troop):
    militaire(nb, troop, 'artillerie', units_res[str(troop)], units_time[str(troop)])


def ecurie(nb, troop):
    militaire(nb, troop, 'cavalerie', units_res[str(troop)], units_time[str(troop)])


def batiment(nom):
    construire(nom, units_res[str(nom)], units_time[str(nom)])

"""
caserne(1, "archer")

ecurie(1, 'uhlan')

batiment('moulin')

usine(1, 'canon_lourd')

villager(3)
"""