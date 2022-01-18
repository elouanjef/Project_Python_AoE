"""the main Menu screen"""

from .button_class import ButtonM
from .menu_class import Menu
from pygame import mixer
from .settings_for_menu import *
import pygame as pg


class All_menus(Menu):
    pg.init()

    def __init__(self):
        Menu.__init__(self)
        self.font = pg.font.SysFont('Constantia', 25)  # if we're not changing the font, move it to Menu class
        self.current = "Main"
        self.background = background_main_menu  # if we're not changing the bg for menus, move it to Menu class
        self.mid_width = (self.screen.get_width() // 2) - (WIDTH_BUTTON // 2)
        self.mid_height = (self.screen.get_height() // 2) - (1.5 * HEIGHT_BUTTON)
        self.start = False
        self.load = False

    def display_main(self):
        if self.displayed:

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            New_Game = ButtonM(self.screen, self.mid_width, self.mid_height - GAP, 'New Game')
            loaded_Games = ButtonM(self.screen, self.mid_width, self.mid_height, 'Load Game')
            Settings = ButtonM(self.screen, self.mid_width, self.mid_height + GAP, 'Settings')
            Credits = ButtonM(self.screen, self.mid_width, self.mid_height + (2 * GAP), 'Credits')
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3 * GAP), 'Quit')

            # background sound
            # mixer.music.load(music_menu)
            # mixer.music.play(-1)

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Age of Cheap Empires", True, (0, 0, 0)),
                                 (self.mid_width, self.mid_height - (2 * GAP)))
                if New_Game.check_button():
                    self.start = True
                    run = False
                if loaded_Games.check_button():
                    self.load = True
                    run = False
                    print('you pressed Load Game')
                if Quit.check_button():
                    run = False
                if Settings.check_button():
                    self.current = "Settings"
                    self.display_settings()
                if Credits.check_button():
                    print('coming soon')
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False

                pg.display.update()

    def display_settings(self):
        if self.displayed:

            pg.display.set_caption('Age of Cheap Empires')


            # buttons
            Full_Screen = ButtonM(self.screen, self.mid_width, self.mid_height, 'Full Screen')
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3*GAP), 'Quit')
            Vol_up = ButtonM(self.screen, self.mid_width + (3*GAP), self.mid_height + GAP, '+')
            Vol_down = ButtonM(self.screen, self.mid_width - (3*GAP), self.mid_height + GAP, '-')
            Return = ButtonM(self.screen, self.mid_width, self.mid_height - GAP, 'Return')

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

                if Return.check_button():
                    self.current = "Main"
                    self.display_main()

                if Quit.check_button():
                    run = False
                    pg.quit()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False

                pg.display.update()

if __name__ == '__main__':
    All_menus().display_main()
