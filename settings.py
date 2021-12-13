from os import path
import pygame as pg




TILE_SIZE = 64
TILE_SIZE_MINI_MAP = 4

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (238, 130, 238)
MARRON = (165,42,42)
PURPLE = (128, 0, 128)
MINI_MAP_COLOUR = (64, 64, 64)
HUD_COLOUR = (198, 155, 93, 175)

CONSTRUCTION = 1
DESTROY = 0


# global check_destroy 
# check_destroy = False

check_destroy = False

#Paths definitions
#Gameplay folder
AOE_folder = path.dirname(__file__) #Path of the Project_Python_AoE foler
graphics_folder = path.join(AOE_folder,"assets/graphics") #Path for graphic
#map's ressource
Tree_img = pg.transform.scale(pg.image.load(path.join(graphics_folder,"tree.png")),(143,128))
Rock_img = pg.transform.scale(pg.image.load(path.join(graphics_folder,"rock.png")),(143,128))
Block_img = pg.transform.scale(pg.image.load(path.join(graphics_folder,"block.png")),(143,128))

#buildings
towncenter = pg.transform.scale(pg.image.load(path.join(graphics_folder,"towncenter.png")), (143, 128))
lumbermill = pg.transform.scale(pg.image.load(path.join(graphics_folder,"lumbermill.png")), (143, 128))
barracks = pg.transform.scale(pg.image.load(path.join(graphics_folder,"barracks.png")), (143, 128))
archery = pg.transform.scale(pg.image.load(path.join(graphics_folder,"archery.png")), (143, 128))


#units
archer = pg.transform.scale(pg.image.load(path.join(graphics_folder,"archer.png")), (30,40))
infantryman = pg.transform.scale(pg.image.load(path.join(graphics_folder,"Barbarian.png")), (38,48))
villager = pg.transform.scale(pg.image.load(path.join(graphics_folder,"villager.png")), (30,40))