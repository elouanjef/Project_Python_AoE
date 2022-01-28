"""the Menu class"""

import pygame as pg


class Menu:
    def __init__(self):
        self.displayed = True
        self.screen = pg.display.set_mode((0, 0), pg.NOFRAME)
        pg.display.toggle_fullscreen()

    def draw_cursor(self):
        pass

    def blit_screen(self):
        pass



