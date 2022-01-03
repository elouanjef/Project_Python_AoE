"""the Menu class"""


from button_class import ButtonM
from settings import *
import pygame as pg


class Menu:
    def __init__(self):
        self.width = screen_width
        self.height = screen_height
        self.mid_width = (self.width // 2) - (WIDTH_BUTTON // 2)
        self.mid_height = (self.height // 2) - (1.5 * HEIGHT_BUTTON)
        #self.cursor_rect = pg.Rect(0, 0, 20, 20)  # pour ajouter un cursor antique
        self.displayed = True
        self.screen = pg.display.set_mode((screen_width, screen_height))
        self.title_font = pg.font.Font('freesansbold.ttf', 300)


    def draw_cursor(self):
        pass

    def blit_screen(self):
        pass



