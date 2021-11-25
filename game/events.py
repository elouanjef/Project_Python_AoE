
import pygame as pg
import sys


class Event:
    def __init__(self,clock) -> None:
        self.destroy = False
        self.troop = None
        self.clock = clock
        self.timer = 0
        self.dt = clock.tick(30)/1000
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
                    self.destroy = True
                    self.timer = 0.0001


    def set_destroy(self):
        self.destroy = True
        self.update_destroy()


    def remise(self):
        self.destroy = False

    def get_destroy(self):
        return self.destroy

    def update_destroy(self):
        if (self.timer != 0):
            if (self.timer > 0.5):
                #print("too late")
                self.timer = 0
                self.destroy = False
            else:
                self.timer += self.dt
        return self.destroy

    def create_troop(self, troop):
        self.troop = str(troop)

    def get_troop(self):
        return self.troop

    def remise_troop(self):
        self.troop = None

