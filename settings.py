from os import path
import pygame as pg


# Buttons
HEIGHT_BUTTON = 50
WIDTH_BUTTON = 250
GAP = 75      # gap between the buttons

# Window
screen_width = 1024
screen_height = 576

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BURGUNDY = (179, 57, 57)
GOLD = (255, 215, 200)
YELLOW_LIGHT = (249, 231, 159)
BEIGE = (255, 253, 208)
GREEN_DARK = (9, 48, 22)
BLUE_SKY = (122, 215, 255)
PINK = (255, 88, 150)
HUD_COLOUR = (198, 155, 93, 175)


menuf = path.dirname(__file__) #Path of the Project_Python_AoE foler
data_image = path.join(menuf,"data/bg_imgs") #Path for graphic
data_son = path.join(menuf,"data/sounds") #Path for graphic

background_main_menu = pg.image.load(path.join(data_image,"background.png"))
music_menu = path.join(data_son,"sound1.mp3")