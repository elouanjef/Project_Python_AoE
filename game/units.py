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

#bug of map edges
class Archer:

    def __init__(self, tile, world, resource_manager):
        image = archer
        self.world = world
        self.tile = tile
        self.image = image
        self.name = "Archer"
        self.game_name = "Archer"
        self.attack = 5
        self.resource_manager = resource_manager
        self.resource_manager.buy(self.game_name)
        self.health = 35
        self.health_max = 35

        self.world.units[tile["grid"][0]][tile["grid"][1]] = self
        self.world.list_troop.append(self)
        self.path_index = 0
        self.move_timer = pg.time.get_ticks()

        self.target = None

        self.previous_time = 0

        self.velocity_inverse = 100  #(miniseconde par carré)

        self.team = "Blue"  #blue team is the player's team




    def get_health(self):
        return self.health

    def change_tile(self, pos):
        x = pos[0] 
        y = pos[1] 
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]
        #print(f'pos = {self.tile["grid"][0]}___{self.tile["grid"][1]}')

    def create_path(self,pos):
        searching_for_path = True
        while searching_for_path:
            x = pos[0]
            y = pos[1] - 1
            dest_tile = self.world.world[x][y]

            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x,y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False
    def set_target(self, pos):
        self.target = pos

    def update(self):
        temps_temp = pg.time.get_ticks()
        temps = temps_temp  - self.previous_time
        if temps > self.velocity_inverse:
            if self.target != None:
                self.create_path(self.target)
                
                if [self.tile["grid"][0],self.tile["grid"][1]] == self.path[-1] :
                    #print(f'target is {self.target}')
                    self.target = None
                    #print('reach')
                else:
                    try:
                        if len(self.path) > 1:
                            new_pos = self.path[1]
                            self.change_tile(new_pos)
                            #print(self.path)
                    except IndexError:
                        #print("########")
                        #print(f'path_index {self.path_index}')
                        #print(f'path: {self.path}')
                        #print(f'len_path:  {len(self.path)}')
                        #print("########")
                        pass
        if temps > self.velocity_inverse:
            self.previous_time = temps_temp
        #print(f'temps:======{temps}')
        #print(f'temps_temp:======{temps_temp}')

        


class Villager:

    def __init__(self, tile, world, resource_manager):
        image = villager
        self.world = world
        #        self.world.entities.append(self)
        self.tile = tile
        self.image = image
        self.name = "Villager"
        self.game_name = "Villageois"
        self.attack = 1
        self.resource_manager = resource_manager
        self.resource_manager.buy(self.game_name)
        self.health = 20
        self.health_max = 20

        self.world.units[tile["grid"][0]][tile["grid"][1]] = self
        self.world.list_troop.append(self)
        self.path_index = 0
        self.move_timer = pg.time.get_ticks()
        self.in_work = False
        self.target = None
        self.previous_time = 0

        self.velocity_inverse = 200

        self.team = "Blue"

    def get_health(self):
        return self.health

    def change_tile(self, pos):
        x = pos[0] 
        y = pos[1] 
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]
        #print(f'pos = {self.tile["grid"][0]}___{self.tile["grid"][1]}')

    def create_path(self,pos):
        searching_for_path = True
        while searching_for_path:
            x = pos[0]
            y = pos[1] - 1
            dest_tile = self.world.world[x][y]

            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x,y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False

    def set_target(self, pos):
        self.target = pos

    def update(self):
        temps_temp = pg.time.get_ticks()
        temps = temps_temp  - self.previous_time
        if temps > self.velocity_inverse:
            if self.target != None:
                self.create_path(self.target)
                
                if [self.tile["grid"][0],self.tile["grid"][1]] == self.path[-1] :
                    #print(f'target is {self.target}')
                    self.target = None
                    #print('reach')
                else:
                    try:
                        if len(self.path) > 1:
                            new_pos = self.path[1]
                            self.change_tile(new_pos)
                            #print(self.path)
                    except IndexError:
                        print("########")
                        print(f'path_index {self.path_index}')
                        print(f'path: {self.path}')
                        print(f'len_path:  {len(self.path)}')
                        print("########")
        if temps > self.velocity_inverse:
            self.previous_time = temps_temp
        #print(f'temps:======{temps}')
        #print(f'temps_temp:======{temps_temp}')

