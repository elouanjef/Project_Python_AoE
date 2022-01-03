"""the Credits Menu screen"""

from button_class import ButtonM
from pygame.locals import *
from menu_class import Menu
from settings import *
import pygame as pg


class SettingsMenu(Menu):
    pg.init()

    def __init__(self):
        Menu.__init__(self)
        self.font = pg.font.SysFont('Constantia', 25)
        self.current = "Settings"
        self.background = background_main_menu

    def display(self):
        if self.displayed:

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            Full_Screen = ButtonM(self.screen, self.mid_width, self.mid_height, 'Full Screen')
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3*GAP), 'Quit')
            Vol_up = ButtonM(self.screen, self.mid_width + (3*GAP), self.mid_height + GAP, '+')
            Vol_down = ButtonM(self.screen, self.mid_width - (3*GAP), self.mid_height + GAP, '-')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Settings", True, (249, 231, 159)), (self.mid_width + (1.5*GAP), self.mid_height - GAP))
                if Full_Screen.check_button():
                    print('you tried to go full screen')
                if Vol_down.check_button():
                    print('you tried the volume down button')
                if Vol_up.check_button():
                    print('you tried the volume up button')
                if Quit.check_button():
                    run = False
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False

                pg.display.update()

            pg.quit()


