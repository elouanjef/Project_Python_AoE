import time
import pygame as pg
from settings import *
from os import path
# from units import *
from game.resource import *
# from tqdm import tqdm

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


class Unit:

    def __init__(self, tile, world, resource_manager, team):
        self.world = world
        self.tile = tile
        self.team = team  # blue team is the player's team
        self.attack = 5
        self.resource_manager = resource_manager

        self.resource_manager.buy(self)

        self.health = 35
        self.health_max = 35
        self.health_bar_length = HEALTH_BAR_LENGTH
        self.health_ratio = self.health_max / self.health_bar_length

        self.world.units[tile["grid"][0]][tile["grid"][1]] = self
        self.world.list_troop.append(self)
        self.path_index = 0
        self.move_timer = pg.time.get_ticks()

        self.target = None

        self.previous_time = 0

    def get_health(self, type):
        if type == 'current':
            return self.health
        elif type == 'max':
            return self.health_max

    def change_tile(self, pos):
        x = pos[0]
        y = pos[1]
        self.world.units[self.tile["grid"][0]][self.tile["grid"][1]] = None
        self.world.units[x][y] = self
        self.tile = self.world.world[x][y]

    def create_path(self, pos):
        searching_for_path = True
        while searching_for_path:
            x = pos[0]
            y = pos[1] - 1
            dest_tile = self.world.world[x][y]

            if not dest_tile["collision"]:
                self.grid = Grid(matrix=self.world.collision_matrix)
                self.start = self.grid.node(self.tile["grid"][0], self.tile["grid"][1])
                self.end = self.grid.node(x, y)
                finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
                self.path, runs = finder.find_path(self.start, self.end, self.grid)
                searching_for_path = False

    def set_target(self, pos):
        self.target = pos

    def update(self):
        temps_temp = pg.time.get_ticks()
        temps = temps_temp - self.previous_time
        if temps > self.velocity_inverse:
            if self.target is not None:
                self.create_path(self.target)

                if [self.tile["grid"][0], self.tile["grid"][1]] == self.path[-1]:
                    self.target = None
                else:
                    try:
                        if len(self.path) > 1:
                            new_pos = self.path[1]
                            self.change_tile(new_pos)
                    except IndexError:
                        pass
        if temps > self.velocity_inverse:
            self.previous_time = temps_temp


class Archer(Unit):
    image = archer
    name = "Archer"
    game_name = "Archer"
    health = 35
    health_max = 35
    attack = 5
    velocity_inverse = 100


class Villager(Unit):
    image = villager
    name = "Villager"
    game_name = "Villageois"
    health = 20
    health_max = 20
    attack = 1
    velocity_inverse = 200


class Infantryman(Unit):
    image = infantryman
    name = "Infantryman"
    game_name = "Barbare"
    health = 50
    health_max = 50
    attack = 7
    velocity_inverse = 300
