import pygame as pg
from settings import RED, TILE_SIZE, TILE_SIZE_MINI_MAP,BLUE, WHITE ,graphics_folder
import random
import noise
from os import path 

class World:


    #create the dimensions of the world (isometric)
    def __init__(self, hud,grid_lenght_x, grid_length_y, width, height):
        self.hud = hud
        self.grid_length_x = grid_lenght_x    #number of square in x-dimension   
        self.grid_length_y = grid_length_y    #number of sqaure in y-demension
        self.width = width
        self.height = height


        self.perlin_scale = self.grid_length_x/2

        self.grass_tiles = pg.Surface((grid_lenght_x * TILE_SIZE *2, grid_length_y * TILE_SIZE + 2 * TILE_SIZE)).convert_alpha()   
        #convert_alpha():   change the pixel format of an image including per pixel alphas convert_alpha(Surface) -> Surface convert_alpha() -> Surface 
        #                   Creates a new copy of the surface with the desired pixel format. The new surface will be in a format suited for quick blitting to the given format
        #                   with per pixel alpha. If no surface is given, the new surface will be optimized for blitting to the current display.
        
        
        self.tiles = self.load_images()
        self.world = self.create_world()

        self.temp_tile = None







    #work in map
    def update(self, camera):
        mouse_pos = pg.mouse.get_pos()
        mouse_action = pg.mouse.get_pressed()
        self.temp_tile = None


        #je vais creer une fonction pour garder cette if-else condition
        if self.hud.selected_tile is not None:

            grid_pos = self.mouse_to_grid(mouse_pos[0], mouse_pos[1], camera.scroll)
            #print(f"grid_pos(0): {grid_pos[0]}  grid_pos(1): {grid_pos[1]}")
            #on placer hud ici
            if self.can_place_tile(grid_pos):
            
                #print('placer hud')
                img = self.hud.selected_tile["image"].copy()
                img.set_alpha(100)






                #this if is to avoid the error: "index out of range" when your mouse run out of map 
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


                #left-click to build
                if mouse_action[0] and not collision:
                    #print('Placed')
                    self.world[grid_pos[0]][grid_pos[1]]["tile"] = self.hud.selected_tile["name"]
                    #print('1')
                    self.world[grid_pos[0]][grid_pos[1]]["collision"] = True
                    #print('2')
                    self.hud.selected_tile = None
                    #print('termine')




    #quand le prog est grandi on doit update plusieuse choses comme heal, shield ou attack point ici






    def draw(self, screen, camera):

        screen.blit(self.grass_tiles, (camera.scroll.x,camera.scroll.y))

        #draw coordinate lines 
        for x in range(self.grid_length_x):
            for y in range(self.grid_length_y):

                #on rect minimap (draw with blue color)
                #sq = self.world.world[x][y]["cart_rect_mini_map"]
                #rect = pg.Rect(sq[0][0], sq[0][1], TILE_SIZE_MINI_MAP, TILE_SIZE_MINI_MAP)
                #pg.draw.rect(self.screen,BLUE, rect, 1)


                #on iso_poly minimap (draw with blue color)
                mini = self.world[x][y]["iso_poly_mini"]
                mini = [(x + 200, y + 20) for x,y in mini]        # position x + ...., y  + ...
                pg.draw.polygon(screen, BLUE, mini, 1)

                
                #on our isometric map (red color)
                #create the world's block
                render_pos = self.world[x][y]["render_pos"]

                #this is the world merged with the computer's screen
                #self.screen.blit(self.world.tiles["block"], (render_pos[0] + self.width/2, render_pos[1] + self.height/4))


                #create the other world's object
                tile = self.world[x][y]["tile"]
                if tile != "":
                    screen.blit(self.tiles[tile], 
                                    (render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x, 
                                     render_pos[1] - (self.tiles[tile].get_height() - TILE_SIZE) + camera.scroll.y))



                #Grid on the main map
                #p = self.world.world[x][y]["iso_poly"]
                #p = [(x + self.width/2, y + self.height/4) for x,y in p]
                #pg.draw.polygon(self.screen, RED, p, 1)

        if self.temp_tile is not None:
            iso_poly = self.temp_tile["iso_poly"]
            iso_poly = [(x + self.grass_tiles.get_width()/2 + camera.scroll.x,y + camera.scroll.y) for x,y in iso_poly]
            if self.temp_tile["collision"]:
                pg.draw.polygon(screen, RED, iso_poly, 3)
            else:
                pg.draw.polygon(screen, WHITE, iso_poly, 3)

            render_pos = self.temp_tile["render_pos"]
            screen.blit(
                self.temp_tile["image"],
                (
                    render_pos[0] + self.grass_tiles.get_width()/2 + camera.scroll.x,
                    render_pos[1] - (self.temp_tile["image"].get_height() - TILE_SIZE) + camera.scroll.y
                )
            )







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
            (grid_x * TILE_SIZE_MINI_MAP, grid_y*TILE_SIZE_MINI_MAP ),
            #(grid_x * TILE_SIZE_MINI_MAP, grid_y*TILE_SIZE_MINI_MAP + 5 * TILE_SIZE_MINI_MAP ),                      #left and top location of every square in mini map
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP),
            (grid_x * TILE_SIZE_MINI_MAP, grid_y * TILE_SIZE_MINI_MAP + TILE_SIZE_MINI_MAP)
        ]


        iso_poly = [self.cart_to_iso(x, y) for x,y in rect]
        iso_poly_mini = [self.cart_to_iso(x, y) for x,y in rect_mini_map]

        minx = min([x for x,y in iso_poly])
        miny = min([y for x,y in iso_poly])






        #create a random map
        #Choose a random position in map
        r = random.randint(1, 100)

        #make a group of tree --> a forest
        perlin = 50 * noise.pnoise2(grid_x/self.perlin_scale, grid_y/self.perlin_scale)


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
            "cart_rect": rect,                      #square map
            "cart_rect_mini_map": rect_mini_map,    #square mini map
            "iso_poly": iso_poly,                   #iso_poly map
            "iso_poly_mini": iso_poly_mini,         #isopoly minimap
            "render_pos": [minx, miny],
            "tile": tile,
            "collision": False if tile == "" else True
            #update the attribute here: heal, attack or shield
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











    def mouse_to_grid(self, x, y, scroll):
        # transform to world position (removing camera scroll and offset)
        world_x = x - scroll.x - self.grass_tiles.get_width()/2
        world_y = y - scroll.y
        #transform to card (inverse of card_to_iso)
        card_y = (2*world_y - world_x)/2
        card_x = card_y + world_x
        #transform to grid coordinates
        grid_x = int(card_x // TILE_SIZE)
        grid_y = int(card_y // TILE_SIZE)
        return grid_x, grid_y










    #load our blocks into the game
    def load_images(self):
        block = pg.image.load(path.join(graphics_folder, "block.png")).convert_alpha()
        tree = pg.image.load(path.join(graphics_folder,"tree.png")).convert_alpha()
        rock = pg.image.load(path.join(graphics_folder,"rock.png")).convert_alpha()
        building1 = pg.image.load(path.join(graphics_folder,"building01.png")).convert_alpha()
        building2 = pg.image.load(path.join(graphics_folder,"building02.png")).convert_alpha()

        images = {
            "building1": building1,
            "building2": building2,
            "tree": tree,
            "rock": rock,
            "block": block
        }

        return images
        

    #colision here
    def can_place_tile(self, grid_pos):
        mouse_on_panel = False
        for rect in [self.hud.resources_rect, self.hud.build_rect, self.hud.select_rect]:
            if rect.collidepoint(pg.mouse.get_pos()):      
                #Essentially you pass a co-ordinate to pygame.Rect.collidepoint(), 
                #and it will return True if that point is within the bounds of the rectangle.
                mouse_on_panel = True
        world_bounds = (0 <= grid_pos[0] <= self.grid_length_x) and (0 <= grid_pos[1] <= self.grid_length_x)

        if world_bounds and not mouse_on_panel:
            #print('can place')
            return True
        else:
            #print('cannot place')
            return False
