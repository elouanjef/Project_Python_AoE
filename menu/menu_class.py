"""the Menu class"""

import pygame as pg


class Menu:
    def __init__(self):
        self.displayed = True
        self.screen = pg.display.set_mode((0, 0))
        self.title_font = pg.font.Font('freesansbold.ttf', 300)

    def draw_cursor(self):
        pass

    def blit_screen(self):
        pass



