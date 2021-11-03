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

#Paths definitions
#Gameplay folder
AOE_folder = path.dirname(__file__) #Path of the Project_Python_AoE foler
graphics_folder = path.join(AOE_folder,"assets/graphics") #Path for graphic
building01 = pg.image.load(path.join(graphics_folder,"building01.png"))
building02 = pg.image.load(path.join(graphics_folder,"building02.png"))
building03 = pg.image.load(path.join(graphics_folder,"building03.png"))

resource_TC = [600, 0, 0, 0]
