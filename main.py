import pygame as pg
from game.game import Game
from menu import all_menu
from menu.all_menu import All_menus


def main():
    running = True
    playing = True

    # problem solved!
    screen = pg.display.set_mode((0, 0), pg.NOFRAME)
    pg.display.toggle_fullscreen()

    pg.mixer.init()

    # screen = pg.display.set_mode((1500, 950))

    clock = pg.time.Clock()

    # implement menus

    # implement game
    game = Game(screen, clock)

    while running:
        menu = All_menus()
        menu.display_main()
        # start menu goes here
        while playing:
            # game loop here
            game.load = menu.load
            game.run()

if __name__ == '__main__':
    main()