class Infantryman:

    def __init__(self, tile, world, resource_manager):
        image = infantryman
        self.world = world
        self.world.entities.append(self)
        self.tile = tile
        self.image = image
        self.name = "Infantryman"
        self.game_name = "Barbare"
        self.resource_manager = resource_manager
        self.resource_manager.buy(self.game_name)
        self.health = 50
        self.health_max = 50

        self.world.units[tile["grid"][0]][tile["grid"][1]] = self
        self.world.list_troop.append(self)
        self.path_index = 0
        self.move_timer = pg.time.get_ticks()

        self.target = None
        self.previous_time = 0

        self.velocity_inverse = 300
        self.previous_time = 0

        self.team = "Blue"


    def get_health(self):
        return self.health

    def change_tile(self, pos):
        x = pos[0] 
        y = pos[1] 
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]
        #print(f'pos = {self.tile["grid"][0]}___{self.tile["grid"][1]}')

    def create_path(self,pos):
        searching_for_path = True
        while searching_for_path:
            x = pos[0]
            y = pos[1] - 1
            dest_tile = self.world.world[x][y]

            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x,y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False
    def set_target(self, pos):
        self.target = pos

    def update(self):
        temps_temp = pg.time.get_ticks()
        temps = temps_temp  - self.previous_time
        if temps > self.velocity_inverse:
            if self.target != None:
                self.create_path(self.target)
                
                if [self.tile["grid"][0],self.tile["grid"][1]] == self.path[-1] :
                    #print(f'target is {self.target}')
                    self.target = None
                    #print('reach')
                else:
                    try:
                        if len(self.path) > 1:
                            new_pos = self.path[1]
                            self.change_tile(new_pos)
                            #print(self.path)
                    except IndexError:
                        print("########")
                        print(f'path_index {self.path_index}')
                        print(f'path: {self.path}')
                        print(f'len_path:  {len(self.path)}')
                        print("########")
        if temps > self.velocity_inverse:
            self.previous_time = temps_temp
        #print(f'temps:======{temps}')
        #print(f'temps_temp:======{temps_temp}')

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

        self.target = None

        self.velocity_inverse = 50
        self.previous_time = 0

        self.team = "Blue"


    def change_tile(self, pos):
        x = pos[0] 
        y = pos[1] 
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]
        print(f'pos = {self.tile["grid"][0]}___{self.tile["grid"][1]}')

    def create_path(self,pos):
        searching_for_path = True
        while searching_for_path:
            x = pos[0]
            y = pos[1] - 1
            dest_tile = self.world.world[x][y]

            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x,y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False
    def set_target(self, pos):
        self.target = pos

    def update(self):
        temps_temp = pg.time.get_ticks()
        temps = temps_temp  - self.previous_time
        if temps > self.velocity_inverse:
            if self.target != None:
                self.create_path(self.target)
                
                if [self.tile["grid"][0],self.tile["grid"][1]] == self.path[-1] :
                    print(f'target is {self.target}')
                    self.target = None
                    print('reach')
                else:
                    try:
                        if len(self.path) > 1:
                            new_pos = self.path[1]
                            self.change_tile(new_pos)
                            print(self.path)
                    except IndexError:
                        print("########")
                        print(f'path_index {self.path_index}')
                        print(f'path: {self.path}')
                        print(f'len_path:  {len(self.path)}')
                        print("########")
        if temps > self.velocity_inverse: 
            self.previous_time = temps_temp
        print(f'temps:======{temps}')
        print(f'temps_temp:======{temps_temp}')


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

        self.target = None

        self.velocity_inverse = 200
        self.previous_time = 0

        self.team = "Blue"

    def change_tile(self, pos):
        x = pos[0] 
        y = pos[1] 
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]
        print(f'pos = {self.tile["grid"][0]}___{self.tile["grid"][1]}')

    def create_path(self,pos):
        searching_for_path = True
        while searching_for_path:
            x = pos[0]
            y = pos[1] - 1
            dest_tile = self.world.world[x][y]

            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x,y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False
    def set_target(self, pos):
        self.target = pos

    def update(self):
        temps_temp = pg.time.get_ticks()
        temps = temps_temp  - self.previous_time
        if temps > self.velocity_inverse:
            if self.target != None:
                self.create_path(self.target)
                
                if [self.tile["grid"][0],self.tile["grid"][1]] == self.path[-1] :
                    print(f'target is {self.target}')
                    self.target = None
                    print('reach')
                else:
                    try:
                        if len(self.path) > 1:
                            new_pos = self.path[1]
                            self.change_tile(new_pos)
                            print(self.path)
                    except IndexError:
                        print("########")
                        print(f'path_index {self.path_index}')
                        print(f'path: {self.path}')
                        print(f'len_path:  {len(self.path)}')
                        print("########")
        if temps > self.velocity_inverse:
            self.previous_time = temps_temp
        print(f'temps:======{temps}')
        print(f'temps_temp:======{temps_temp}')





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