"""the main Menu screen"""

import pygame
from button_menu import Button_m
from pygame import mixer
from settings import *
from main import main


pygame.init()


screen_width = 1024
screen_height = 576

screen = pygame.display.set_mode((0, 0), pg.NOFRAME)
pygame.display.set_caption('Age of Cheap Empires')

font = pygame.font.SysFont('Constantia', 25)

# define colours
black = (0, 0, 0)
white = (255, 255, 255)

# define global variable
clicked = False


# add formulas instead of values
New_Game = Button_m(screen, 420, 280, 'New Game')
loaded_Games = Button_m(screen, 420, 340, 'Loaded Games')
Settings = Button_m(screen, 420, 400, 'Settings')
Credits = Button_m(screen, 420, 520, 'Credits')
Quit = Button_m(screen, 420, 460, 'Quit')

# Background 
background = background_main_menu

# background sound
mixer.music.load(music_menu)
mixer.music.play(-1)

# Title
title_font = pygame.font.Font('freesansbold.ttf', 300)


run = True
while run:

	screen.fill((255, 255, 255))
	# Background Image
	screen.blit(background, (0, 0))
	screen.blit(font.render("Age of Cheap Empires", True, (249, 231, 159)), (435, 100))

	if New_Game.check_button():
		print('You pressed New Game')
		main()
	if loaded_Games.check_button():
		print('You pressed loaded Games')
	if Quit.check_button():
		print('You pressed Quit')
		run = False
	if Settings.check_button():
		print('You pressed Settings')
	if Credits.check_button():
		print('You pressed Credits')

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

	pygame.display.update()


pygame.quit()
