"""the main Menu screen"""


from button_class import ButtonM
from menu_class import Menu
from pygame import mixer
from settings import *
import pygame as pg
from menu_settings import SettingsMenu



class MainMenu(Menu):
    pg.init()

    def __init__(self):
        Menu.__init__(self)
        self.font = pg.font.SysFont('Constantia', 25)  # if we're not changing the font, move it to Menu class
        self.current = "Main"
        self.background = background_main_menu         # if we're not changing the bg for menus, move it to Menu class
        

    def display(self):
        if self.displayed:

            pg.display.set_caption('Age of Cheap Empires')
            
            # buttons
            New_Game = ButtonM(self.screen, self.mid_width, self.mid_height, 'New Game')
            loaded_Games = ButtonM(self.screen, self.mid_width, self.mid_height + GAP, 'loaded Games')
            Settings = ButtonM(self.screen, self.mid_width, self.mid_height + (2*GAP), 'Settings')
            Credits = ButtonM(self.screen, self.mid_width, self.mid_height + (3*GAP), 'Credits')
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (4*GAP), 'Quit')

            # background sound
            #mixer.music.load(music_menu)
            #mixer.music.play(-1)

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Age of Empire", True, (249, 231, 159)), (435, 100))
                if New_Game.check_button():
                    print('you pressed New Game')
                if loaded_Games.check_button():
                    print('you pressed loaded Games')
                if Quit.check_button():
                    run = False
                if Settings.check_button():
                    self.current = "Settings"
                    print(self.current)
                    SettingsMenu().display()
                if Credits.check_button():
                    print('you pressed credits')
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False

                pg.display.update()

            pg.quit()


if __name__ == '__main__':
    MainMenu().display()
