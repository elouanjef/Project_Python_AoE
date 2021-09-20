import pygame as pg
from game.game import Game


def main():
    running = True
    playing = True

    pg.init()
    pg.mixer.init()

    #the command below does not work on my ubuntu
    #screen = pg.display.set_mode((0,0), pg.FULLSCREEN)

    #this command works better, but it just shows a bigger window
    #screen = pg.display.set_mode((pg.display.Info().current_w, pg.display.Info().current_h), pg.SCALED)

    #problem solved!
    screen = pg.display.set_mode((0, 0), pg.NOFRAME)
    pg.display.toggle_fullscreen()

    clock = pg.time.Clock()

    #implement menus

    #implement game
    game = Game(screen, clock)


    while running:

        #start menu goes here

        while playing:
            # game loop here
            game.run()

if __name__ == '__main__':
    main()