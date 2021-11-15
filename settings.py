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
image_T = pg.image.load(path.join(graphics_folder,"building01.png"))
image_M = pg.image.load(path.join(graphics_folder,"building02.png"))
image_B = pg.image.load(path.join(graphics_folder,"building02.png"))

resource_TC = [600, 0, 0, 0]
