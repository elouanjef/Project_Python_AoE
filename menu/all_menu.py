"""the main Menu screen"""
import pygame.mixer

from .button_class import ButtonM
from .menu_class import Menu
from pygame import mixer
from .settings_for_menu import *
import pygame as pg
import sys

class All_menus(Menu):
    pg.init()

    def __init__(self):

        Menu.__init__(self)


    def display_main(self):
        if self.displayed:

            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            New_Game = ButtonM(self.screen, self.mid_width, self.mid_height - GAP, 'New Game')
            loaded_Games = ButtonM(self.screen, self.mid_width, self.mid_height, 'Load Game')
            Settings = ButtonM(self.screen, self.mid_width, self.mid_height + GAP, 'Settings')
            Credits = ButtonM(self.screen, self.mid_width, self.mid_height + (2 * GAP), 'Credits')
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3 * GAP), 'Quit')




            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Age of Cheap Empires", True, (249, 231, 159)),
                                 (self.mid_width - (3.5*GAP), self.mid_height - (2.5 * GAP)))
                if New_Game.check_button():
                    self.start = True
                    run = False

                if loaded_Games.check_button():
                    self.load = True
                    run = False

                if Quit.check_button():
                    run = False
                    sys.exit()

                if Settings.check_button():
                    self.current = "Settings"
                    self.display_settings()
                    run = False

                if Credits.check_button():
                    self.current = "Credits"
                    self.display_credits()
                    run = False

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        sys.exit()

                pg.display.update()
                clock.tick(30)

    def display_pause(self):
        if self.displayed:

            self.current = "Pause"
            self.pause = True
            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3*GAP), 'Quit')
            Resume = ButtonM(self.screen, self.mid_width, self.mid_height - GAP*2, 'Resume')
            Settings = ButtonM(self.screen, self.mid_width, self.mid_height + GAP, 'Settings')
            Save = ButtonM(self.screen, self.mid_width, self.mid_height + 2*GAP, 'Save Game')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Pause", True, (249, 231, 159)), (self.mid_width*0.98, self.mid_height - GAP*3.25))

                if Settings.check_button():
                    self.current = "Settings"
                    self.display_settings()
                    run = False

                if Resume.check_button():
                    self.pause = False
                    run = False

                if Quit.check_button():
                    self.pause = False
                    run = False
                    sys.exit()

                if Save.check_button():
                    self.save = True
                    self.pause = False
                    run = False

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()

                pg.display.update()
                clock.tick(30)

    def display_settings(self):
        if self.displayed:

            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            # buttons
            Quit = ButtonM(self.screen, self.mid_width, self.mid_height + (3*GAP), 'Quit')
            Vol_up = ButtonM(self.screen, self.mid_width + (3.5*GAP), self.mid_height + GAP, '+')
            Vol_down = ButtonM(self.screen, self.mid_width - (3.5*GAP), self.mid_height + GAP, '-')
            Return = ButtonM(self.screen, self.mid_width, self.mid_height - GAP * 1.5, 'Return')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Settings", True, (249, 231, 159)), (self.mid_width*0.97, self.mid_height - GAP*3.25))
                self.screen.blit(self.font2.render("Volume", True, (249, 231, 159)), (self.mid_width * 0.98 + (0.6 * GAP), self.mid_height + GAP))

                if Vol_down.check_button():
                    if self.volume > 0.0 :
                        self.volume -= 0.1
                        mixer.music.set_volume(self.volume)

                if Vol_up.check_button():
                    if self.volume < 1.0:
                        self.volume += 0.1
                        mixer.music.set_volume(self.volume)

                if Return.check_button():
                    run = False
                    if not self.pause:
                        self.current = "Main"
                        self.display_main()
                    else:
                        self.current = "Pause"
                        self.display_pause()

                if Quit.check_button():
                    run = False
                    sys.exit()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        pg.quit()

                pg.display.update()
                clock.tick(30)

    def display_credits(self):
        if self.displayed:

            clock = pygame.time.Clock()

            pg.display.set_caption('Age of Cheap Empires')

            Return = ButtonM(self.screen, self.mid_width, self.mid_height - GAP*2, 'Return')

            run = True
            while run:
                self.screen.fill((255, 255, 255))
                self.screen.blit(self.background, (0, 0))
                self.screen.blit(self.font.render("Nguyen Cong Khai", True, (249, 231, 159), (0, 0, 0)), (self.mid_width*0.95, self.mid_height + GAP))
                self.screen.blit(self.font.render("Elouan Rabouin", True, (249, 231, 159), (0, 0, 0)),
                                 (self.mid_width * 0.95, self.mid_height + GAP * 2))
                self.screen.blit(self.font.render("Pham Ngoc Tuan", True, (249, 231, 159), (0, 0, 0)),
                                 (self.mid_width * 0.95, self.mid_height + GAP * 3))
                self.screen.blit(self.font.render("Le Quang Tan", True, (249, 231, 159), (0, 0, 0)),
                                 (self.mid_width * 0.95, self.mid_height + GAP * 4))
                self.screen.blit(self.font.render("Nguyen Ngoc Khanh Hoai", True, (249, 231, 159), (0, 0, 0)),
                                 (self.mid_width * 0.95, self.mid_height + GAP * 5))
                self.screen.blit(self.font.render("Zakaria Bahraoui", True, (249, 231, 159), (0, 0, 0)),
                                 (self.mid_width * 0.95, self.mid_height + GAP * 6))

                if Return.check_button():
                    run = False
                    self.current = "Main"
                    self.display_main()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        run = False
                        sys.exit()

                pg.display.update()
                clock.tick(30)

if __name__ == '__main__':
    pg.init()
    All_menus().display_main()
