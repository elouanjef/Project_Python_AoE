import pygame as pg
from .settings import TILE_SIZE, TILE_SIZE_MINI_MAP
import random
import noise

class World:


    #create the dimensions of the world (isometric)
    def __init__(self, grid_lenght_x, grid_length_y, width, height):
        self.grid_length_x = grid_lenght_x
        self.grid_length_y = grid_length_y
        self.width = width
        self.height = height


        self.perlin_scale = self.grid_length_x/2

        self.grass_tiles = pg.Surface((grid_lenght_x * TILE_SIZE *2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()   
        #convert_alpha():   change the pixel format of an image including per pixel alphas convert_alpha(Surface) -> Surface convert_alpha() -> Surface 
        #                   Creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format
        #                   with per pixel alpha. If no surface is given, the new surface will be optimized for blitting to the current display.
        
        
        self.tiles = self.load_images()
        self.world = self.create_world()


    #create worlds based on created dimensions
    def create_world(self):

        world = []

        for grid_x in range(self.grid_length_x):
            world.append([])
            for grid_y in range(self.grid_length_y):
                world_tile = self.grid_to_world(grid_x, grid_y)
                world[grid_x].append(world_tile)

                render_pos = world_tile["render_pos"]
                self.grass_tiles.blit(self.tiles["block"], (render_pos[0] + self.grass_tiles.get_width()/2, render_pos[1]))

        return world

    
    def grid_to_world(self, grid_x,grid_y):


        #create a square with four vertices and their dimensions
        rect = [
            (grid_x * TILE_SIZE, grid_y*TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE),
            (grid_x * TILE_SIZE + TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE),
            (grid_x * TILE_SIZE, grid_y * TILE_SIZE + TILE_SIZE)
        ]

        rect_mini_map = [
            (grid_x * TILE_SIZE_MINI_MAP, grid_y*TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP)
        ]


        iso_poly = [self.cart_to_iso(x, y) for x,y in rect]

        minx = min([x for x,y in iso_poly])
        miny = min([y for x,y in iso_poly])

        #Choose a random position in map
        r = random.randint(1, 100)

        #make a group of tree --> a forest
        perlin = 100 * noise.pnoise2(grid_x/self.perlin_scale, grid_y/self.perlin_scale)


        if (perlin >= 15) or (perlin <= -35):
            tile = "tree"
        else:
            #isolated tree will appear at a rate of 1%
            if r == 1:
                tile = "tree"
            #Rocks will appear at a rate of 1%
            elif r == 2:
                tile = "rock"
            #Normal block 
            else:
                tile = ""


        #this dict() store all kind of info of all elements in grid
        out = {
            "grid":  [grid_x,grid_y],
            "cart_rect": rect,
            "cart_rect_mini_map": rect_mini_map,
            "iso_poly": iso_poly,
            "render_pos": [minx, miny],
            "tile": tile
        }

        return out


    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = (x+y)/2
        return iso_x, iso_y


    def cart_to_iso(self, x, y):
        iso_x = x - y
        iso_y = ( x + y )/2
        return iso_x,iso_y


    #load our blocks into the game
    def load_images(self):
        block = pg.image.load("assets/graphics/block.png").convert_alpha()
        tree = pg.image.load("assets/graphics/tree.png").convert_alpha()
        rock = pg.image.load("assets/graphics/rock.png").convert_alpha()

        return {"block": block, "tree": tree, "rock": rock}