"""the class for all the botton used in the various menus"""

import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from sys import _xoptions
from typing import Text
from settings import *
import pygame
from pygame.locals import *
from main import *


class Button_m():
    def __init__ (self, screen, x, y, text):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = WIDTH_BUTTON
        self.height = HEIGHT_BUTTON
        self.button_rect = Rect(self.x, self.y, self.width, self.height)
        self.text = text
        self.font = pygame.font.SysFont('Constantia', 30)
        self.clicked = False
        self.button_col = YELLOW_LIGHT
        self.hover_col = BEIGE
        self.click_col = GOLD
        self.text_col = BLACK

    def check_button(self):
        global clicked
        action = False

        pos = pygame.mouse.get_pos()
        mouse_action = pygame.mouse.get_pressed()

        if self.button_rect.collidepoint(pos):
            if mouse_action[0]:
                clicked = True
                pygame.draw.rect(self.screen, self.click_col, self.button_rect)
                clicked = False
                action = True

            else:
                pygame.draw.rect(self.screen, self.hover_col, self.button_rect)
        else:
                pygame.draw.rect(self.screen, self.button_col, self.button_rect)

        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 12))
        return action