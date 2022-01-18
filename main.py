import pygame as pg
from game.game import Game
from menu import all_menu
from menu.all_menu import All_menus


def main():
    running = True
    playing = True

    pg.init()
    pg.mixer.init()

    # problem solved!
    screen = pg.display.set_mode((0, 0), pg.NOFRAME)
    pg.display.toggle_fullscreen()

    # screen = pg.display.set_mode((1500, 950))

    clock = pg.time.Clock()

    # implement menus

    # implement game
    game = Game(screen, clock)

    while running:
        menu = All_menus()
        menu.display_main()
        # start menu goes here
        if menu.start:
            while playing:
                # game loop here
                game.run()
        if menu.load:
            game.load = True
            while playing:
                # game loop here
                game.run()


if __name__ == '__main__':
    main()
