import pygame as pg
from settings import *
import random
import noise
from os import path
from .buildings import TownCenter, LumberMill, Barracks, Archery
from .units import Archer, Infantryman, Villager
import resource
from .events import *
from .map_resource_class import *
import time


class World:

    # create the dimensions of the world (isometric)
    def __init__(self, resource_manager, entities, hud, grid_lenght_x, grid_length_y, width, height, events):

        self.resource_manager = resource_manager
        self.entities = entities
        self.hud = hud
        self.grid_length_x = grid_lenght_x  # number of square in x-dimension
        self.grid_length_y = grid_length_y  # number of sqaure in y-demension
        self.width = width
        self.height = height

        self.resource = resource

        self.perlin_scale = self.grid_length_x / 2


        self.chossing_pos_x = None
        self.chossing_pos_y = None

        self.grass_tiles = pg.Surface(
            (grid_lenght_x * TILE_SIZE * 2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        # convert_alpha():   change the pixel format of an image including per pixel alphas convert_alpha(Surface) -> Surface convert_alpha() -> Surface
        #                   Creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format
        #                   with per pixel alpha. If no surface is given, the new surface will be optimized for blitting to the current display.
        self.tiles = self.load_images()
        self.world = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.buildings = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        self.units = [[None for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]

        self.temp_tile = None
        self.examine_tile = None
        self.examine_unit = None

        self.events = events
        #choose tree, rock or gold
        self.choose = None

        self.moving_to_resource = False
        self.mining = False
        self.mined = None
        self.mining_position = None
        self.past_mining_pos = None

        self.list_mining = []

        self.list_troop = []


    # work in map
    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()

        if mouse_action[2]:
            self.examine_tile = None
            self.hud.examined_tile = None
            self.choose = None

        if mouse_action[0]:
            self.examine_unit = None
            self.hud.examined_unit = None



        self.temp_tile = None

        # je vais creer une fonction pour garder cette if-else condition
        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            # print(f"grid_pos(0): {grid_pos[0]}  grid_pos(1): {grid_pos[1]}")
            # on placer hud ici
            if self.can_place_tile(grid_pos):

                # print('placer hud')
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)

                # this if is to avoid the error: "index out of range" when your mouse run out of map
                if (grid_pos[0] < self.grid_length_x and grid_pos[1] < self.grid_length_y):
                    render_pos = self.world[grid_pos[0]][grid_pos[1]].get("render_pos")
                    iso_poly = self.world[grid_pos[0]][grid_pos[1]]["iso_poly"]
                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                    self.temp_tile = {
                        "image": img,
                        "render_pos": render_pos,
                        "iso_poly": iso_poly,
                        "collision": collision
                    }
                else:
                    pass

                # left-click to build
                if mouse_action[0] and not collision:
                    if self.hud.selected_tile["name"] == "TownCenter":
                        ent = TownCenter(render_pos, self.resource_manager, "Blue")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "LumberMill":
                        ent = LumberMill(render_pos, self.resource_manager, "Blue")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "Barracks":
                        ent = Barracks(render_pos, self.resource_manager, "Blue")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.hud.selected_tile["name"] == "Archery":
                        ent = Archery(render_pos, self.resource_manager, self.world, "Blue")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    self.collision_matrix[grid_pos[1]][grid_pos[0]] = 0
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.hud.selected_tile = None


        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if self.can_place_tile(grid_pos):  # and wood > resource:
                if (grid_pos[0] < self.grid_length_x and grid_pos[1] < self.grid_length_y):
                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                    building = self.buildings[grid_pos[0]][grid_pos[1]]
                    units = self.units[grid_pos[0]][grid_pos[1]-1]


                    if mouse_action[0] and (building is not None):
                        self.examine_tile = grid_pos
                        self.hud.examined_tile = building

                    if mouse_action[0] and (units is not None):
                        self.examine_unit = grid_pos
                        self.hud.examined_unit = units


                    if mouse_action[0] and collision:
                        #print(f'{grid_pos}')
                        self.choose = grid_pos
                        self.hud.mining_hud = False
                        self.hud.choose = self.world[grid_pos[0]][grid_pos[1]]

                    if mouse_action[0] and not collision:
                        self.choose = None
                        self.hud.choose = None

                    if mouse_action[2] and collision and (self.hud.examined_unit is not None):
                        self.choose = grid_pos
                        self.hud.choose = self.world[grid_pos[0]][grid_pos[1]]
                        self.mining = True
                        self.hud.mining_hud = True

                    if self.hud.events.get_troop() != None:
                        if self.examine_tile != None:
                            pos = self.examine_tile
                            pos_x = pos[0]
                            pos_y = pos[1]

                            if self.hud.events.get_troop() == 'archer':
                                #archer = Archer(self.world[pos_x][pos_y], self, self.resource_manager)
                                #archer.target = pos
                                Archer(self.world[pos_x][pos_y], self, self.resource_manager)
                                self.examine_tile = None
                                self.hud.events.remise_troop()
                                #self.list_troop.append(archer)

                            elif self.hud.events.get_troop() == 'infantryman':
                                #infantryman=Infantryman(self.world[pos_x][pos_y], self, self.resource_manager)
                                #infantryman.target = pos
                                Infantryman(self.world[pos_x][pos_y], self, self.resource_manager)
                                self.examine_tile = None
                                self.hud.events.remise_troop()
                                #self.list_troop.append(infantryman)

                            elif self.hud.events.get_troop() == 'villager':
                                #villager=Villager(self.world[pos_x][pos_y], self, self.resource_manager)
                                #villager.target = pos
                                Villager(self.world[pos_x][pos_y], self, self.resource_manager)
                                self.examine_tile = None
                                self.hud.events.remise_troop()
                                #self.list_troop.append(villager)

                        self.hud.events.remise_troop()


                    if self.events.get_grid_pos_unit() and (self.hud.examined_unit is not None):
                        if not collision:
                            new_unit_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                            #self.hud.examined_unit.change_tile(new_unit_pos)
                            self.hud.examined_unit.set_target(new_unit_pos)
                            #print("moving", self.hud.examined_unit.game_name,"to", new_unit_pos)
                            self.events.remise_moving_troop()
                            self.mining_position = None
                            self.mining = False
            

                        elif (self.hud.examined_unit.game_name == "Villager"):  #je voulais mettre game_name = "Villager" mais je n'arrive pas à créer de villager
                            new_unit_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                            #self.hud.examined_unit.change_tile((new_unit_pos[0]+1,new_unit_pos[1]))
                            new_unit_pos = (new_unit_pos[0]+1, new_unit_pos[1])
                            self.hud.examined_unit.set_target(new_unit_pos)
                            #print("mining", self.hud.examined_unit.game_name, "to", new_unit_pos)
                            self.events.remise_moving_troop()

                            if self.hud.choose is not None:
                                if self.hud.choose["class"].available:

                                    self.mining = True
                                    if new_unit_pos != self.mining_position and (self.mining_position is not None):
                                        self.list_mining.remove(self.mined)
                                    self.mined = self.hud.choose

                                    self.events.getting_resource()
                                    self.moving_to_resource = True
                                    self.mining_position = self.hud.choose["grid"]
                                    #print("mining pos:", self.mining_position)

                                    self.list_mining.append(self.mined)

                                elif not self.hud.choose["class"].available:
                                    self.moving_to_resource = False
                                    self.mining = False
                                    self.events.getting_resource()
                                    if self.mined in self.list_mining:
                                        self.list_mining.remove(self.mined)
                                    self.mined = None
                                    self.choose = None
                                    self.hud.choose = None
                                    self.mining_position = None
                                    self.hud.mining_hud = False



                    # if self.mining and self.moving_to_resource and self.events.getting_resource:
                    #     self.mined["class"].mine()
                    

                    if self.mining and self.moving_to_resource and self.events.getting_resource:
                        for mined in self.list_mining:
                            mined["class"].mine()




                    if self.events.update_destroy():
                        if (self.chossing_pos_x != None  and self.chossing_pos_y != None):
                            building = self.buildings[self.chossing_pos_x][self.chossing_pos_y]
                            if building is not None:
                                self.world[self.chossing_pos_x][self.chossing_pos_y]["collision"] = False
                                index = self.entities.index(building)
                                self.examine_tile = None
                                self.hud.examined_tile = None
                                #print(index)
                                self.entities.pop(index)
                                self.buildings[self.chossing_pos_x][self.chossing_pos_y] = None
                                self.events.remise()
                                self.chossing_pos_x, self.chossing_pos_y = None, None

                    elif mouse_action[0] and (building is None):
                        self.chossing_pos_x = None
                        self.chossing_pos_y = None
                        self.examine_tile = None
                        self.hud.examined_tile = None

        for unit in self.list_troop:
            if unit.target != None:
                unit.update()
            




    # quand le prog est grandi on doit update plusieuse choses comme heal, shield ou attack point ici
    def is_next_to(self, pos1, pos2):
        return ((pos1[0]-1 == pos2[0] and pos1[1] == pos2[1])
                or (pos1[0]+1 == pos2[0] and pos1[1] == pos2[1])
                or (pos1[0] == pos2[0] and pos1[1]-1 == pos2[1])
                or (pos1[0] == pos2[0] and pos1[1]+1 == pos2[1]))

    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        # draw coordinate lines
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                
                render_pos = self.world[x][y]["render_pos"]
                # create the other world's object
                tile = self.world[x][y]["tile"]
                if tile != "" and self.world[x][y]["class"].available:
                    screen.blit(self.tiles[tile],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.choose is not None:
                        if (x == self.choose[0]) and (y == self.choose[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                                     y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y) for x, y in mask]
                            pg.draw.polygon(screen, (255, 255, 255), mask, 3)

                units = self.units[x][y]
                if units is not None:
                    screen.blit(units.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (units.image.get_height() - TILE_SIZE) + camera.scroll.y))

                building = self.buildings[x][y]
                if building is not None:

                    screen.blit(building.image,
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y))

                    if self.examine_tile is not None:
                        if (x == self.examine_tile[0]) and (y == self.examine_tile[1]):
                            mask = pg.mask.from_surface(building.image).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (building.image.get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
                            self.chossing_pos_x, self.chossing_pos_y = x, y
                            pg.draw.polygon(screen, GREEN, mask, 2)


                #minimap here
                render_pos_mini = self.world[x][y]["render_pos_mini"]
                if tile == "tree":
                    #screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, MARRON,(render_pos_mini[0] + TILE_SIZE_MINI_MAP*51,render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP*7), 1)
                elif tile == "rock":
                    #screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, VIOLET,(render_pos_mini[0] + TILE_SIZE_MINI_MAP*51,render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP*7), 1)
                elif self.units[x][y-1] != None:
                    pg.draw.circle(screen, WHITE,(render_pos_mini[0] + TILE_SIZE_MINI_MAP*51,render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP*7), 1)
                elif self.buildings[x][y] != None:
                    pg.draw.circle(screen, GREEN,(render_pos_mini[0] + TILE_SIZE_MINI_MAP*51,render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP*7), 1)
                mini = self.world[x][y]["iso_poly_mini"]
                mini = [(x + 200, y + 20) for x, y in mini]  # position x + ...., y  + ...
                pg.draw.polygon(screen, MINI_MAP_COLOUR, mini, 1)


        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width() / 2 + camera.scroll.x, y + camera.scroll.y) for x, y in
                        iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, RED, iso_poly, 3)
            else:
                pg.draw.polygon(screen, WHITE, iso_poly, 3)

            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )

    # create worlds based on created dimensions
    def create_world(self):

        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"],
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

        return world

    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range(self.grid_length_x)] for y in range(self.grid_length_y)]
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):
                if self.world[x][y]["collision"]:
                    collision_matrix[y][x] = 0
        return collision_matrix

    def grid_to_world(self, grid_x, grid_y):

        # create a square with four vertices and their dimensions
        rect = [
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        rect_mini_map = [
            (grid_x * TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP),
            # (grid_x * TILE_SIZE_MINI_MAP, grid_y*TILE_SIZE_MINI_MAP + 5 * TILE_SIZE_MINI_MAP ),                      #left and top location of every square in mini map
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP)
        ]

        iso_poly = [self.cart_to_iso(x, y) for x, y in rect]
        iso_poly_mini = [self.cart_to_iso(x, y) for x, y in rect_mini_map]

        minx = min([x for x, y in iso_poly])
        miny = min([y for x, y in iso_poly])

        minx_mini = min([x for x, y in iso_poly_mini])
        miny_mini = min([y for x, y in iso_poly_mini])


        # create a random map
        # Choose a random position in map
        r = random.randint(1, 100)

        # make a group of tree --> a forest
        perlin = 20 * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale)

        if (perlin >= 15) or (perlin <= -35):
            tile = "tree"
        else:
            # isolated tree will appear at a rate of 1%
            if r == 1:
                tile = "tree"
            # Rocks will appear at a rate of 1%
            elif r == 2:
                tile = "rock"
            # Normal block
            elif r == 3:
                tile = "gold"
            else:
                tile = ""



        #We create the tree's object here
        if (tile == "tree"):
            map_resource = Map_Tree(self.resource_manager)
        #We create the rock's object here
        elif (tile == "rock"):
            map_resource = Map_Rock(self.resource_manager)
        #We create the gold's object here
        elif (tile == "gold"):
            map_resource = Map_Gold(self.resource_manager)
        #Tile's Object
        else:
            map_resource = Map_Tree(self.resource_manager)
        # this dict() store all kind of info of all elements in grid
        out = {
            "grid": [grid_x, grid_y],
            "cart_rect": rect,  # square map
            "cart_rect_mini_map": rect_mini_map,  # square mini map
            "iso_poly": iso_poly,  # iso_poly map
            "iso_poly_mini": iso_poly_mini,  # isopoly minimap
            "render_pos": [minx, miny],
            "render_pos_mini": [minx_mini, miny_mini],
            "tile": tile,
            "collision": False if tile == "" else True,
            "class": map_resource
        }

        return out

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x + y) / 2
        return iso_x, iso_y

    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width() / 2
        world_y = y - scroll.y
        # transform to card (inverse of card_to_iso)
        card_y = (2 * world_y - world_x) / 2
        card_x = card_y + world_x
        # transform to grid coordinates
        grid_x = int(card_x // TILE_SIZE)
        grid_y = int(card_y // TILE_SIZE)
        return grid_x, grid_y

    # load our blocks into the game
    def load_images(self):
        block = Block_img.convert_alpha()
        # tree = pg.image.load(path.join(graphics_folder, "tree.png")).convert_alpha()
        tree = Tree_img.convert_alpha()
        #rock = pg.image.load(path.join(graphics_folder, "rock.png")).convert_alpha()
        rock = Rock_img.convert_alpha()
        gold = Gold_img.convert_alpha()
        building1 = towncenter.convert_alpha()
        building2 = lumbermill.convert_alpha()
        building3 = barracks.convert_alpha()
        building4 = archery.convert_alpha()
        troop = pg.image.load(path.join(graphics_folder, "cart_E.png")).convert_alpha()
        images = {
            "building1": building1,
            "building2": building2,
            "building3": building3,
            "building4": building4,
            "tree": tree,
            "rock": rock,
            "block": block,
            "gold": gold,
            "troop": troop
        }
        return images

    # colision here
    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False