import pygame as pg
from settings import *
import random
import noise
import numpy as np
from os import path
from .buildings import TownCenter, Barracks, Archery
from .units import Archer, Infantryman, Villager
import resource
from .events import *
from .map_resource_class import *


class World:

    # create the dimensions of the world (isometric)
    def __init__(self, resource_manager, entities, gui, grid_size_x, grid_size_y, width, height, events):

        self.resource_manager = resource_manager
        self.entities = entities
        self.gui = gui
        self.grid_size_x = grid_size_x  # number of square in x-dimension
        self.grid_size_y = grid_size_y  # number of square in y-dimension
        self.width = width
        self.height = height

        self.resource = resource

        self.perlin_scale = self.grid_size_x / 2
        self.octave = random.randint(1,20)
        self.modifier = random.randint(10,85)

        self.choosing_pos_x = None
        self.choosing_pos_y = None

        self.grass_tiles = pg.Surface(
            (grid_size_x * TILE_SIZE * 2, grid_size_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()
        # convert_alpha():   change the pixel format of an image including per pixel alphas convert_alpha(Surface) -> Surface convert_alpha() -> Surface
        #                   Creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format
        #                   with per pixel alpha. If no surface is given, the new surface will be optimized for blitting to the current display.
        self.tiles = self.load_images()
        self.world = self.create_world()
        self.collision_matrix = self.create_collision_matrix()

        self.buildings = [[None for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        self.units = [[None for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]

        self.temp_tile = None
        self.examine_tile = None
        self.examine_unit = None

        self.events = events
        # choose Arbre, rock or gold
        self.choose = None

        # self.moving_to_resource = False
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
            self.gui.examined_tile = None
            self.choose = None

        if mouse_action[0]:
            self.examine_unit = None
            self.gui.examined_unit = None

        self.temp_tile = None

        # je vais creer une fonction pour garder cette if-else condition
        if self.gui.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            # print(f"grid_pos(0): {grid_pos[0]}  grid_pos(1): {grid_pos[1]}")
            # on placer gui ici
            if self.can_place_tile(grid_pos):

                # print('placer gui')
                img = self.gui.selected_tile["image"].copy()
                img.set_alpha(100)

                # this if is to avoid the error: "index out of range" when your mouse run out of map
                if grid_pos[0] < self.grid_size_x and grid_pos[1] < self.grid_size_y:
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

                # ce bloc de code sert à construire un bâtiment à un endroit où il n'y a pas de collision
                if mouse_action[0] and not collision:
                    if self.gui.selected_tile["name"] == "TownCenter":
                        ent = TownCenter(render_pos, self.resource_manager, "Blue")
                        self.entities.append(ent)  # On ajoute le bâtiment à la liste des bâtiments
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.gui.selected_tile["name"] == "Barracks":
                        ent = Barracks(render_pos, self.resource_manager, "Blue")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    elif self.gui.selected_tile["name"] == "Archery":
                        ent = Archery(render_pos, self.resource_manager, "Blue")
                        self.entities.append(ent)
                        self.buildings[grid_pos[0]][grid_pos[1]] = ent
                    self.collision_matrix[grid_pos[1]][grid_pos[0]] = 0
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    self.gui.selected_tile = None


        else:
            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            if self.can_place_tile(grid_pos):  # and wood > resource:
                if grid_pos[0] < self.grid_size_x and grid_pos[1] < self.grid_size_y:
                    collision = self.world[grid_pos[0]][grid_pos[1]]["collision"]
                    building = self.buildings[grid_pos[0]][grid_pos[1]]
                    units = self.units[grid_pos[0]][grid_pos[1] - 1]

                    if mouse_action[0] and (
                            building is not None):  # Si on a selectionné un bâtiment avec le clic gauche on affiche
                        self.examine_tile = grid_pos
                        self.gui.examined_tile = building

                    if mouse_action[0] and (
                            units is not None):  # Si on a selectionné une troupe avec le clic gauche on affiche
                        self.examine_unit = grid_pos
                        self.gui.examined_unit = units

                    if mouse_action[
                        0] and collision:  # Si on a selectionné une ressource avec le clic gauche on affiche
                        self.choose = grid_pos
                        self.gui.mining_gui = False
                        self.gui.choose = self.world[grid_pos[0]][grid_pos[1]]

                    if mouse_action[
                        0] and not collision:  # Si on clic gauche dans le vide on ferme tous les interfaces de sélection
                        self.choose = None
                        self.gui.choose = None

                    if mouse_action[2] and collision and (self.gui.examined_unit is not None):  # Si on a sélectionné
                        # une troupe et qu'on clic droit quelque part sur une ressource
                        self.choose = grid_pos  # on choisit la ressource correspondante
                        self.gui.choose = self.world[grid_pos[0]][grid_pos[1]]
                        # self.mining = True  # on active le mode minage
                        self.gui.mining_gui = True  # et on active le gui de minage

                    if self.gui.events.get_troop() is not None:
                        if (self.examine_tile and self.gui.examined_tile) is not None:
                            pos = self.examine_tile
                            pos_x = pos[0]
                            pos_y = pos[1]
                            # ce bloc est la réponse de l'appel de la fonction create_troop dans events en créant la
                            # troupe concernée
                            if self.gui.events.get_troop() == 'archer' and self.resource_manager.is_affordable(
                                    "Archer"):
                                Archer(self.world[pos_x][pos_y], self, self.resource_manager,
                                       self.gui.examined_tile.team)
                                self.examine_tile = None
                                self.gui.events.remise_troop()

                            elif self.gui.events.get_troop() == 'infantryman' and self.resource_manager.is_affordable(
                                    "Infantryman"):
                                Infantryman(self.world[pos_x][pos_y], self, self.resource_manager,
                                            self.gui.examined_tile.team)
                                self.examine_tile = None
                                self.gui.events.remise_troop()

                            elif self.gui.events.get_troop() == 'villager' and self.resource_manager.is_affordable(
                                    "Villager"):
                                Villager(self.world[pos_x][pos_y], self, self.resource_manager,
                                         self.gui.examined_tile.team)
                                self.examine_tile = None
                                self.gui.events.remise_troop()

                        self.gui.events.remise_troop()

                    if self.events.get_grid_pos_unit() and (self.gui.examined_unit is not None):
                        new_unit_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
                        new_unit_pos_world = self.grid_to_world(new_unit_pos[0], new_unit_pos[1])
                        # si on clic droit autre part que sur une ressource:
                        if not collision:  # and new_unit_pos_world["collision"])
                            # self.gui.examined_unit.change_tile(new_unit_pos)
                            self.gui.examined_unit.set_target(new_unit_pos)
                            # print("moving", self.gui.examined_unit.name,"to", new_unit_pos)
                            self.events.remise_moving_troop()
                            self.mining_position = None
                            self.mining = False

                        elif new_unit_pos_world["collision"] and self.gui.examined_unit.name == "Archer":
                            print("j'attaque")

                        # si on clic droit sur une ressource pour la miner avec un villageois:
                        elif self.gui.examined_unit.name == "Villager" and collision:
                            # self.gui.examined_unit.change_tile((new_unit_pos[0]+1,new_unit_pos[1]))
                            new_unit_pos = (new_unit_pos[0] + 1, new_unit_pos[1])
                            self.gui.examined_unit.set_target(new_unit_pos)
                            # print("mining", self.gui.examined_unit.name, "to", new_unit_pos)
                            self.events.remise_moving_troop()
                            # on vérifie qu'on a bien sélectionné une ressource
                            if self.gui.choose is not None:
                                # et qu'elle dispose toujours de ressources
                                if self.gui.choose["class"].available:
                                    self.mining = True
                                    # condition permettant de changer de ressource minée sans que la précédente soit toujours minée
                                    if new_unit_pos != self.mining_position and (self.mining_position is not None):
                                        self.list_mining.remove(self.mined)
                                    self.mined = self.gui.choose

                                    self.events.getting_resource()
                                    # self.moving_to_resource = True
                                    self.mining_position = self.gui.choose
                                    # print("mining pos:", self.mining_position)

                                    self.list_mining.append(self.mined)

                                elif not self.gui.choose["class"].available:
                                    # self.moving_to_resource = False
                                    self.mining = False
                                    self.events.getting_resource()
                                    # condition permettant de vider la variable contenant l'objet ressource miné précédemment (peut être None)
                                    if self.mined in self.list_mining:
                                        self.list_mining.remove(self.mined)
                                    self.mined = None
                                    self.choose = None
                                    self.gui.choose = None
                                    self.mining_position = None
                                    self.gui.mining_gui = False

                    # if self.mining and self.moving_to_resource and self.events.getting_resource:
                    #     self.mined["class"].mine()

                    if self.mining and self.events.getting_resource:
                        for mined in self.list_mining:
                            mined["class"].mine()
                            # pass
                            # on mine la ressource tant que self.mining = True

                    if self.events.update_destroy():
                        # condition qui récupère la variable dans events permettant de savoir si on veut détruire
                        # en gros on supprimer toute trace du bâtiment et on enlève le GUI de ce dernier
                        if self.choosing_pos_x is not None and (self.choosing_pos_y is not None):
                            building = self.buildings[self.choosing_pos_x][self.choosing_pos_y]
                            if building is not None:
                                self.world[self.choosing_pos_x][self.choosing_pos_y]["collision"] = False
                                index = self.entities.index(building)
                                self.examine_tile = None
                                self.gui.examined_tile = None
                                # print(index)
                                self.entities.pop(index)
                                self.buildings[self.choosing_pos_x][self.choosing_pos_y] = None
                                self.events.remise()
                                self.choosing_pos_x, self.choosing_pos_y = None, None

                    # si on clic gauche sur aucun bâtiment on n'affiche plus son GUI
                    elif mouse_action[0] and (building is None):
                        self.choosing_pos_x = None
                        self.choosing_pos_y = None
                        self.examine_tile = None
                        self.gui.examined_tile = None

        for unit in self.list_troop:
            self.gui.health_bar(unit.image, unit)
            if unit.target is not None:
                unit.update()

        for entity in self.entities:
            self.gui.health_bar(entity.image, entity)

    # quand le prog est grandi on doit update plusieurs choses comme heal, shield ou attack point ici
    def draw_mini(self, screen, camera):

        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
                render_pos = self.world[x][y]["render_pos"]
                tile = self.world[x][y]["tile"]
                # minimap here
                minimap_offset = [50, self.height * 0.77 - 20]
                render_pos_mini = self.world[x][y]["render_pos_mini"]
                if tile == "Arbre":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, GREEN, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)
                elif tile == "Carrière de pierre":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, VIOLET, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)
                elif tile == "Or":
                    # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, YELLOW_LIGHT, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)

                elif tile == "Buisson":
                # screen.blit(self.tiles[tile],(render_pos_mini[0],render_pos_mini[1]))
                    pg.draw.circle(screen, PINK, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   1)

                elif self.units[x][y - 1] is not None:
                    # render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7
                    pg.draw.circle(screen, self.units[x][y - 1].team, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   2)
                elif self.buildings[x][y] is not None:
                    pg.draw.circle(screen, self.buildings[x][y].team, (
                        render_pos_mini[0] + TILE_SIZE_MINI_MAP * 51 + minimap_offset[0],
                        render_pos_mini[1] + 50 - TILE_SIZE_MINI_MAP * 7 + minimap_offset[1]),
                                   2)
                mini = self.world[x][y]["iso_poly_mini"]
                mini = [(x + 200 + minimap_offset[0], y + 20 + minimap_offset[1]) for x, y in
                        mini]  # position x + ...., y  + ...
                pg.draw.polygon(screen, MINI_MAP_COLOUR, mini, 1)

    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x, camera.scroll.y))

        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):

                render_pos = self.world[x][y]["render_pos"]
                # conditions pour surligner les objets qu'on sélectionne afin de mieux les voir
                tile = self.world[x][y]["tile"]
                if tile != "" and self.world[x][y]["class"].available:
                    screen.blit(self.tiles[tile],
                                (render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                 render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))
                    if self.choose is not None:
                        if (x == self.choose[0]) and (y == self.choose[1]):
                            mask = pg.mask.from_surface(self.tiles[tile]).outline()
                            mask = [(x + render_pos[0] + self.grass_tiles.get_width() / 2 + camera.scroll.x,
                                     y + render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y)
                                    for x, y in mask]
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
                            self.choosing_pos_x, self.choosing_pos_y = x, y
                            pg.draw.polygon(screen, self.buildings[x][y].team, mask, 2)

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

        for grid_x in range(self.grid_size_x):
            world.append([])
            for grid_y in range(self.grid_size_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"],
                                      (render_pos[0] + self.grass_tiles.get_width() / 2, render_pos[1]))

        return world

    def create_collision_matrix(self):
        collision_matrix = [[1 for x in range(self.grid_size_x)] for y in range(self.grid_size_y)]
        for x in range(self.grid_size_x):
            for y in range(self.grid_size_y):
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
            # (grid_x * TILE_SIZE_MINI_MAP, grid_y*TILE_SIZE_MINI_MAP + 5 * TILE_SIZE_MINI_MAP ), left and top
            # location of every square in mini map
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
        r = random.randint(1, 500)
        # Faire une forêt
        for o in range(10):
            perlin = self.modifier * noise.pnoise2(grid_x / self.perlin_scale, grid_y / self.perlin_scale, octaves=o + 1)


        if perlin < -2.25:
            tile = "Arbre"

        else:
            # Mettre des rochers OU des mines d'or aléatoirement à un taux de 0.8%
            if r <= 4:
                r2 = random.randint(1, 2)
                if r2 == 1:
                    tile = "Or"
                elif r2 == 2:
                    tile = "Carrière de pierre"
            elif 5 <= r <= 15:
                tile = "Buisson"
            # Un arbre isolé sera placé ici à un taux de 10%
            elif r <= 50:
                tile = "Arbre"
            else:
                tile = ""
                # Ne rien mettre sur le block

        # We create the Arbre's object here
        if tile == "Arbre":
            map_resource = Map_Tree(self.resource_manager)
        # We create the rock's object here
        elif tile == "Carrière de pierre":
            map_resource = Map_Rock(self.resource_manager)
        # We create the gold's object here
        elif tile == "Or":
            map_resource = Map_Gold(self.resource_manager)
        # We create the bush's object here
        elif tile == "Buisson":
            map_resource = Map_Bush(self.resource_manager)
        # Tile's Object
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
        Arbre = Tree_img.convert_alpha()
        rock = Rock_img.convert_alpha()
        gold = Gold_img.convert_alpha()  # C'est ici que l'on va lier les entités du jeu à des images (sauf pour les troupes)
        bush = Bush_img.convert_alpha()
        building1 = towncenter.convert_alpha()
        # building2 = lumbermill.convert_alpha()
        building3 = barracks.convert_alpha()
        building4 = archery.convert_alpha()
        images = {
            "building1": building1,
            # "building2": building2,
            "building3": building3,
            "building4": building4,
            "Arbre": Arbre,
            "Carrière de pierre": rock,
            "block": block,
            "Or": gold,
            "Buisson": bush
        }
        return images

    # collision here
    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.gui.resources_rect, self.gui.build_rect, self.gui.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_size_x) and (0 <= grid_pos[1] <= self.grid_size_x)

        if world_bounds and not mouse_on_panel:
            return True
        else:
            return False