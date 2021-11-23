
import pygame as pg
import sys


class Event:
    def __init__(self,clock) -> None:
        self.destroy = False
        self.clock = clock
        self.timer = 0
        # / 1000 to convert milliseconds to seconds.
        self.dt = self.clock.tick(30) / 1000
    #capture the events
    def events(self):
        for event in pg.event.get():
            #Exit the game by clicking the red cross
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            #Exit game by pressing escape (Echap in fr)  button on the keyboard
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    sys.exit()

                if event.key == pg.K_DELETE:
                    self.timer += self.dt
                    self.destroy = True


    def set_destroy(self):
        self.destroy = True

    # def count(self):
    #     self.timer += self.dt
    #     if self.timer > 0.5:
    #         self.remise()

    def remise(self):
        self.destroy = False

    def get_destroy(self):
        return self.destroy
